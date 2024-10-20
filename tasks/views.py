from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView
from django_filters import rest_framework as django_filters
from .pagination import CustomPagination
from django.shortcuts import render

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES, required=False)
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_LEVELS, required=False)
    due_date = django_filters.DateFilter(field_name='due_date', lookup_expr='exact', required=False)

    class Meta:
        model = Task
        fields = ['status', 'priority', 'due_date']

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TaskFilter
    ordering_fields = ['due_date', 'priority']
    ordering = ['due_date']
    pagination_class = CustomPagination

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

# User Profile Update View
class ProfileUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'bio', 'profile_picture']
    template_name = 'profile_update.html'
    success_url = reverse_lazy('task-overview')

    def get_object(self):
        return self.request.user

# User Registration View
class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

# ViewSets for Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Task Overview
@api_view(['GET'])
def taskOverview(request):
    tasks_urls = {
        'List': '/api/tasks/',
        'Detail View': '/api/tasks/<str:pk>/',
        'Create': '/api/tasks/create/',
        'Update': '/api/tasks/update/<str:pk>/',
        'Delete': '/api/tasks/delete/<str:pk>/',
        'Mark Complete': '/api/tasks/<str:pk>/mark-complete/',
        'Mark Incomplete': '/api/tasks/<str:pk>/mark-incomplete/',
    }
    return Response(tasks_urls)

# Task Completion Handlers
def set_task_status(task, status):
    task.status = status
    task.completed_at = timezone.now() if status == 'Completed' else None
    task.save()
    return TaskSerializer(task).data

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_task_complete(request, pk):
    task = get_object_or_404(Task, id=pk, owner=request.user)  # Updated to use 'owner'
    if task.status == 'Completed':
        return Response({'error': 'Task is already marked as complete.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = set_task_status(task, 'Completed')
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_task_incomplete(request, pk):
    task = get_object_or_404(Task, id=pk, owner=request.user)  # Updated to use 'owner'
    if task.status == 'Pending':
        return Response({'error': 'Task is already marked as incomplete.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = set_task_status(task, 'Pending')
    return Response(data, status=status.HTTP_200_OK)

# User Management Views
@api_view(['POST'])
def userCreate(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def userUpdate(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.user != user:
        return Response({'error': 'You are not allowed to update this user.'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def userDelete(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.user != user:
        return Response({'error': 'You are not allowed to delete this user.'}, status=status.HTTP_403_FORBIDDEN)
    
    user.delete()
    return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Custom 404 View
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
