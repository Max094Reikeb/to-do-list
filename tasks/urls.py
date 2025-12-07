from django.urls import path

from tasks.views import deleteTask, index, updateTask

urlpatterns = [
    path('', index, name="list"),
    path('update_task/<str:pk>/', updateTask, name="update_task"),
    path('delete_task/<str:pk>/', deleteTask, name="delete_task")

]
