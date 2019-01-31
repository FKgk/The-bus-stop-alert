from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from .fields import CommaSeparatedCharField

class User_infomation(models.Model):
    start = models.CharField(max_length = 20, blank = True, null = True)
    terminate = models.CharField(max_length = 20, blank = True, null = True)
    bus_num = models.IntegerField()
    user_id = models.IntegerField()
    
    def __str__(self):
        return self.start + " -> " + self.terminate + " (" + str(self.bus_num) + "번) / userID : " + str(self.user_id)
    
class Bus_cancel_list(models.Model):
    start = models.CharField(max_length = 20, blank = True, null = True)
    terminate = models.CharField(max_length = 20, blank = True, null = True)
    bus_num = models.IntegerField(blank = True)
    user_id = models.IntegerField(primary_key = True, unique = True)
    status = models.BooleanField(default = True)
    runningstatus = models.BooleanField(default = False)
    
    def __str__(self):
        return str(self.status)

class Alarm(models.Model):
    user_id = models.IntegerField(primary_key = True, unique = True)
    card_id = models.CharField(max_length = 20, blank = True, null = True)
    time = models.IntegerField(default = 0)
    status = models.BooleanField(default = False)
    
    def __str__(self):
        return str(self.time)
    