from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('',views.dashboard_view,name='dashboard'),
     path('create_note/', views.create_note, name='create_note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
]