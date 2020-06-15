def test_error_404(test_client,init_db):
    response = test_client.get('/project/tom/3')

    assert response.status_code == 404
    assert b'That page does not exit. Please go back' in response.data
    assert b'Oops! Page not found' in response.data


def test_error_403(test_client,init_db,auth):
    auth.login()
    username = 'testuser1'
    response = test_client.get(f'/project/{username}/2/update')

    assert response.status_code == 403
    assert b'You do not have permission to access this page' in response.data
    assert b'Please check your account information' in response.data


