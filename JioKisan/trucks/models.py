from django.db import models


# Create your models here.

statusChoices = (
    ("PENDING","Pending"),
    ("ASSIGNED","Assigned"),
    ("TRANSIT","Transit"),
    ("COMPLETED", "Completed")
)

class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100, default = "None")
    currentPositionLongitude = models.FloatField(default =0.00)
    currentPositionLatitude = models.FloatField(default =0.00)
    homeAddressLongitude = models.FloatField(default =0.00)
    homeAddressLatitude = models.FloatField(default =0.00)
    truckCapacity = models.IntegerField(blank=True)
    hired = models.BooleanField(default=False)
    currentCapacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name




class Delivery(models.Model):
    pickupLocationLongitude = models.FloatField(default =0.00)
    pickupLocationLatitude = models.FloatField(default =0.00)
    dropLocationLongitude = models.FloatField(default =0.00)
    dropLocationLatitude = models.FloatField(default =0.00)
    pickupDate = models.DateTimeField()
    dropDate = models.DateTimeField()
    weight = models.IntegerField()
    status = models.CharField(max_length=25,choices = statusChoices, default="PENDING")





    

