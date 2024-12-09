from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from collections import defaultdict
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.http import JsonResponse
import pickle
import os
from .models import SudokuMatrix

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def loginpage(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/game')
            else:
                messages.error(request, 'Invalid Username or Password')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.extend(errors)
            messages.error(request, " ".join(error_messages))
    else:
        form = AuthenticationForm()
    return render(request, 'loginpage.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/loginpage')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.extend(errors)
            messages.error(request, " ".join(error_messages))
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


#madhu 
def solveSudoku(board):
   
    def isvalid(row,col,num):
        for i in range(9):
            if board[i][col]==num or board[row][i]==num:
                return False
        r=(row//3)*3
        c=(col//3)*3

        for i in range(r,r+3):
            for j in range(c,c+3):
                if board[i][j]==num:
                    return False
        return True

    for row in range(9):
        for col in range(9):
            if board[row][col] == '':
                for num in '123456789':       
                    if isvalid(row, col, num):
                        board[row][col] = num            
                        if solveSudoku(board):
                            return True              
                        board[row][col] = ''
                return False
    return True



        
def isValidSudoku(board):
        row=defaultdict(set)
        col=defaultdict(set)
        grid=defaultdict(set)
        for i in range(9):
            for j in range(9):
                if board[i][j]=='':
                    continue
                if  board[i][j]  in col[j] or  board[i][j] in row[i] or board[i][j] in grid[(i//3,j//3)]:
                    return False
                else:
                    col[j].add(board[i][j])
                    row[i].add(board[i][j])
                    grid[(i//3,j//3)].add(board[i][j])
        return True



def game(request):
    values=['?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',]
    if request.method=='POST':
        data=request.POST
        
        for i in range(1,82):
            values[i-1]=data[str(i)]
        board=[]
        for i in range(0, len(values), 9):
            x = i
            board.append(values[x:x+9])
        if isValidSudoku(board):
            solveSudoku(board)
            print(board)
            resultB=[]
            for sublist in board:
                resultB.extend(sublist)
            save_matrix_to_db(request.user, resultB)
            return render(request,'result.html',context={'list':resultB,'result':True})
        else:
            return render(request,'result.html',context={'result':False})
        
    return render(request,'game.html',context={'list':values} )

#Rajesh



#3. history page
def history(request):
    user_matrices = get_matrices_for_user(request.user)
    return render(request, 'history.html', {'user_matrices': user_matrices})


def save_matrix_to_db(user, matrix_data):
    # Serialize the matrix and save it to the database
    sudoku_matrix = SudokuMatrix(user=user)
    sudoku_matrix.set_matrix(matrix_data)
    sudoku_matrix.save()
    print(f"Successfully saved matrix for user: {user.username}")


def load_matrix_from_db(user, matrix_id):
    try:
        sudoku_matrix = SudokuMatrix.objects.get(id=matrix_id, user=user)
        matrix = sudoku_matrix.get_matrix()
        print(f"Loaded matrix for user: {user.username}")
        return JsonResponse({"matrix": matrix})
    except SudokuMatrix.DoesNotExist:
        return JsonResponse({"error": "Matrix not found."}, status=404)
    

def get_matrices_for_user(user):
    matrices = SudokuMatrix.objects.filter(user=user).order_by('-created_at')
    user_matrices = [
        {
            'id': matrix.id,
            'matrix': matrix.get_matrix(),
            'created_at': matrix.created_at
        }
        for matrix in matrices
    ]
    return user_matrices
