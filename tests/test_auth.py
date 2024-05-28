import json

def test_register(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' endpoint is hit (POST)
    THEN check if the user is registered successfully
    """
    response = test_client.post('/api/auth/register',
                                data=json.dumps(dict(username='testuser3', email='test3@example.com', password='password')),
                                content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert data['message'] == 'User registered successfully'

def test_register_existing_user(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' endpoint is hit (POST) with an existing user
    THEN check if the user registration fails
    """
    response = test_client.post('/api/auth/register',
                                data=json.dumps(dict(username='testuser', email='test1@example.com', password='password')),
                                content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data['message'] == 'Username already exists'

def test_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' endpoint is hit (POST)
    THEN check if the user is logged in successfully
    """
    response = test_client.post('/api/auth/login',
                                data=json.dumps(dict(email='test1@example.com', password='password')),
                                content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['message'] == 'User logged in successfully'

def test_login_invalid_credentials(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' endpoint is hit (POST) with invalid credentials
    THEN check if the user login fails
    """
    response = test_client.post('/api/auth/login',
                                data=json.dumps(dict(email='wrong@example.com', password='wrongpassword')),
                                content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 401
    assert data['message'] == 'Invalid credentials'

def test_reset_password(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/reset-password' endpoint is hit (POST)
    THEN check if the password is reset successfully
    """
    login_response = test_client.post('/api/auth/login',
                                      data=json.dumps(dict(email='test1@example.com', password='password')),
                                      content_type='application/json')
    login_data = json.loads(login_response.data.decode())
    access_token = login_data['access_token']

    response = test_client.post('/api/auth/reset-password',
                                headers={'Authorization': f'Bearer {access_token}'},
                                data=json.dumps(dict(new_password='newpassword')),
                                content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data['message'] == 'Password updated successfully'

def test_change_password(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/change-password' endpoint is hit (POST)
    THEN check if the password is changed successfully
    """
    login_response = test_client.post('/api/auth/login',
                                      data=json.dumps(dict(email='test1@example.com', password='password')),
                                      content_type='application/json')
    login_data = json.loads(login_response.data.decode())
    access_token = login_data['access_token']

    response = test_client.post('/api/auth/change-password',
                                headers={'Authorization': f'Bearer {access_token}'},
                                data=json.dumps(dict(current_password='password', new_password='newpassword')),
                                content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data['message'] == 'Password updated successfully'

def test_refresh_token(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/refresh' endpoint is hit (POST)
    THEN check if the access token is refreshed successfully
    """
    login_response = test_client.post('/api/auth/login',
                                      data=json.dumps(dict(email='test1@example.com', password='password')),
                                      content_type='application/json')
    login_data = json.loads(login_response.data.decode())
    refresh_token = login_data['refresh_token']

    response = test_client.post('/api/auth/refresh',
                                headers={'Authorization': f'Bearer {refresh_token}'})
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'access_token' in data
    assert data['message'] == 'Token refreshed successfully'
