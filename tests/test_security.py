from http import HTTPStatus

from jwt import decode

from fastapi_zero.security import create_access_token


def test_jwt(settings):

    data = {'test': 'test'}

    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/{user.id}', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_no_sub(client):
    # Cria um token sem o campo 'sub'
    token = create_access_token(data={})

    # Faz uma requisição usando esse token
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    # Verifica que retornou 401
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_no_email(client):

    token = create_access_token(data={'sub': 'emailquenaoexiste@test.com'})

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
