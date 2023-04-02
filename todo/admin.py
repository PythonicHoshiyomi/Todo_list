from django.contrib import admin
from .models import ToDoList,ToDoItem

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(ToDoItem)