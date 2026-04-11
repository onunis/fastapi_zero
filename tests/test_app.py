from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app, appweb


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A:  Act - Executa a coisa (o SUT)
    - A: Assert - Garanta que A eh A
    """

    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.json() == {'message': 'Ola Mundo!'}  # Assert
    assert response.status_code == HTTPStatus.OK


def test_rootweb_deve_retornar_ola_mundo():

    client = TestClient(appweb)

    response = client.get('/')

    assert (
        response.text
        == """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>
    """
    )
    assert response.status_code == HTTPStatus.OK
