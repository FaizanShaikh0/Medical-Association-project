from django.db import models

# Create your models here.

# class company(models.Model):
#     company_name = models.CharField(max_length=200)
#     stockiest_name = models.CharField(max_length=200)


class CSP(models.Model):
    company_name = models.CharField(max_length=200)
    stockiest_name = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    pcontain = models.CharField(max_length=500)
    mobile = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20)



