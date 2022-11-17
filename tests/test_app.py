"""test app"""

import pytest


@pytest.mark.asyncio
async def test_get_all_users(client, init_user):
    """test get all users"""
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_create_user(client, init_user):
    """test create user"""
    user = {
        'name': 'doo',
        'age': 12
    }
    client.post('/users', json=user)
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json()) == 4
