from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.

class SudokuMatrix(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matrix = models.TextField()  # Store serialized matrix (JSON)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_matrix(self, matrix_data):
        self.matrix = json.dumps(matrix_data)

    def get_matrix(self):
        return json.loads(self.matrix)
