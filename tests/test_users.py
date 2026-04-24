from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'cecilia',
            'email': 'cecilia@example.com',
            'password': 'secret',
        },
    )

    # Voltou o status code correto ?
    assert response.status_code == HTTPStatus.CREATED

    # Validar UserPublic
    assert response.json() == {
        'id': 1,
        'username': 'cecilia',
        'email': 'cecilia@example.com',
    }


def test_read_users(client, user, token):

    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Teste',
            'email': 'test@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'Teste',
        'email': 'test@test.com',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_integrity_error(client, user, token):
    # Inserindo fausto
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user das fixture para fausto
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_create_username_integrity_error(client, user):

    response = client.post(
        '/users',
        json={
            'username': 'Teste',
            'email': 'cecilia@example.com',
            'password': 'testeteste',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_email_integrity_error(client, user):

    response = client.post(
        '/users',
        json={
            'username': 'cecilia',
            'email': 'teste@test.com',
            'password': 'testeteste',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_get_user_id(client, user):

    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'Teste',
        'email': 'teste@test.com',
    }


def test_get_user_id_integrity_error(client, user):

    response = client.get('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
