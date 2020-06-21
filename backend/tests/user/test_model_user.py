from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_succeed(self):
        """Test creating user using email address is succeed"""
        email = 'admin@admin.com'
        password = 'admin'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_lower_email(self):
        """Test new user email is converted to lowercase string"""
        email = 'admin@ADMIN.COM'
        user = get_user_model().objects.create_user(email, 'admin')
        self.assertEqual(user.email, email.lower())

    def test_new_user_no_email(self):
        """Test new user with no email should fail"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'admin')

    def test_create_new_superuser(self):
        """Test create new superuser"""
        user = get_user_model().objects.create_superuser(
            'admin@admin.com',
            'admin'
        )

        self.assertTrue(user.is_superuser)
