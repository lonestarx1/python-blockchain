from flask import Flask
import uuid
from blockchain import Blockchain


# Creating a node on the network, with a uniuqe id
app = Flask(__name__)
node_id = str(uuid.uuid4()).replace('-', '')


# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    '''
    - Handles a request to mine a new block, (by running POW algorithm)
    '''
    pass


@app.route('/transactions/new/', methods=['POST'])
def newTransaction():
    '''
    - Handles a request to register a new transaction in the pending block
    '''
    pass


@app.route('/chain', methods=['GET'])
def chain():
    '''
    - Returns the full blockchain of this node
    '''
    pass



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)