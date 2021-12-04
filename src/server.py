from flask import Flask, jsonify, request
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
    required_fields = ['sender', 'receiver', 'amount']
    provided_fields = request.get_json()

    # handle some types of bad requests
    if not all(field in provided_fields for field in required_fields):
        return 'Required data missing', 400
    if not provided_fields['sender'] or type(provided_fields['sender']) != str:
        return 'Invalid sender address', 400
    if not provided_fields['receiver'] or type(provided_fields['receiver']) != str:
        return 'Invalid receiver address', 400
    if not provided_fields['amount'] or type(provided_fields['amount']) != int:
        return 'Invalid amount', 400

    # add the transaction to the pending block
    block_indx = blockchain.registerTransaction(
        provided_fields['sender'],
        provided_fields['receiver'],
        provided_fields['amount']
    )
    response = {'message': f'Transaction added to pending block: {block_indx}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def chain():
    '''
    - Returns the full blockchain of this node
    '''
    pass



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
