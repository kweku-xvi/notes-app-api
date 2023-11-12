from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_note_view, name='create_note'),
    path('<uuid:note_id>/', views.get_note_view, name='get_note'),
    path('<uuid:note_id>/update/', views.update_note_view, name='update_note'),
    path('<uuid:note_id>/delete/', views.delete_note_view, name='update_note'),
    path('user/', views.all_user_notes_view, name='all_user_notes'),
]