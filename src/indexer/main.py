"""Apibara indexer entrypoint."""

import asyncio
from functools import wraps

import click

from indexer.indexer import run_indexer
from indexer.graphql import run_graphql_api


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.option("--server-url", default=None, help="Apibara stream url.")
@click.option("--mongo-url", default=None, help="MongoDB url.")
@click.option("--restart", is_flag=True, help="Restart indexing from the beginning.")
@async_command
async def start(server_url, mongo_url, restart):
    """Start the Apibara indexer."""
    if server_url is None:
        server_url = "goerli.starknet.a5a.ch:443"
    if mongo_url is None:
        mongo_url = "mongodb://apibara:apibara@localhost:27017"

    await run_indexer(
        restart=restart,
        server_url=server_url,
        mongo_url=mongo_url,
    )


@cli.command()
@click.option("--mongo-url", default=None, help="MongoDB url.")
@async_command
async def graphql(mongo_url):
    """Start the GraphQL server."""
    if mongo_url is None:
        mongo_url = "mongodb://apibara:apibara@localhost:27017"

    await run_graphql_api(
        mongo_url=mongo_url,
    )
