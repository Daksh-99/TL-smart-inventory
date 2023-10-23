# items/models.py
from django.db import models

class studentUser(models.Model):
    rfid = models.CharField(max_length=10, null=False, blank=False, primary_key=True)
    roll_number = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class BorrowRecord(models.Model):
    user = models.ForeignKey(studentUser, on_delete=models.CASCADE)
    item = models.CharField(max_length=100,null=False, blank=False)
    borrowed_at = models.DateTimeField(auto_now_add=True, editable=False)
    returned = models.BooleanField(default=False) 

    def __str__(self):
        return self.item
