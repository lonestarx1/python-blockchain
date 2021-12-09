# Blockchain build in python
import time
import hashlib
import json
import requests
from urllib.parse import urlparse

class Blockchain:

    # in practice we would discover seed nodes though a DNS service
    seed_node_address =  '61.73.43.24:5000'

    def __init__(self, mining_difficulty):
        '''
        - Initialize the blockchain with a genesis block
        '''
        self.mining_difficulty = mining_difficulty
        self.chain = []
        self.pending_transactions = []
        self.nodes = set(['61.73.43.24:5000'])
        genesis_block = {
            'indx': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash':  1,
            'nonce': 100
        }
        self.registerBlock(genesis_block)

    
    def generateBlock(self):
        '''
        - Creates a new block from pending transactions and return it to the caller
        '''
        block = {
            'indx': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.pending_transactions,
            'previous_hash':  self.hash(self.chain[-1]),
            'nonce': 0
        }
        return block

    
    def registerBlock(self, block):
        '''
        - add a new block to the chain
        - if the resulting chain is valid save it, else undo it
        '''
        # before we may try appending a block, we have to get the longest valid chain on the network
        self.reachConsensus()

        # try appending the block to the current chain
        self.chain.append(block)

        # if valid we win
        if self.isValidChain(self.chain):
            self.pending_transactions = []
            return True
        
        # else undo what we added
        self.chain.pop()
        return False


    def registerTransaction(self, transaction):
        '''
        - Adds a new transaction to the list of transactions pending to be converted into a block
        - Returns the index of the block that will be containing this transaction
        '''
        self.pending_transactions.append(transaction)
        return self.chain[-1]['indx'] + 1

    
    @staticmethod
    def hash(block):
        '''
        - Hashes a block of transactions, returning SHA-256 hash
        - sorting dict keys makes for consistent hash
        '''
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    
    def proofOfWork(self, block):
        '''
        - Find a number 'nonce' such that when added to the block and hashed, the result is a string of 4 leading zeros
        '''
        while True:
            cur_hash = self.hash(block)
            # uncomment the next line to see proof-of-work in action
            print(cur_hash)
            if cur_hash[:self.mining_difficulty] == '0' * self.mining_difficulty:
                break
            block['nonce'] += 1
        return block


    def registerNode(self, node_address):
        '''
        - Add a new node to the list of nodes 
        '''
        self.nodes.add(node_address)

    
    def isValidChain(self, received_chain=None):
        '''
        - Checks is the given chain is valid.
        - Returns True if the chain is valid, False otherwise
        '''
        chain = received_chain or self.chain
        prev_block = chain[0]
        cur_block_indx = 1
        while cur_block_indx < len(chain):
            # check if its "prev_hash" is the correct hash of the previous block (except if prev block is genesis block)
            if prev_block['indx'] > 0 and  chain[cur_block_indx]['previous_hash'] != self.hash(prev_block):
                return False
            # check if the proof of work has been done correctly for cur_block
            cur_block_hash = self.hash(chain[cur_block_indx])
            
            if cur_block_hash[:self.mining_difficulty] != "0" * self.mining_difficulty:
                return False
            # if all checks out advance to the next block
            prev_block = chain[cur_block_indx]
            cur_block_indx += 1
        return True


    def reachConsensus(self):
        '''
        - A consensus algorithm that replaces the current node's chain with the longest valid chain on the network
        - visits all nodes on the network, download their chain, verifies them and keep the longest
        '''
        print("GETTING THE LONGEST VALID CHAIN ON THE NETWORK")
        longest_valid_chain = self.chain

        # verify the chains from all nodes
        for node in self.nodes:
            try:
                res = requests.get(f'http://{node}/chain')
                if res.status_code != 200:
                    continue
                chain, length = res.json()['chain'], res.json()['length']
            except:
                continue
            
            # record any valid chain longer than the best we have so far
            if length > len(longest_valid_chain) and self.isValidChain(chain):
                longest_valid_chain = chain
            
        # replace the current node's chain with the winner
        self.chain = longest_valid_chain
        print(f"CURRENT CHAIN HAS LENGTH {len(self.chain)}")
