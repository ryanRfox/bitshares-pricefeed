import os
from dataetime import datetime
import pydocumentdb.documents as documents
import pydocumentdb.document_client as document_client
import pydocumentdb.errors as errors

def update_cosmos(prices):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    exportDoc = { "_timestamp": str(timestamp) }
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
