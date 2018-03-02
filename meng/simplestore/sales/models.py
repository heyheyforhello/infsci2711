from django.db import models
from django.core.validators import MinValueValidator
from simplestore.checkout.models.address import Address

# # Create your models here.
# class Region(models.Model):
#     # use default id as region id
#     REGION_CHOICES = (
#     ('NE', 'Northeast'),
#     ('SE', 'Southeast'),
#     ('MW', 'Midwest'),
#     ('SW', 'Southwest'),
#     ('W', 'West'),
#     )
#     region_name = models.CharField(max_length=2,choices=REGION_CHOICES)


class Store(models.Model):
    # use default id as store id
    aid = models.OneToOneField(Address,on_delete=models.CASCADE)
    #region_id = models.OneToOneField(Region,on_delete=models.CASCADE)
    employee_number = models.PositiveIntegerField()
    store_name = models.CharField(max_length=255)

    REGION_CHOICES = (
    ('NE', 'Northeast'),
    ('SE', 'Southeast'),
    ('MW', 'Midwest'),
    ('SW', 'Southwest'),
    ('W', 'West'),
    )
    region_name = models.CharField(max_length=2,choices=REGION_CHOICES)

class Salesperson(models.Model):
    # use id as Salesperson id
    TITLE_CHOICES= (
       ('S', 'Saler'),
       ('M', 'Store_manager'),
       ('R', 'Region_manager'),
    )

    job_title = models.CharField(max_length=1, choices=TITLE_CHOICES)
    salary = models.FloatField(validators = [MinValueValidator(0),])
    store_id = models.OneToOneField(Store,on_delete=models.CASCADE)
