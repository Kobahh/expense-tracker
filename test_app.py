from app import app

def test_login_page_loads():
    client = app.test_client()
    response = client.get('/login')
    assert response.status_code == 200

def test_delete_rejects_get():
    client = app.test_client()
    response = client.get('/delete-expense/5')
    assert response.status_code == 405

def test_homepage_redirects_when_logged_out():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')
