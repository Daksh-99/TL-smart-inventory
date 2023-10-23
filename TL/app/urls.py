# rfidapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('rfid/', process_rfid_tag, name='process_rfid_tag'),
    path('', home, name='home'),
    path('register_student/', register_student, name='register_student'),
    path('borrow_item/', borrow_item, name='borrow_item'),
    path('return_item/<int:student_id>/', return_item, name='return_item'),
    path('student_items/', student_items, name='student_items'),
]
