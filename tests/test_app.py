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
