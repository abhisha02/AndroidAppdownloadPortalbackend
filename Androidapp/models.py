from django.db import models
from api.models import CustomUser
from django.utils import timezone

class AndroidApp(models.Model):
    CATEGORY_CHOICES = [
        ('GAMES', 'Games'),
        ('PRODUCTIVITY', 'Productivity'),
        ('SOCIAL', 'Social Media'),
        ('UTILITY', 'Utility'),
        ('OTHER', 'Other')
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    package_name = models.CharField(max_length=200, unique=True)
    points_value = models.IntegerField(default=10)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    app_icon = models.ImageField(upload_to='android_app_icons/', null=True, blank=True)
    playstore_link = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserAppTask(models.Model):
    TASK_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='app_tasks')
    app = models.ForeignKey(AndroidApp, on_delete=models.CASCADE, related_name='user_tasks')
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='PENDING')
    screenshot = models.ImageField(upload_to='app_task_screenshots/', null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'app')
        verbose_name = 'User App Task'
        verbose_name_plural = 'User App Tasks'

    def save(self, *args, **kwargs):
        # Automatically update points when task is approved
        if self.status == 'APPROVED' and self.points_earned == 0:
            self.points_earned = self.app.points_value
            self.approved_at = timezone.now()
            self.user.total_points += self.points_earned
            self.user.save()
        
        if self.status == 'SUBMITTED' and not self.submitted_at:
            self.submitted_at = timezone.now()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.app.name} Task"
