from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A:  Act - Executa a coisa (o SUT)
    - A: Assert - Garanta que A eh A
    """

    response = client.get('/')  # Act

    assert response.json() == {'message': 'Ola Mundo!'}  # Assert
    assert response.status_code == HTTPStatus.OK


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


def test_read_users(client):

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'cecilia',
                'email': 'cecilia@example.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'catarina',
            'email': 'catarina@example.com',
            'password': 'segredin123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'catarina',
        'email': 'catarina@example.com',
    }


def test_get_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'catarina',
        'email': 'catarina@example.com',
    }


def test_404_get_user(client):
    response = client.get('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Deu ruim paizao! Nao achei...'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'catarina',
        'email': 'catarina@example.com',
    }


def test_404_update(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'catarina',
            'email': 'catarina@example.com',
            'password': 'segredin123',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Deu ruim paizao! Nao achei...'}


def test_404_delete(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Deu ruim paizao! Nao achei...'}
