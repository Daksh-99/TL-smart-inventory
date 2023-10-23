from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
# from .forms import *
from django.contrib import messages
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response


def process_rfid_tag(request):
    rfid_tag = request.POST.get('rfid_tag',"")
    print(rfid_tag)
    request.session['active_student_id'] = rfid_tag

    if rfid_tag and len(rfid_tag) == 10:
        # Check if the user with the provided RFID tag exists
        try:
            student = studentUser.objects.get(rfid=rfid_tag)
            return render(request, 'home.html', {'student': student})
        except studentUser.DoesNotExist:
            return redirect('register_student')

    # Invalid RFID tag or tag not provided, return to the RFID input page
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

    print("No RFID tag found")
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
        
        BorrowRecord.objects.create(user=student, item=item_name)
        #end user session
        
        return redirect('home')
    
    return render(request, 'borrow_item.html')

def return_item(request, student_id):
    student = studentUser.objects.get(rfid=student_id)
    borrowed_items = BorrowRecord.objects.filter(user = student, returned=False)
    
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        BorrowRecord.objects.filter(id__in=selected_items).update(returned=True)
        
        return redirect('return_item', student_id=student_id)
    
    return render(request, 'return_item.html', {'borrowed_items': borrowed_items})

# def student_items(request):
#     rfid_tag = request.session.get('active_student_id')
#     student = studentUser.objects.get(rfid=rfid_tag)
#     borrowed_items = BorrowRecord.objects.filter(user= student, returned=False)
#     return render(request, 'student_items.html', {'borrowed_items': borrowed_items})

from django.shortcuts import render, redirect

# ... your other imports ...

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
