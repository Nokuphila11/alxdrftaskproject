from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

# Custom User model
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)  # Email field with unique constraint
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Ensure unique related names to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='tasks_user_groups',  # Change related_name to avoid conflict
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='tasks_user_permissions',  # Change related_name to avoid conflict
        blank=True,
    )

    def __str__(self):
        return self.username


# Custom validator function for due date
def validate_due_date(value):
    if value < timezone.now().date():
        raise ValidationError("Due date must be in the future.")


# Task model
class Task(models.Model):
    # Priority levels
    PRIORITY_LOW = 'Low'
    PRIORITY_MEDIUM = 'Medium'
    PRIORITY_HIGH = 'High'
    
    PRIORITY_LEVELS = (
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    )

    # Status choices
    STATUS_PENDING = 'Pending'
    STATUS_COMPLETED = 'Completed'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField(validators=[validate_due_date])  # Use the custom validator
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # Link to custom User model
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    completed_at = models.DateTimeField(null=True, blank=True)  # Field to store completion timestamp

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()}) - {self.get_status_display()} - Assigned to: {self.user.username if self.user else 'Unassigned'}"
