from rest_framework import serializers
from account.models import CustomUser
from jobapp.models import Job, Applicant
from taggit.serializers import (TagListSerializerField,TaggitSerializer)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role')
        read_only_fields = ('id',)

class JobSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagListSerializerField()
    
    class Meta:
        model = Job
        fields = (
            'id', 
            'title',
            'description',
            'tags',
            'location',
            'job_type',
            'category',
            'salary',
            'company_name',
            'company_description',
            'url',
            'last_date',
            'is_published',
            'is_closed',
            'timestamp',
            'user'
        )
        read_only_fields = ('id', 'timestamp', 'user')

class ApplicantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = Applicant
        fields = (
            'id',
            'user',
            'job',
            'timestamp',
            'status'
        )
        read_only_fields = ('id', 'timestamp') 