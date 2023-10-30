from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
# from .forms import *
from django.contrib import messages
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import csv

#admin views

def export_items_csv(request):
    data = csv.reader(open('C:\\Users\\daksh\\Downloads\\Inventory_Mapping_Main.csv'), delimiter=",")
    for row in data:
        item_name = row[0]
        quantity = row[1]
        print(item_name, quantity)
        Item.objects.get_or_create(name=item_name, quantity=quantity)
    return redirect('get_item_names')

def itemlist(request):
    items = Item.objects.all()

    if request.method == "POST":
        ids = request.POST['id']
        name = request.POST['name']
        quantity = request.POST['quantity']
        item = Item.objects.get(id=ids)
        item.name = name
        item.quantity = quantity
        item.save()
        return redirect('itemlist')     

    return render(request, 'itemlist.html', {'items': items})


def get_item_names(request):
    items = Item.objects.all().values_list('name', flat=True)
    items = list(items)
    return JsonResponse(items, safe=False)


def process_rfid_tag(request):
    rfid_tag = request.POST.get('rfid_tag',"")
    request.session['active_student_id'] = rfid_tag

    if rfid_tag and len(rfid_tag) == 10:
        try:
            student = studentUser.objects.get(rfid=rfid_tag)
            return render(request, 'home.html', {'student': student})
        except studentUser.DoesNotExist:
            return redirect('register_student')

    return render(request, 'rfid_input.html')


@csrf_exempt
def home(request):
    rfid_tag = request.POST.get('rfid_tag') or None
    student = None
    if rfid_tag is not None:
        try:
            student = studentUser.objects.get(rfid=rfid_tag)
            request.session['active_student_id'] = rfid_tag
            return JsonResponse({'success': True, 'has_rfid_data': True, 'rfid_data': rfid_tag, 'student': {'name': student.name, 'id': student.rfid}})
        except studentUser.DoesNotExist:
            pass

    return render(request, 'home.html')


def register_student(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        rfid_tag = request.session.get('active_student_id')
        name = request.POST.get('name')

        studentUser.objects.create(roll_number=roll_number, rfid=rfid_tag, name=name)
        return redirect('home')
    
    return render(request, 'register_student.html')

def borrow_item(request):
    if request.method == 'POST':
        rfid_tag = request.session.get('active_student_id')
        student = studentUser.objects.get(rfid=rfid_tag)
        item_name = request.POST.get('item_name')
        item = Item.objects.get(name=item_name)
        
        BorrowRecord.objects.create(user=student, item=item)
        #end user session
        
        return redirect('home')
    
    return render(request, 'borrow_item.html')

def student_items(request):
    rfid_tag = request.session.get('active_student_id')
    student = studentUser.objects.get(rfid=rfid_tag)
    borrowed_items = BorrowRecord.objects.filter(user=student, returned=False)

    if request.method == 'POST':
        selected_item_id = request.POST.get('submit_item')
        if selected_item_id:
            # Get the item based on the selected_item_id
            item_to_return = BorrowRecord.objects.get(id=selected_item_id)
            item_to_return.returned = True
            item_to_return.save()
            # You can add additional logic here if needed

            return redirect('student_items')

    return render(request, 'student_items.html', {'borrowed_items': borrowed_items})
