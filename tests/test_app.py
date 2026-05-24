import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app


class TestIndexPage(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_contains_login_link(self):
        response = self.client.get('/')
        self.assertIn(b'Login', response.data)


class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_register_page_returns_200(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_register_new_user(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_empty_username_rejected(self):
        response = self.client.post('/register', data={
            'username': '',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertIn(b'required', response.data)


class TestLogin(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login_page_returns_200(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_shows_error(self):
        response = self.client.post('/login', data={
            'username': 'nonexistent',
            'password': 'wrongpass'
        }, follow_redirects=True)
        self.assertIn(b'Invalid', response.data)


class TestDashboard(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'log in', response.data)




class TestAddTask(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.client.post('/register', data={
            'username': 'taskuser',
            'password': 'pass123'
        })
        self.client.post('/login', data={
            'username': 'taskuser',
            'password': 'pass123'
        })

    def test_add_task_page_requires_login(self):
        client2 = app.test_client()
        response = client2.get('/task/add', follow_redirects=True)
        self.assertIn(b'log in', response.data)

    def test_add_task_page_loads_when_logged_in(self):
        response = self.client.get('/task/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Task', response.data)

if __name__ == '__main__':
    unittest.main()
