from myblog.models import User


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Create your own blog" in response.data
    assert b"Let's get started" in response.data
    assert b"Login" in response.data


def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Email' in response.data
    assert b'Forgot your' in response.data
    assert b'Username' not in response.data


def test_register_page(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'Already have an account?' in response.data
    assert b'Register Now!' in response.data
    assert b'Confirm Password' in response.data


def test_blog_history_page(test_client,init_db,auth):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    response = test_client.get(f'/blog_history/{user.username}')

    assert response.status_code == 200
    assert b'test' in response.data
    assert b'History' in response.data


def test_forgot_password_page(test_client):
    response = test_client.get('/forgot_password')

    assert response.status_code == 200
    assert b'Find Your Password' in response.data
    assert b'Please Enter your email' in response.data


def test_reset_password_page(test_client,init_db):
    user = User.query.filter_by(username='tom').first()
    token = user.get_reset_token()
    response = test_client.get(f'/reset_password/{token}')

    assert response.status_code == 200
    assert b'Reset your password' in response.data
    assert b'Confirm Password' in response.data
    assert b'Password' in response.data
