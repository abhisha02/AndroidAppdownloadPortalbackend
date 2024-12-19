# Androidapp/urls.py
from django.urls import path
from . import views
from .views import AvailableAppsView,SubmitAppTaskView,ScreenshotApprovalListView,ScreenshotApprovalUpdateView,AcceptedUserAppsView



urlpatterns = [
    path('', views.AndroidAppListView.as_view(), name='app-list'),
    path('<int:pk>/', views.AndroidAppDetailView.as_view(), name='app-detail'),
    path('upload/', views.AndroidAppCreateView.as_view(), name='app-upload'),
    path('<int:pk>/update/', views.AndroidAppUpdateView.as_view(), name='app-update'),
    path('<int:pk>/delete/', views.AndroidAppDeleteView.as_view(), name='app-delete'),
    path('tasks/submitted/', ScreenshotApprovalListView.as_view(), name='screenshot-approval-list'),
    path('tasks/<int:pk>/update-status/', ScreenshotApprovalUpdateView.as_view(), name='screenshot-approval-update'),
    path('available/', AvailableAppsView.as_view(), name='available-apps'),
    path('tasks/submit/', SubmitAppTaskView.as_view(), name='submit-task'),
    path('user/apps/accepted/', AcceptedUserAppsView.as_view(), name='accepted-apps')
   
]