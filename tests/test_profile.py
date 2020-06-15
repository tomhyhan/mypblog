from myblog.models import User


def test_profile_page(test_client, auth):
    auth.login()
    response = test_client.post('/profile/')

    assert response.status_code == 200
    assert b'Update your profile' in response.data
    assert b'Upload Profile Picture' in response.data
    assert b'Description' in response.data


def test_update_profile(test_client, auth, init_db):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    response = test_client.post('/profile/', data=dict(username=user.username,
                                                       email='update@update.com',
                                                       description="Testing"),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'update@update.com' in response.data
    assert b'Testing' in response.data
    assert b'Your profile has been updated' in response.data
    assert b'tom' in response.data


def test_static_profile_page(test_client, init_db):
    user = User.query.filter_by(username='tom').first()
    response = test_client.get(f'/profile/{user.username}')

    assert response.status_code == 200
    assert b'tom' in response.data
    assert b'tom@c.com' in response.data

