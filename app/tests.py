from unittest import TestCase
from flask import url_for
from .app import init_app
from .base import db
from .models import User


class AppTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = init_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.client = cls.app.test_client()
        cls.context = cls.app.test_request_context()
        cls.context.push()
        cls.username = 'SomeName'
        cls.user = User(username=cls.username)
        cls.user.set_password('1')
        cls.objects_to_delete = [cls.user]
        db.session.add(cls.user)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.context.pop()
        for obj in cls.objects_to_delete:
            db.session.delete(obj)
        db.session.commit()

    def login(self, username, password):
        return self.client.post(url_for('login'),
                                data={'username': username, 'password': password, 'submit': 'Login'},
                                follow_redirects=False)

    def registration(self, username, password, repeat_password):
        return self.client.post(url_for('registration'),
                                data={'username': username, 'password': password, 'repeat_password': repeat_password,
                                      'submit': 'Registration'},
                                follow_redirects=False)

    def test_success_index_method_get(self):
        response = self.client.get(url_for('index'))
        assert response.status_code == 200

    def test_success_login_method_get(self):
        response = self.client.get(url_for('login'))
        assert response.status_code == 200

    def test_success_registration_method_get(self):
        response = self.client.get(url_for('registration'))
        assert response.status_code == 200

    def test_index_auth_redirect(self):
        response = self.login(self.username, '1')
        assert response.status_code == 302
        assert response.location == url_for('tasks.index', _external=True)

        response = self.client.get(url_for('index'), follow_redirects=False)
        assert response.status_code == 302
        assert response.location == url_for('tasks.index', _external=True)

        response = self.client.get(url_for('tasks.logout'))
        assert response.status_code == 302

    def test_fail_login(self):
        response = self.login(self.username, '2')
        assert response.status_code == 200
        assert response.location is None

    def test_success_login(self):
        response = self.login(self.username, '1')
        assert response.status_code == 302
        assert response.location == url_for('tasks.index', _external=True)

        response = self.client.get(url_for('tasks.logout'))
        assert response.status_code == 302

    def test_login_auth_redirect(self):
        response = self.login(self.username, '1')
        assert response.status_code == 302
        assert response.location == url_for('tasks.index', _external=True)

        response = self.client.get(url_for('login'), follow_redirects=False)
        assert response.status_code == 302
        assert response.location == url_for('tasks.index', _external=True)

        response = self.client.get(url_for('tasks.logout'))
        assert response.status_code == 302

    def test_fail_registration_uqinue_username(self):
        response = self.registration(self.username, '1', '1')
        assert response.status_code == 200
        assert response.location is None

    def test_fail_registration_passwords_not_equals(self):
        response = self.registration('SomeName1', '1', '2')
        assert response.status_code == 200
        assert response.location is None

    def test_success_registration(self):
        username = 'SomeName1'
        response = self.registration(username, '1', '1')
        assert response.status_code == 302
        assert response.location == url_for('login', _external=True)

        user = User.query.filter(User.username == username).first()
        self.objects_to_delete.append(user)

    def test_registration_auth_redirect(self):
        response = self.login(self.username, '1')
        assert response.status_code == 302
        assert response.location == url_for('tasks.index', _external=True)

        response = self.client.get(url_for('registration'), follow_redirects=False)
        assert response.status_code == 302
        assert response.location == url_for('tasks.index', _external=True)

        response = self.client.get(url_for('tasks.logout'))
        assert response.status_code == 302
