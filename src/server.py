import socket
import requests
import sys
import json
from flask import Flask, jsonify, request
import uuid
from blockchain import Blockchain


# Creating a node on the network, with a uniuqe id
app = Flask(__name__)
node_id = str(uuid.uuid4()).replace('-', '')

# current node's address
host_ip = socket.gethostbyname(socket.gethostname())
port = sys.argv[1] if len(sys.argv) > 1 else 5000
host_address =  host_ip + ':' + str(port)


# Instantiate the Blockchain
blockchain = Blockchain(mining_difficulty=3)

# Registering a new node on the network

if host_address != blockchain.seed_node_address:
    
    # Get addresses of the nodes on the network from the seed node
    try:
        res = requests.get(f'http://{blockchain.seed_node_address}/nodes')
        if res.status_code != 200:
            pass
        node_addresses = res.json()['nodes']
        for address in node_addresses:
            blockchain.nodes.add(address)
    except:
        pass

    # announce & register my address to all other nodes
    for address in blockchain.nodes:
        try:
            requests.post(f'http://{address}/nodes/register', data=json.dumps({'nodes': [host_address,]}), headers={'Content-Type': 'application/json'})
        except:
            pass
    
    # register my own address as well
    blockchain.nodes.add(host_address)


@app.route('/mine', methods=['GET'])
def mine():
    '''
    - if seed node:forward the mining request to all other nodes on the nwtwork
    - else: try mining the block
    '''

    
    if host_address == blockchain.seed_node_address:
        print('I AM SEED NODE, FORWORDING TO PARTICIPANTS')
        # forward the mining request to all other nodes on the network
        for address in blockchain.nodes:
            if address == host_address:
                continue
            try:
                requests.get(f'http://{address}/mine')
            except:
                pass
        return jsonify({'message': 'Mining request forwarded to all nodes on the network'}), 200
    else:
        print('I AM A PARTICIPANT NODE, MINING THE BLOCK')

        # if no pending transactions there is no work to do
        if len(blockchain.pending_transactions) == 0:
            print("NO PENDING TRANSACTIONS")
            return jsonify({'message': 'No transactions to mine'}), 200

        # generate a block from pending transactions
        non_validated_new_block = blockchain.generateBlock()
       
        # run the proof of work algorithm to find the correct nonce (hence validating the block)
        validated_new_block     = blockchain.proofOfWork(non_validated_new_block)
        print('VALIDATED BLOCK',  validated_new_block)

        # try to add a block to the chain if it is valid
        did_register_block = blockchain.registerBlock(validated_new_block)

        # If successful reward the miner by adding a transaction granting the miner a coin
        if did_register_block:
            reward_transaction = {
                'sender': 'MINING',
                'receiver': node_id,
                'amount': 1
            }
            blockchain.registerTransaction(reward_transaction)
            print('WINNNING BLOCK MINED, 1 COIN RECEIVED')

            block_index = validated_new_block['indx']
            response = {
                'message': f'Block {block_index} added to the blockchain',
                'index': block_index,
                'transactions': validated_new_block['transactions'],
                'nonce': validated_new_block['nonce'],
                'previous_hash': validated_new_block['previous_hash']
            }
            return jsonify(response), 200
        else:
            print('OTHER NODE MINED THE BLOCK, NO REWARD')
            return jsonify({'message': 'Block is not valid, or other node finished first'}), 200



@app.route('/transactions', methods=['GET'])
def getPendingTransactions():
    '''
    - Returns all the pending transactions
    '''
    response = {
        'transactions': blockchain.pending_transactions,
        'length': len(blockchain.pending_transactions)
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def newTransaction():
    '''
    - If seed node forward to participant nodes:
    - else: register the transaction in the pending transactions
    '''
    if host_address == blockchain.seed_node_address:
        print('I AM SEED NODE, FORWORDING THE REQUEST TO PARTICIPANT NODES')
        # forward the request to all other nodes on the network
        for address in blockchain.nodes:
            if address == host_address:
                continue
            try:
                requests.post(f'http://{address}/transactions/new', data=json.dumps(request.get_json()), headers={'Content-Type': 'application/json'})
            except:
                pass
        return jsonify({'message': 'Request forwarded to all nodes on the network'}), 200
    else:
        print('I AM A PARTICIPANT NODE, REGISTERING TRANSACTION')
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
        block_indx = blockchain.registerTransaction(provided_fields)
        print("transaction registered")
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



@app.route('/nodes', methods=['GET'])
def getNodes():
    '''
    - Returns the nodes on the network
    '''
    response = {
        'nodes': list(blockchain.nodes)
    }
    return jsonify(response), 200



@app.route('/nodes/register', methods=['POST'])
def registerNodes():
    ''''
    - Receives a list of new node addresses and register them on the netwok
    '''
    node_addresses = request.get_json().get('nodes')
    print("New node joined the network:", node_addresses)

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
    app.run(host='0.0.0.0', port=port)
