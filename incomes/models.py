from django.db import models
from authentication.models import User



class Income(models.Model):
    
    
    SOURCE_OPTIONS = [
        ('SALARY','SALARY'),
        ('BUSINESS','BUSINESS'),
        ('SIDE-HUSTLE','SIDE-HUSTLE'),
        ('OTHERS','OTHERS')
    ]
    
    source =models.CharField(choices=SOURCE_OPTIONS,max_length=255)
    amounts= models.DecimalField(max_digits=10,max_length=255,decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    date=models.DateField(null=False,blank=False)
    
    
    
    class Meta:
        ordering: ['-date'] # type: ignore
        
    def __str__(self) -> str:
        return str(self.owner)+ 's income'
