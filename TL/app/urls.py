# rfidapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [    
    path('newitem/', newitem, name='newitem'),
    path('itemlist/', itemlist, name='itemlist'),#admin use
    path('total_borrowed/', total_borrowed, name='total_borrowed'),#admin use
    path('item_names/', get_item_names, name='get_item_names'),
    path('', process_rfid_tag, name='process_rfid_tag'),
    path('home/', home, name='home'),
    path('register_student/', register_student, name='register_student'),
    path('borrow_item/', borrow_item, name='borrow_item'),
    path('student_items/', student_items, name='student_items'),
]
