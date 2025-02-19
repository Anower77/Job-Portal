from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.exceptions import PermissionDenied
from .serializers import JobSerializer, ApplicantSerializer, UserSerializer
from jobapp.models import Job, Applicant
from account.models import CustomUser

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Applicant.objects.filter(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own profile unless they're admin
        if not self.request.user.is_staff:
            return CustomUser.objects.filter(id=self.request.user.id)
        return CustomUser.objects.all()
        
    def perform_update(self, serializer):
        # Users can only update their own profile unless they're admin
        if self.request.user.is_staff or serializer.instance.id == self.request.user.id:
            serializer.save()
        else:
            raise PermissionDenied("You don't have permission to update this user")