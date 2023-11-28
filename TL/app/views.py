from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
# from .forms import *
from django.contrib import messages
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import csv
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from .decorators import allow_specific_ip

#admin views

# def export_items_csv(request):
#     data = csv.reader(open('C:\\Users\\daksh\\Downloads\\Inventory_Mapping_Main.csv'), delimiter=",")
#     for row in data:
#         item_name = row[0]
#         quantity = row[1]
#         print(item_name, quantity)
#         Item.objects.get_or_create(name=item_name, quantity=quantity)
#     return redirect('get_item_names')

@staff_member_required
def newitem(request):
    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        Item.objects.create(name=name, quantity=quantity)
        return redirect('itemlist')
    return render(request, 'newitem.html')

@staff_member_required
def total_borrowed(request):
    borrowed_items = BorrowRecord.objects.filter(returned=False)
    #can return upto a limit(eg: recent 100 records)
    returned_items = BorrowRecord.objects.filter(returned=True).order_by('-returned_at')

    return render(request, 'total_borrowed.html', {'borrowed_items': borrowed_items, 'returned_items': returned_items})

@staff_member_required
@api_view(['GET','POST'])
def itemlist(request):
    items = Item.objects.all().order_by('name')

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

@api_view(['GET','POST'])
def process_rfid_tag(request):
    if 'active_student_id' in request.session:
        del request.session['active_student_id']    
    rfid_tag = request.POST.get('rfid_tag',None)
    request.session['active_student_id'] = rfid_tag

    if rfid_tag and len(rfid_tag) == 10:
        try:
            student = studentUser.objects.get(rfid=rfid_tag)
            return render(request, 'home.html', {'student': student})
        except studentUser.DoesNotExist:
            return redirect('register_student')

    return render(request, 'rfid_input.html')

@api_view(['GET','POST'])
def home(request):
    rfid_tag = None
    if request.session['active_student_id'] is not None:
        rfid_tag = request.session['active_student_id']
    student = None
    if rfid_tag is not None:
        try:
            student = studentUser.objects.get(rfid=rfid_tag)
            request.session['active_student_id'] = rfid_tag
            return render(request, 'home.html', {'student': student})
        except studentUser.DoesNotExist:
            pass

    return render(request, 'home.html', {'student': student})

@api_view(['GET','POST'])
def register_student(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        rfid_tag = request.session.get('active_student_id')
        name = request.POST.get('name')

        studentUser.objects.create(roll_number=roll_number, rfid=rfid_tag, name=name)
        return redirect('home')
    
    return render(request, 'register_student.html')

@api_view(['GET','POST'])
def borrow_item(request):
    if request.session['active_student_id'] is not None:
        if request.method == 'POST':
            rfid_tag = request.session.get('active_student_id')
            student = studentUser.objects.get(rfid=rfid_tag)
            item_name = request.POST.get('item_name')
            item = Item.objects.get(name=item_name)
        
            BorrowRecord.objects.create(user=student, item=item)
            return redirect('home')
    
        return render(request, 'borrow_item.html')
    else:
        return redirect('process_rfid_tag')

@api_view(['GET','POST'])
def student_items(request):
    if request.session['active_student_id'] is not None:
        rfid_tag = request.session.get('active_student_id')
        student = studentUser.objects.get(rfid=rfid_tag)
        borrowed_items = BorrowRecord.objects.filter(user=student, returned=False)
        empty_message = ""
        if borrowed_items.count() == 0:
            empty_message = "No records found"

        if request.method == 'POST' :
            selected_item_id = request.POST.get('submit_item')
            if selected_item_id:
                item_to_return = BorrowRecord.objects.get(id=selected_item_id)
                item_to_return.returned = True
                item_to_return.returned_at = datetime.now()
                item_to_return.save()

                return redirect('home')

        return render(request, 'student_items.html', {'borrowed_items': borrowed_items, 'empty_message': empty_message})
    else:
        return redirect('process_rfid_tag')
