import json

from unittest import mock

import pytest

from jobsbrowser.api import init_app


@pytest.fixture(scope='session')
def app(request):
    app = init_app(config_name='TESTING', init_extensions=False)
    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(lambda: ctx.pop())
    return app


@pytest.fixture(scope='session')
def test_client(app):
    return app.test_client()


def test_ping_resource_returns_pong(test_client):
    response = test_client.get('/ping')
    assert response.status_code == 200
    assert response.data == b'pong'


@pytest.mark.parametrize('offer_dict', [
    {'offer_id': '1234', 'url': 'http://spam.egg/1234'},
])
def test_add_offer_resource_try_add_offer_to_mongo_db(test_client, offer_dict):
    with mock.patch('jobsbrowser.api.resources.mongo'):
        response = test_client.post(
            '/offers',
            data=json.dumps(offer_dict),
            content_type='application/json',
        )
    assert response.status_code == 200
    assert response.data.strip() == b'{}'


def test_get_offers_resource_query_mongo_db(test_client):
    with mock.patch('jobsbrowser.api.resources.mongo'):
        response = test_client.get('/offers')
    assert response.status_code == 200
    assert json.loads(response.data.strip()) == {'links': []}


def test_update_offer_resource_query_mongo_db(test_client):
    with mock.patch('jobsbrowser.api.resources.mongo'):
        response = test_client.put(
            '/offers',
            data=json.dumps({
                'url': 'foo.bar/',
                'job_title': 'foo bar developer',
            }),
            content_type='application/json',
        )
    assert response.status_code == 200
    assert response.data.strip() == b'{}'
