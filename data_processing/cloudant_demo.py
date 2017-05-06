from cloudant import cloudant
from cloudant.adapters import Replay429Adapter
from cloudant.document import Document

USERNAME = "7b4c3699-de51-474f-8737-ead54fdce0d1-bluemix"
PASSWORD = "82baf9e127752d4f0f46ec9bf378dd330557948261a928fc7dea2ed402b21692"
# URL = "https://7b4c3699-de51-474f-8737-ead54fdce0d1-bluemix:82baf9e127752d4f0f46ec9bf3" \
#       "78dd330557948261a928fc7dea2ed402b21692@7b4c3699-de51-474f-8737-ead54fdce0d1-bluemix.cloudant.com"
ACCOUNT_NAME = "7b4c3699-de51-474f-8737-ead54fdce0d1-bluemix"
# Use CouchDB to create a CouchDB client
# from cloudant.client import CouchDB
# client = CouchDB(USERNAME, PASSWORD, url='http://127.0.0.1:5984')

# Use Cloudant to create a Cloudant client using account
from cloudant.client import Cloudant
# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME, connect=True)
# or using url
# client = Cloudant(USERNAME, PASSWORD, url='https://acct.cloudant.com')

# or with a 429 replay adapter that includes configured retries and initial backoff
# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME,
#                   adapter=Replay429Adapter(retries=10, initialBackoff=0.01))

# or with a connect and read timeout of 5 minutes
# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME,
#                   timeout=300)

# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME, connect=True,
#                   adapter=Replay429Adapter(retries=10, initialBackoff=0.01),
#                   timeout=300)

# Perform client tasks...
# session = client.session()
# print('Username: {0}'.format(session['userCtx']['name']))
# print('Databases: {0}'.format(client.all_dbs()))

# Disconnect from the server
# client.disconnect()


# Perform a connect upon entry and a disconnect upon exit of the block
with cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME) as client:

# CouchDB variant
# with couchdb(USERNAME, PASSWORD, url=COUCHDB_URL) as client:

    # Perform client tasks...
    session = client.session()
    print('Username: {0}'.format(session['userCtx']['name']))
    print('Databases: {0}'.format(client.all_dbs()))

    # Create a database
    my_database = client.create_database('my_database')
    if my_database.exists():
        print('SUCCESS!!')

    # You can open an existing database
    del my_database
    my_database = client['my_database']

    # Performs a fetch upon entry and a save upon exit of this block
    # Use this context manager to create or update a Document
    with Document(my_database, 'julia30') as doc:
        doc['name'] = 'Julia'
        doc['age'] = 30
        doc['pets'] = ['cat', 'dog', 'frog']

    # Display a Document
    print(my_database['julia30'])

    # Delete the database
    client.delete_database('my_database')

    print('Databases: {0}'.format(client.all_dbs()))
