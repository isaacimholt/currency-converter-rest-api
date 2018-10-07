import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'aud' in rv.data
