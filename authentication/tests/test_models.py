from rest_framework.test import APITestCase
from authentication.models import User
from django.test import TestCase 

class TestModel(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user(email='mkhizenokuphila45@gmail.com', password='password1106!@')
        self.assertEqual(user.email, 'mkhizenokuphila45@gmail.com')
        self.assertTrue(user.check_password('password1106!@'))
        
        
        
    def test_creates_super_user(self):
        user = User.objects.create_superuser(email='mkhizenokuphila45@gmail.com', password='password1106!@')
        self.assertIsInstance(user,User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'mkhizenokuphila45@gmail.com')
        self.assertTrue(user.check_password('password1106!@'))
        
class TestModel(TestCase):
    def test_raises_error_with_message_when_no_email_is_supplied(self):
        self.assertRaisesMessage(ValueError,'The given username must be set')
        with self.assertRaises(ValueError):
         User.objects.create_user(username='' , email='', password='password1106!@')
        
            
def test_raises_error_when_no_email_is_supplied(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='password1106!@')
            
def test_create_super_user_with_is_staff_status(self):
    with self.assertRaises(ValueError,'Superuser must have is_staff=True.'):
        User.objects.create_superuser(username='username,email', password='password1106!@', is_staff=False)      
        
def test_create_super_user_with_super_user_status(self):
    with self.assertRaises(ValueError,'Superuser must have is_superuser=True.'):
        User.objects.create_superuser(username='username,email', password='password1106!@', is_superuser=False)      
        
def test_creates_super_user(self):
        user = User.objects.create_superuser(
            email='mkhizenokuphila45@gmail.com',  # Corrected email
            password='password1106!@'
        )
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email, 'mkhizenokuphila45@gmail.com') 
    
    
        