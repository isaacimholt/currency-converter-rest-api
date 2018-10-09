import json
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


# list of test cases that should pass
test_cases = [
    # ({request},
    #  {expected response})
    ({
         # reflection
         'reference_date': '2018-09-10',
         'amount':         1.2,
         'src_currency':   'EUR',
         'dest_currency':  'EUR'
     },
     {
         'amount':   1.2,
         'currency': 'EUR'
     }),

    ({
         # conversion
         'reference_date': '2018-09-04',
         'amount':         1.5,
         'src_currency':   'SGD',
         'dest_currency':  'ISK'
     },
     {
         'amount':   118.8800201118723,
         'currency': 'ISK'
     }),
]


@pytest.mark.parametrize("test_data, expected_data", test_cases)
def test_rate_converter(test_data, expected_data, client):
    """Test predefined currency conversions."""

    rv = client.get('/convert', data=test_data)
    assert json.loads(rv.data) == expected_data
