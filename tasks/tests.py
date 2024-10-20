from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from tasks.models import Task 


class CustomPaginationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='password123'
        )
        self.token = self.get_token_for_user(self.user)
        
        
        # Create a task for testing detail view
        self.task = Task.objects.create(
            title='Test Task',
            description='A task for testing.',
            due_date='2024-12-31',  # Adjust this to be a future date
            priority='Medium',  # Ensure this matches your priority choices
            status='Pending',  # Ensure this matches your status choices
            owner=self.user  # Set the task owner to the test user
        )
               
    
def get_token_for_user(user):
       refresh = RefreshToken.for_user(user)
       refresh['username'] = user.username  # Add username to the token payload
       return str(refresh.access_token)    

def test_pagination(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('task-list'))
        
        print("Response Status Code:", response.status_code)  # Debugging
        print("Response Data:", response.data)  # Check for any error messages or permissions issues
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expecting 403
        


def test_expired_token(self):
        # Generate an expired token
        valid_token = self.get_token_for_user(self.user)
        payload = jwt.decode(valid_token, settings.SECRET_KEY, algorithms=['HS256'])
        payload['exp'] = 0  # Set expiration to the past (simulating an expired token)
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expecting 403


def test_task_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task.id}))

        print("Task Detail Response Status Code:", response.status_code)  # Debugging
        print("Task Detail Response Data:", response.data)  # Check the task detail response

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task.id)  # Check the correct task is returned
        self.assertEqual(response.data['title'], self.task.title)  # Check task title
        self.assertEqual(response.data['description'], self.task.description)  # Check task description

def test_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        task_data = {
            'title': 'New Task',
            'description': 'A new task for testing creation.',
            'due_date': '2024-12-31',  # Future date
            'priority': 'Low',
            'status': 'Pending',
        }
        response = self.client.post(reverse('task-list'), task_data)

        print("Create Task Response Status Code:", response.status_code)  # Debugging
        print("Create Task Response Data:", response.data)  # Check the response data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)  # Ensure task count has increased
        self.assertEqual(Task.objects.get(id=response.data['id']).title, task_data['title'])  # Check the task was created correctly

def test_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        update_data = {
            'title': 'Updated Task',
            'description': 'Updated description for the task.',
            'due_date': '2024-12-31',
            'priority': 'High',
            'status': 'Completed',
        }
        response = self.client.put(reverse('task-detail', kwargs={'pk': self.task.id}), update_data)

        print("Update Task Response Status Code:", response.status_code)  # Debugging
        print("Update Task Response Data:", response.data)  # Check the response data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()  # Refresh the task instance from the database
        self.assertEqual(self.task.title, update_data['title'])  # Check the task was updated
        self.assertEqual(self.task.description, update_data['description'])

def test_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(reverse('task-detail', kwargs={'pk': self.task.id}))

        print("Delete Task Response Status Code:", response.status_code)  # Debugging
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Expecting 204

        # Check that the task is deleted
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)  # Task should no longer exist