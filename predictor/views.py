from django.shortcuts import render, redirect
from sklearn import linear_model
from .forms import Parameters
import pandas as pd
import numpy as np
from . import regressor
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import MinMaxScaler
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import HeartData, DoctorHospital, TrainedModel
from django.core.mail import send_mail
from .regressor import LogisticRegressionModel, find
import logging
from django.db import transaction
from django.http import JsonResponse
import joblib

logger = logging.getLogger(__name__)



def train_logistic_regression_model():
    X, Y = find()  

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.3, random_state=0)

    logistic_model = LogisticRegressionModel(learning_rate=0.001, iterations=50000)  
    logistic_model.fit(X_train, Y_train)

    Y_pred = logistic_model.predict_class(X_test)

    accuracy = np.mean(Y_pred == Y_test)

    return logistic_model, scaler, accuracy



def quickpredict(request):
    if request.method == 'POST':
        form = Parameters(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            cp = form.cleaned_data['cp']
            trestbps = form.cleaned_data['trestbps']
            chol = form.cleaned_data['chol']
            fbs = form.cleaned_data['fbs']
            restcg = form.cleaned_data['restcg']
            thalach = form.cleaned_data['thalach']
            exang = form.cleaned_data['exang']
            oldpeak = form.cleaned_data['oldpeak']
            slope = form.cleaned_data['slope']
            ca = form.cleaned_data['ca']
            thal = form.cleaned_data['thal']

            linear_model, scaler, linear_r2 = train_logistic_regression_model()
            input_features = np.array([[age, sex, cp, trestbps, chol, fbs, restcg, thalach, exang, oldpeak, slope, ca, thal]])
            
            # Scale the input features
            input_features_scaled = scaler.transform(input_features)
            
            # Make prediction using the linear regression model
            linear_pred = linear_model.predict(input_features_scaled)

            threshold = 0.5  # Example threshold for binary classification
            output1 = 1 if linear_pred[0] >= threshold else 0
            danger = 'high' if output1 == 1 else 'low'
            
            return render(request, 'output.html', {'output1': output1, 'danger': danger})
        else:
            print('The form was not valid.')
            return redirect('/')
    else:
        form = Parameters()
        return render(request, 'quickpredict.html', {'form': form})

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Parameters(request.POST)
            if form.is_valid():
                input_features = np.array([[form.cleaned_data[field] for field in form.cleaned_data]])

                logistic_model, scaler, accuracy = train_logistic_regression_model()

                input_features_scaled = scaler.transform(input_features)

                logistic_pred = logistic_model.predict(input_features_scaled)

                output1 = np.clip(logistic_pred[0], 0, 1)
                danger = 'high' if output1 >= 0.5 else 'low'

                saved_data = HeartData(
                    age=form.cleaned_data['age'],
                    sex=form.cleaned_data['sex'],
                    cp=form.cleaned_data['cp'],
                    trestbps=form.cleaned_data['trestbps'],
                    chol=form.cleaned_data['chol'],
                    fbs=form.cleaned_data['fbs'],
                    restcg=form.cleaned_data['restcg'],
                    thalach=form.cleaned_data['thalach'],
                    exang=form.cleaned_data['exang'],
                    oldpeak=form.cleaned_data['oldpeak'],
                    slope=form.cleaned_data['slope'],
                    ca=form.cleaned_data['ca'],
                    thal=form.cleaned_data['thal'],
                    owner=request.user,  
                    probability=output1,
                    linearRegression=accuracy * 100,  # Accuracy percentage for Logistic Regression
                    selected_model="Logistic Regression"
                )
                saved_data.save()

                return render(request, 'output2.html', {
                    'output1': output1 * 100,
                    'danger': danger,
                    'model_used': "Logistic Regression",
                    'accuracy': accuracy * 100  
                })
        else:
            form = Parameters()
            return render(request, 'user.html', {'form': form})

    return render(request, 'index.html')




def record(request):
    if request.user.is_authenticated:
        record_data = HeartData.objects.filter(owner=request.user)
        return render(request, 'record.html', {'record_data': record_data})
    return redirect('/')

def description(request):
    if request.user.is_authenticated:
        record_data = HeartData.objects.filter(owner=request.user)
        return render(request, 'description.html', {'record_data': record_data})
    return redirect('/')

def Train(request):
    if request.user.is_authenticated:
        record_data = HeartData.objects.filter(owner=request.user)
        return render(request, 'Train.html', {'record_data': record_data})
    return redirect('/')

def Test(request):
    if request.user.is_authenticated:
        record_data = HeartData.objects.filter(owner=request.user)
        return render(request, 'Test.html', {'record_data': record_data})
    return redirect('/')

def heartdetail(request):
    if request.user.is_authenticated:
        record_data = HeartData.objects.filter(owner=request.user)
        return render(request, 'heartdetail.html', {'record_data': record_data})
    return redirect('/')

def symptoms(request):
    if request.user.is_authenticated:
        return render(request, 'symptoms.html')
    return redirect('/')

def prevention(request):
    if request.user.is_authenticated:
        return render(request, 'prevention.html')
    return redirect('/')

def doctorhospital(request):
    if request.user.is_authenticated:
        datas = DoctorHospital.objects.all()
        return render(request, 'doctorshospitals.html', {'datas': datas})
    return redirect('/')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        title = request.POST.get('title1')
        message = request.POST.get('message')
        
        send_mail(title, message + '\n' + 'From: ' + name + '\n' + 'Email: ' + email, from_email=email, recipient_list=['saugat@gmail.com'])
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def train_view(request):
    if request.method == 'POST':
        try:
            linear_model, scaler, linear_r2 = train_logistic_regression_model()
            messages.success(request, "Linear Regression model trained and saved successfully!")
        except Exception as e:
            messages.error(request, f"Error training model: {str(e)}")

    # Fetch all trained models from the database
    trained_models = TrainedModel.objects.all().order_by('-accuracy')

    context = {
        'trained_models': trained_models
    }

    return render(request, 'Train.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            messages.success(request, f"User {username} created!")
            return redirect('signin')
    else:
        return render(request, 'signup.html')

def signout(request):
    logout(request)
    return redirect('/')
