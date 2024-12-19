# Androidapp/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import AndroidApp, UserAppTask
from .serializers import AndroidAppSerializer, UserAppTaskSerializer, UserSerializer,UserAppTaskCreateSerializer
from .permissions import IsAdminOrReadOnly
from Androidapp.permissions import IsAdminOrReadOnly
from api.models import CustomUser
from django.db.models import Exists, OuterRef

class AndroidAppListView(generics.ListAPIView):
    queryset = AndroidApp.objects.filter(is_active=True)
    serializer_class = AndroidAppSerializer
    permission_classes = [permissions.AllowAny]

class AndroidAppDetailView(generics.RetrieveAPIView):
    queryset = AndroidApp.objects.filter(is_active=True)
    serializer_class = AndroidAppSerializer
    permission_classes = [permissions.AllowAny]

class AndroidAppCreateView(generics.CreateAPIView):
    queryset = AndroidApp.objects.all()
    serializer_class = AndroidAppSerializer
    permission_classes = [permissions.IsAdminUser]

class AndroidAppUpdateView(generics.UpdateAPIView):
    queryset = AndroidApp.objects.all()
    serializer_class = AndroidAppSerializer
    permission_classes = [permissions.IsAdminUser]

class AndroidAppDeleteView(generics.DestroyAPIView):
    queryset = AndroidApp.objects.all()
    serializer_class = AndroidAppSerializer
    permission_classes = [permissions.IsAdminUser]



class AvailableAppsView(generics.ListAPIView):
    """
    API view to retrieve all active apps that the current user hasn't created tasks for yet.
    """
    serializer_class = AndroidAppSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Create a subquery to check for existing user tasks
        user_tasks = UserAppTask.objects.filter(
            user=self.request.user,
            app=OuterRef('pk')
        )

        # Get all active apps that don't have a corresponding task for the current user
        return AndroidApp.objects.filter(
            is_active=True
        ).annotate(
            has_task=Exists(user_tasks)
        ).filter(
            has_task=False
        )
class SubmitAppTaskView(generics.CreateAPIView):
    """
    API view to submit a new app task with screenshot
    """
    serializer_class = UserAppTaskCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            status='SUBMITTED'
        )

class ScreenshotApprovalListView(generics.ListAPIView):
    """
    API view to list all submitted tasks for admin review
    """
    serializer_class = UserAppTaskSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return UserAppTask.objects.filter(status='SUBMITTED').select_related('user', 'app')

class ScreenshotApprovalUpdateView(generics.UpdateAPIView):
    """
    API view to approve or reject submitted tasks
    """
    queryset = UserAppTask.objects.all()
    serializer_class = UserAppTaskSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['APPROVED', 'REJECTED']:
            return Response(
                {'error': 'Invalid status. Must be APPROVED or REJECTED'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        task.status = new_status
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)
class AcceptedUserAppsView(generics.ListAPIView):
    """
    API view to retrieve all apps with APPROVED status for the current authenticated user.
    """
    serializer_class = UserAppTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAppTask.objects.filter(
            user=self.request.user,
            status='APPROVED'
        ).select_related('user', 'app')