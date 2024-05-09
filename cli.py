import click
from aiohttp import web
from server import app

@click.command()
@click.option('--port', default=8080, help='Port to run the server on')
def runserver(port):
    web.run_app(app, port=port)

if __name__ == '__main__':
    runserver()
