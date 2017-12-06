#!/usr/bin/env python3

import sys
import click
import os
import logging
from pprint import pprint
from bitshares.storage import configStorage as config
from bitshares.price import Price
from bitshares.account import Account
# from bitshares.asset import Asset
from .pricefeed import Feed
from uptick.decorators import (
    # verbose,
    chain,
    unlock,
)
from .ui import (
    configfile,
    print_prices,
    confirmwarning,
    confirmalert,
    alert,
)
import pydocumentdb.documents as documents
import pydocumentdb.document_client as document_client
import pydocumentdb.errors as errors

log = logging.getLogger(__name__)


@click.group()
@click.option(
    "--configfile",
    default="config.yml",
    # type=click.File('r'),
)
@click.option(
    "--confirm-warning/--no-confirm-warning",
    help="Need for manual confirmation of warnings",
    default=True,
)
@click.option(
    "--skip-critical/--no-skip-critical",
    help="Skip critical feeds",
    default=False,
)
@click.pass_context
def main(ctx, **kwargs):
    ctx.obj = {}
    for k, v in kwargs.items():
        ctx.obj[k] = v


@main.command()
@click.pass_context
@chain
@click.argument(
    "key",
    nargs=-1
)
@unlock
def addkey(ctx, key):
    """ Add a private key to the wallet
    """
    if not key:
        while True:
            key = click.prompt(
                "Private Key (wif) [Enter to quit]",
                hide_input=True,
                show_default=False,
                default="exit"
            )
            if not key or key == "exit":
                break
            try:
                ctx.bitshares.wallet.addPrivateKey(key)
            except Exception as e:
                click.echo(str(e))
                continue
    else:
        for k in key:
            try:
                ctx.bitshares.wallet.addPrivateKey(k)
            except Exception as e:
                click.echo(str(e))

    installedKeys = ctx.bitshares.wallet.getPublicKeys()
    if len(installedKeys) == 1:
        name = ctx.bitshares.wallet.getAccountFromPublicKey(installedKeys[0])
        if name:  # only if a name to the key was found
            account = Account(name, bitshares_instance=ctx.bitshares)
            click.echo("=" * 30)
            click.echo("Setting new default user: %s" % account["name"])
            click.echo()
            click.echo("You can change these settings with:")
            click.echo("    uptick set default_account <account>")
            click.echo("=" * 30)
            config["default_account"] = account["name"]


@main.command()
@click.argument(
    "example",
    default="default"
)
@click.pass_context
def create(ctx, example):
    """ Create config file
    """
    import shutil
    this_dir, this_filename = os.path.split(__file__)
    default_config_file = os.path.join(this_dir, "examples", example + ".yaml")
    config_file = ctx.obj["configfile"]
    shutil.copyfile(
        default_config_file,
        config_file
    )
    click.echo("Config file created: %s" % config_file)


@main.command()
@click.argument(
    "assets",
    nargs=-1,
    required=False,
)
@click.pass_context
@configfile
@chain
@unlock
def update(ctx, assets):
    """ Update price feed for assets
    """
    exitcode = 0

    # Do i have a producer?
    assert "producer" in ctx.config and ctx.config["producer"], \
        "Please provide a feed producer name in the configuration!"

    feed = Feed(config=ctx.config)
    feed.fetch()
    feed.derive(assets)
    prices = feed.get_prices()

    exportDoc = {}
    for asset in prices:
        exportDoc[asset] = {
            "price": prices[asset]["price"],
            "cer": prices[asset]["cer"],
            "mean": prices[asset]["mean"],
            "median": prices[asset]["median"],
            "weighted": prices[asset]["weighted"],
            "std": prices[asset]["std"],
            "number": prices[asset]["number"],
            "mssr": prices[asset]["mssr"],
            "mcr": prices[asset]["mcr"],
            "short_backing_symbol": prices[asset]["short_backing_symbol"]
            }
    print(exportDoc)

    # Get the DocumentDB settings from the environment variables
    ENDPOINT              = os.environ['ENDPOINT']
    MASTERKEY             = os.environ['MASTERKEY']
    DOCUMENTDB_DATABASE   = os.environ['DOCUMENTDB_DATABASE']
    DOCUMENTDB_COLLECTION = os.environ['DOCUMENTDB_COLLECTION']

    # Initialize the CosmosDB client
    client = document_client.DocumentClient(ENDPOINT, {'masterKey': MASTERKEY})

    # Store the pricing data in CosmosDB
    collectionUrl = "dbs/" + DOCUMENTDB_DATABASE + "/colls/" + DOCUMENTDB_COLLECTION
    document1 = client.CreateDocument(collectionUrl, exportDoc)

    print_prices(prices)

    sys.exit(exitcode)


if __name__ == '__main__':
    main()
