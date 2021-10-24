from django.db import models
from django.utils import timezone


# Create your models here.
class image(models.Model):
    img = models.ImageField(upload_to = 'img')
    name = models.CharField(max_length = 20)
class sellor(models.Model):
    parentid = models.ForeignKey(image,on_delete = models.CASCADE,verbose_name = 'source',default = 0)
    img = models.CharField(max_length =200, verbose_name = 'file_name',default = '')
    name = models.CharField(max_length =20)

class merchant(models.Model):
    name = models.CharField(max_length = 30, default = "Not_Registered")
    merchant_id = models.IntegerField(primary_key = True, unique = True)
    category = models.CharField(max_length = 15, default = "NOT_Recognized")
    last_update_time = models.DateTimeField(auto_now = True)
    current_queue_size = models.IntegerField()
    approximate_queue_waiting_time = models.IntegerField(default = 0)
    waiting_time_per_person = models.FloatField()
    
    
    def set_current_queue_size(self,run_model_result):
        self.current_queue_size = run_model_result
        self.save()
    

    def __str__(self):
        return f'{self.name}: Current waiting time is {self.approximate_waiting_time} minute(s). Last update time: {self.last_update_time.strftime("%m/%d/%y %I:%M %p")}.'

    
    def __gt__(self, other):
        return self.current_queue_size > other.current_queue_size

    