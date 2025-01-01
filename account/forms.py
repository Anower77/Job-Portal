from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from account.models import CustomUser

class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Password', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password', 'class': 'form-control'})
    
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "employer"
        user.is_active = False  # Account needs to be activated via email
        if commit:
            user.save()
        return user

class EmployeeRegistrationForm(UserCreationForm):
    gender = forms.ChoiceField(
        choices=CustomUser.GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select Gender'
        })
    )

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Password', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password', 'class': 'form-control'})

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'gender']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid email/password combination.")
            if not self.user.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

    def get_user(self):
        return self.user if hasattr(self, 'user') else None

class EmployeeProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'linkedin_profile', 'personal_website', 'city', 'country',
            'date_of_birth', 'profile_picture', 'nationality',
            'work_eligibility', 'languages', 'github_profile', 'cv_link'
        ]
