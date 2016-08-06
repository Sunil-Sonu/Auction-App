from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Categories(models.Model):

    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name



class UserProfile(models.Model):
    user=models.OneToOneField(User)
    userimage=models.ImageField(upload_to='userimages')
    address=models.TextField()
    contact=models.CharField(max_length=10,blank=True)

    def __unicode__(self):
        return self.user.first_name


class Products(models.Model):
    current=models.ForeignKey(UserProfile)
    pname = models.CharField(max_length=30)
    pimage=models.ImageField(upload_to='productimages')
    description = models.TextField()
    postdate = models.DateField(auto_now_add=True)
    finaldate = models.DateField(blank=True,null=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    bidprice = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    sold = models.BooleanField(default=False)
    list = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.pname

class BidDetails(models.Model):
    userinfo=models.ForeignKey(UserProfile)
    bid=models.ForeignKey(Products)
    userbid=models.IntegerField(default=0,validators=[MinValueValidator(0)])
    won = models.BooleanField(default=False)

    def __unicode__(self):
        return self.userinfo.user.first_name

