import json
from flask import Flask, jsonify, request
import uuid
from blockchain import Blockchain


# Creating a node on the network, with a uniuqe id
app = Flask(__name__)
node_id = str(uuid.uuid4()).replace('-', '')


# Instantiate the Blockchain
blockchain = Blockchain(mining_difficulty=4)
print("Blockchain initiated")
print("Current Ledger:", blockchain.chain)

@app.route('/mine', methods=['GET'])
def mine():
    '''
    - Generates a block from pending transactions
    - Runs the proof of work algorithm to find the correct nonce (hence validating the block)
    - Adds the block to the chain
    - Rewards the miner by adding a transaction granting the miner a coin
    '''
    non_validated_new_block = blockchain.generateBlock()
    validated_new_block     = blockchain.proofOfWork(non_validated_new_block)
    blockchain.registerBlock(validated_new_block)
    reward_transaction = {
        'sender': 'MINING',
        'receiver': node_id,
        'amount': 1
    }
    blockchain.registerTransaction(reward_transaction)
    block_index = validated_new_block['indx']
    response = {
        'message': f'Block {block_index} added to the blockchain',
        'index': block_index,
        'transactions': validated_new_block['transactions'],
        'nonce': validated_new_block['nonce'],
        'previous_hash': validated_new_block['previous_hash']
    }
    return jsonify(response), 200




@app.route('/transactions', methods=['GET'])
def getTransactions():
    '''
    - Returns a list of all pending transactions
    '''
    transactions = blockchain.pending_transactions
    response = {
        'transactions': transactions
    }
    return jsonify(response), 200



@app.route('/transactions/new', methods=['POST'])
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
    if not provided_fields['amount'] or type(provided_fields['amount']) != int or provided_fields['amount'] <= 0:
        return 'Invalid amount', 400

    # check is sender has enough coins
    sender_balance = blockchain.getBalance(provided_fields['sender'])
    if sender_balance < provided_fields['amount']:
        return 'Insufficient funds', 400

    # add the transaction to the pending block
    block_indx = blockchain.registerTransaction(provided_fields)
    response = {'message': f'Transaction added to pending block: #{block_indx}'}
    return jsonify(response), 201



@app.route('/chain', methods=['GET'])
def chain():
    '''
    - Returns the full blockchain of this node
    '''
    response = {
        'chain_length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200




@app.route('/balance', methods=['GET'])
def balance():
    '''
    - Returns the balance of the node
    '''
    address = request.args.get('address')
    balance = blockchain.getBalance(address)
    response = {
        'balance': balance
    }
    return jsonify(response), 200



@app.route('/nodes/register', methods=['POST'])
def registerNodes():
    ''''
    - Receives a list of new node addresses and register them on the netwok
    '''
    node_addresses = request.get_json().get('nodes')

    # handle bad requests
    if not node_addresses:
        return "Node addresses missing", 400
    
    # register the addresses
    for address in node_addresses:
        blockchain.registerNode(address)
    
    response = {
        'message': 'Nodes added to the network',
        'current_nodes':list(blockchain.nodes)
    }
    return jsonify(response), 200



@app.route('/nodes/consensus', methods=['GET'])
def consensus():
    prev_chain_length = len(blockchain.chain)
    blockchain.reachConsensus()
    new_chain_length = len(blockchain.chain)
    if new_chain_length > prev_chain_length:
        response = {
            'message': 'Our chain was replaced',
            'previous_chain_length': prev_chain_length,
            'new_chain_length': new_chain_length,
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain leads the network',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
