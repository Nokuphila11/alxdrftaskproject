from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet, RegisterView, ProfileUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LoginView, LogoutView
from .views import TaskViewSet, mark_task_complete, mark_task_incomplete

# Define the router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # Include the router URLs for User and Task ViewSets (this handles standard CRUD operations)
    path('api/', include(router.urls)),

    # Custom task-related URLs using function-based views
    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),  # List and create tasks
    path('tasks/<str:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-detail'),  # Retrieve, update, and delete a specific task
    path('tasks/<str:pk>/mark-complete/', mark_task_complete, name='mark-task-complete'),  # Custom endpoint to mark task as complete
    path('tasks/<str:pk>/mark-incomplete/', mark_task_incomplete, name='mark-task-incomplete'),  # Custom endpoint to mark task as incomplete

    # New endpoints for marking tasks complete/incomplete
    path('tasks/<int:pk>/mark-complete/', views.mark_task_complete, name='mark-task-complete'),
    path('tasks/<int:pk>/mark-incomplete/', views.mark_task_incomplete, name='mark-task-incomplete'),

    # Token authentication URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User authentication URLs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
]

