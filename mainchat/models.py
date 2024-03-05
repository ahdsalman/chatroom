from django.db import models
from chatapp.models import User
# Create your models here.



class Chating(models.Model):
    room = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    username=models.CharField(max_length =100)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "chat_message"
        ordering = ("timestamp",)