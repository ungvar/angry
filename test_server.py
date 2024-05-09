import pytest
from aiohttp import web
from server import healthcheck, calculate_hash

@pytest.fixture
async def cli(aiohttp_client):
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/hash', calculate_hash)
    return await aiohttp_client(app)

async def test_healthcheck(cli):
    resp = await cli.get('/healthcheck')
    assert resp.status == 200
    assert await resp.text() == '{}'

async def test_hash(cli):
    resp = await cli.post('/hash', json={"string": "hello"})
    assert resp.status == 200
    result = await resp.json()
    assert 'hash_string' in result

async def test_hash_without_string(cli):
    resp = await cli.post('/hash', json={})
    assert resp.status == 400
    result = await resp.json()
    assert 'validation_errors' in result

async def test_hash_with_empty_body(cli):
    resp = await cli.post('/hash', data="")
    assert resp.status == 400
    result = await resp.json()
    assert result == {"error": "Invalid JSON data provided"}

async def test_hash_with_invalid_json(cli):
    resp = await cli.post('/hash', data="{not: 'json'}")
    assert resp.status == 400
    result = await resp.json()
    assert result == {"error": "Invalid JSON data provided"}
