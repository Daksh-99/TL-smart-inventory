# items/models.py
from django.db import models

class studentUser(models.Model):
    rfid = models.CharField(max_length=10, null=False, blank=False, primary_key=True)
    roll_number = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    
    def __str__(self):
        return self.name


class BorrowRecord(models.Model):
    user = models.ForeignKey(studentUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True, editable=False)
    returned = models.BooleanField(default=False) 
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.item.name + ' - ' + self.user.name
