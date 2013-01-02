from django.db import models
from users.models import UserProfile

# Create your models here.
class BarcodeMap(models.Model):
    """
    Maps barcode to participant
    """
    barcode = models.CharField(max_length=128,blank=True)
    shaastra_id = models.ForeignKey(UserProfile, blank=True, null=True)  
    
    def __str__(self):
        return self.barcode

