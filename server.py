import json
import hashlib
from aiohttp import web

async def healthcheck(request):
    return web.json_response({})

async def calculate_hash(request):
    try:
        data = await request.json()
        input_string = data['string']
        hash_string = hashlib.sha256(input_string.encode()).hexdigest()
        return web.json_response({"hash_string": hash_string})
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON data provided"}, status=400)
    except KeyError:
        return web.json_response({"validation_errors": "Field 'string' is missing"}, status=400)

app = web.Application()
app.add_routes([web.get('/healthcheck', healthcheck),
                web.post('/hash', calculate_hash)])
