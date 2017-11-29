# -*- coding: utf-8 -*-

"""Console script for ws2812_server."""

import click
import yaml
from .ws2812_server import Ws2812ApiServer

@click.command()
@click.argument('config_file', type=click.File('rb'))

def ws2812server(config_file):
    """Console script for ws2812_server."""
    set = yaml.load(config_file)
    srv = Ws2812ApiServer(settings=set)
    srv.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    ws2812server()


