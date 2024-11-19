from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.

class HeartData(models.Model):
    age = models.IntegerField()
    sex = models.IntegerField()
    cp = models.FloatField()
    trestbps = models.FloatField()
    chol = models.FloatField()
    fbs = models.FloatField()
    restcg = models.FloatField()
    thalach = models.FloatField()
    exang = models.FloatField()
    oldpeak = models.FloatField()
    slope = models.FloatField()
    ca = models.FloatField()
    thal = models.FloatField()
    owner = models.ForeignKey(get_user_model() , on_delete=models.CASCADE , related_name='owner' , null=True)
    date = models.DateField(auto_now_add=True)
    probability = models.FloatField(null=True)
    RandomForest = models.FloatField(null=True)
    BinaryTree = models.FloatField(null=True, blank=True)  # Corrected from BiayTreee
    logisticRegression = models.FloatField(null=True)
    linearRegression = models.FloatField(null=True, blank=True)  # Add this line
    selected_model = models.CharField(max_length=25, null=True)
    def __str__(self):
        return '{} {}'.format(self.owner , self.pk)

class DoctorHospital(models.Model):
    doctor_name = models.CharField(max_length=25)
    hospital_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_no = models.IntegerField()
    Location = models.CharField(max_length=25)

class TrainedModel(models.Model):
    model_type = models.CharField(max_length=50)
    learning_rate = models.FloatField(null=True, blank=True)
    iterations = models.IntegerField(null=True, blank=True)
    max_depth = models.IntegerField(null=True, blank=True)
    n_estimators = models.IntegerField(null=True, blank=True)
    accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_type} - Accuracy: {self.accuracy}"
