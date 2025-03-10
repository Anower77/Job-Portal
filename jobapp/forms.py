from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.core.validators import RegexValidator, URLValidator
from django.utils import timezone

from jobapp.models import *
from django_ckeditor_5.widgets import CKEditor5Widget


    

class JobForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditor5Widget(
            attrs={'class': 'django-ckeditor-5'},
            config_name='default'
        )
    )
    
    company_description = forms.CharField(
        widget=CKEditor5Widget(
            attrs={'class': 'django-ckeditor-5'},
            config_name='default'
        ),
        required=False
    )
    
    job_type = forms.ChoiceField(
        choices=JOB_TYPE,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select Job Type'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select Category'
        })
    )

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Job Title"
        self.fields['location'].label = "Job Location"
        self.fields['salary'].label = "Salary"
        self.fields['description'].label = "Job Description"
        self.fields['last_date'].label = "Application Deadline"
        self.fields['company_name'].label = "Company Name"
        self.fields['url'].label = "Company Website"

        # Add form-control class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Job
        exclude = ['user', 'created_at', 'updated_at', 'is_closed', 'is_published', 'timestamp']
        labels = {
            'last_date': 'Application Deadline',
            'company_name': 'Company Name',
            'company_description': 'Company Description',
            'title': 'Job Title',
            'description': 'Job Description',
            'salary': 'Salary Range',
        }

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category


    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            
            job.save()
        return job




class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job']

class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkJob
        fields = ['job']




class JobEditForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add field validations
        self.fields['salary'].validators.append(
            RegexValidator(
                r'^\$?\d+(?:,\d{3})*(?:\s*-\s*\$?\d+(?:,\d{3})*)?$',
                'Enter a valid salary range (e.g. $800 - $1200)'
            )
        )
        self.fields['url'].validators.append(URLValidator())
        
        # Add required fields
        self.fields['title'].required = True
        self.fields['location'].required = True
        self.fields['job_type'].required = True
        self.fields['category'].required = True
        
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        # self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Dead Line :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"


        self.fields['title'].widget.attrs.update({'placeholder': 'eg : Software Developer', 'class': 'form-control'})        
        self.fields['location'].widget.attrs.update({'placeholder': 'eg : Bangladesh', 'class': 'form-control'})
        self.fields['salary'].widget.attrs.update({'placeholder': '$800 - $1200', 'class': 'form-control'})
        self.fields['last_date'].widget.attrs.update({'placeholder': 'YYYY-MM-DD ', 'class': 'form-control'})        
        self.fields['company_name'].widget.attrs.update({'placeholder': 'Company Name', 'class': 'form-control'})           
        self.fields['url'].widget.attrs.update({'placeholder': 'https://example.com', 'class': 'form-control'})    

    
        # last_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Service Name','class' : 'datetimepicker1'}))

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Job Type is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("Category is required")
        return category

    def clean(self):
        cleaned_data = super().clean()
        last_date = cleaned_data.get('last_date')
        
        if last_date and last_date < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past")
            
        return cleaned_data

    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)      
        if commit:
            job.save()
        return job

