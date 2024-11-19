from django import forms

class Parameters(forms.Form):
    SEX_CHOICES = [
        (0, 'Male'),
        (1, 'Female'),
    ]

    CP_CHOICES = [
        (0, 'Typical Angina'),
        (1, 'Atypical Angina'),
        (2, 'Non-Anginal Pain'),
        (3, 'Asymptomatic')
    ]

    FBS_CHOICES = [
        (0, 'Less than 120 mg/dl'),
        (1, 'More than 120 mg/dl')
    ]

    RESTCG_CHOICES = [
        (0, 'Normal'),
        (1, 'Having ST-T wave abnormality'),
        (2, 'Left ventricular hypertrophy')
    ]

    EXANG_CHOICES = [
        (0, 'No'),
        (1, 'Yes')
    ]

    SLOPE_CHOICES = [
        (0, 'Upsloping'),
        (1, 'Flat'),
        (2, 'Downsloping')
    ]

    THAL_CHOICES = [
        (3, 'Normal'),
        (6, 'Fixed Defect'),
        (7, 'Reversible Defect')
    ]

    age = forms.IntegerField(
        max_value=120,
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'a1',
            'type': 'number',
            'class': 'validate',
            'min': '1',
            'max': '120',
            'required': 'required'
        }),
        error_messages={'invalid': 'Please enter a valid age between 1 and 120.'}
    )

    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        required=True,
        widget=forms.Select(attrs={'id': 'a2', 'class': 'validate', 'required': 'required'})
    )

    cp = forms.ChoiceField(
        choices=CP_CHOICES,
        required=True,
        widget=forms.Select(attrs={'id': 'a3', 'class': 'validate', 'required': 'required'})
    )

    trestbps = forms.IntegerField(
        max_value=200,
        min_value=80,
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'a4',
            'type': 'number',
            'class': 'validate',
            'min': '80',
            'max': '200',
            'required': 'required'
        }),
        error_messages={'invalid': 'Please enter a valid resting blood pressure between 80 and 200.'}
    )

    chol = forms.IntegerField(
        max_value=600,
        min_value=100,
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'a5',
            'type': 'number',
            'class': 'validate',
            'min': '100',
            'max': '600',
            'required': 'required'
        }),
        error_messages={'invalid': 'Please enter a valid cholesterol level between 100 and 600.'}
    )

    fbs = forms.ChoiceField(
        choices=FBS_CHOICES,
        required=True,
        widget=forms.Select(attrs={'id': 'a6', 'class': 'validate', 'required': 'required'})
    )

    restcg = forms.ChoiceField(
        choices=RESTCG_CHOICES,
        required=True,
        widget=forms.Select(attrs={'id': 'a7', 'class': 'validate', 'required': 'required'})
    )

    thalach = forms.IntegerField(
        max_value=220,
        min_value=60,
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'a8',
            'type': 'number',
            'class': 'validate',
            'min': '60',
            'max': '220',
            'required': 'required'
        }),
        error_messages={'invalid': 'Please enter a valid heart rate between 60 and 220.'}
    )

    exang = forms.ChoiceField(
        choices=EXANG_CHOICES,
        required=True,
        widget=forms.Select(attrs={'id': 'a9', 'class': 'validate', 'required': 'required'})
    )

    oldpeak = forms.FloatField(
        max_value=6.0,
        min_value=0.0,
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'a10',
            'type': 'number',
            'class': 'validate',
            'step': '0.1',
            'min': '0.0',
            'max': '6.0',
            'required': 'required'
        }),
        error_messages={'invalid': 'Please enter a valid ST depression between 0.0 and 6.0.'}
    )

    slope = forms.ChoiceField(
        choices=SLOPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'id': 'a11', 'class': 'validate', 'required': 'required'})
    )

    ca = forms.IntegerField(
        max_value=3,
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'a12',
            'type': 'number',
            'class': 'validate',
            'min': '0',
            'max': '3',
            'required': 'required'
        }),
        error_messages={'invalid': 'Please enter a valid number of major vessels between 0 and 3.'}
    )

    thal = forms.ChoiceField(
        choices=THAL_CHOICES,
        required=True,
        widget=forms.Select(attrs={'id': 'a13', 'class': 'validate', 'required': 'required'})
    )
