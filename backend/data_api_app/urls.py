from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_videos),
    path('read/', views.get_video),
    path('create/', views.add_video),
    path('delete/', views.del_video),
    path('update/', views.edit_video),
]
