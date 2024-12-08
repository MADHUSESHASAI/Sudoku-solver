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
            save_matrix_to_file(request.user, resultB)
            return render(request,'result.html',context={'list':resultB,'result':True})
        else:
            return render(request,'result.html',context={'result':False})
        
    return render(request,'game.html',context={'list':values} )

#Rajesh

#1. for saving the matrix
def save_matrix_to_file(user, matrix_data):
    matrix_dir = 'C:\\Users\\ACER\\Desktop\\project\\Sudoku-solver\\Sudokusolver\\matrices\\'
    if not os.path.exists(matrix_dir):
        os.makedirs(matrix_dir)
    i = 1
    while os.path.exists(os.path.join(matrix_dir, f'{user.username}_matrix_{i}.pkl')):
        i += 1
    file_path = os.path.join(matrix_dir, f'{user.username}_matrix_{i}.pkl')
    with open(file_path, 'wb') as f:
        pickle.dump(matrix_data, f)
    print(f"Successfully saved as {file_path}")
    load_matrix_from_file(user)


#2. load the single matrix
def load_matrix_from_file(user):
    file_name = f"{user.username}_matrix.pkl"
    file_path = os.path.join("matrices", file_name)
    if not default_storage.exists(file_path):
        return JsonResponse({"error": "Matrix not found."}, status=404)
    with default_storage.open(file_path, 'rb') as f:
        matrix = pickle.load(f)
    print(matrix)
    return JsonResponse({"matrix": matrix})

#3. history page
def history(request):
    user_matrices = get_matrices_for_user(request.user)
    print(user_matrices) 
    return render(request, 'history.html', {'user_matrices': user_matrices})

#4. to get multiple matrices
def get_matrices_for_user(user):
    BASE_DIR = 'C:\\Users\\ACER\\Desktop\\project\\Sudoku-solver\\Sudokusolver\\matrices\\'
    user_matrices = []
    all_files = os.listdir(BASE_DIR)
    print(f"All files in directory: {all_files}")
    for filename in all_files:
        if filename.startswith(user.username):
            file_path = os.path.join(BASE_DIR, filename)
            with open(file_path, 'rb') as f:
                matrix = pickle.load(f)  
                print(f"Loaded matrix from {filename}: {matrix}")
                user_matrices.append({
                    'filename': filename,
                    'matrix': matrix
                })
    print(f"User matrices found: {user_matrices}")  
    return user_matrices