def test__login__success_case(client):
    response = client.get('/users/login')

    assert '<h1><b>Авторизация</b></h1>' in response.data.decode()
    assert '<form action="/users/process-login" method="POST">' in response.data.decode()
