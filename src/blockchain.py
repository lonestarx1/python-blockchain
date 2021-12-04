# Blockchain build in python
import time
import hashlib
import json

class Blockchain:

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # genesis block
        self.registerBlock(proof=100, previous_hash=1)
    
    def registerBlock(self, proof, previous_hash=None):
        '''
        - Creates a new block, append it to the chain and reset pending transactions
        - Returns the newly created block
        '''
        block = {
            'indx': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]), # todo: check is re-calculating the hash always is better
            'nonce': 0
        }
        self.chain.append(block)
        self.pending_transactions = []
        return block


    def registerTransaction(self, sender, receiver, amount):
        '''
        - Adds a new transaction to the list of transactions pending to be converted into a block
        - Returns the index of the block that will be containing this transaction
        '''
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
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
        while self.hash(block)[:4] != '0000':
            block['nonce'] += 1
        return block['nonce']
