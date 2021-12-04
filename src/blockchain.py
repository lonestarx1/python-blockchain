# Blockchain build in python
import time
import hashlib
import json

class Blockchain:

    def __init__(self):
        '''
        - Initialize the blockchain with a genesis block
        '''
        self.chain = []
        self.pending_transactions = []
        genesis_block = {
            'indx': len(self.chain) + 1,
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
        - Register a new block in the chain
        - Reset the list of pending transactions
        '''
        self.chain.append(block)
        self.pending_transactions = []


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
        while self.hash(block)[:4] != '0000':
            block['nonce'] += 1
        return block
