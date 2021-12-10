# Blockchain build in python
import time
import hashlib
import json
import requests
from urllib.parse import urlparse

class Blockchain:

    def __init__(self, mining_difficulty):
        '''
        - Initialize the blockchain with a genesis block
        '''
        self.mining_difficulty = mining_difficulty
        self.chain = []
        self.pending_transactions = []
        self.nodes = set()
        genesis_block = {
            'indx': 1,
            'timestamp': 1639170932.3943253,
            'transactions': [
                {
                    "sender":"0",
                    "receiver":"Adriel",
                    "amount": 1000
                }
            ],
            'previous_hash':  1,
            'nonce': 35093
        }
        self.registerBlock(genesis_block)

    

    @staticmethod
    def hash(block):
        '''
        - Hashes a block of transactions, returning SHA-256 hash
        - sorting dict keys makes for consistent hash
        '''
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()



    def registerBlock(self, block):
        '''
        - Register a new block in the chain
        - Reset the list of pending transactions
        '''
        self.chain.append(block)
        if self.isValidChain(self.chain):
            print('Blockchain is valid')
            self.pending_transactions = []
        else:
            print("Invalid chain")
            self.chain.pop()



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



    def registerTransaction(self, transaction):
        '''
        - Adds a new transaction to the list of transactions pending to be converted into a block
        - Returns the index of the block that will be containing this transaction
        '''
        self.pending_transactions.append(transaction)
        return self.chain[-1]['indx'] + 1
 


    def proofOfWork(self, block):
        '''
        - Find a number 'nonce' such that when added to the block and hashed, 
        the result is a string of 4 leading zeros
        '''
        while True:
            cur_hash = self.hash(block)
            print(cur_hash)
            if cur_hash[:self.mining_difficulty] == '0' * self.mining_difficulty:
                break
            block['nonce'] += 1
        return block



    def getBalance(self, address):
        '''
        - Returns the balance of the given address
        '''
        balance = 0
        # iterate over all blocks in the chain
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == address:
                    balance -= transaction['amount']
                if transaction['receiver'] == address:
                    balance += transaction['amount']
        # iterate over all pending transactions
        for transaction in self.pending_transactions:
            if transaction['sender'] == address:
                balance -= transaction['amount']
            if transaction['receiver'] == address:
                balance += transaction['amount']
        return balance


    
    def isValidChain(self, chain=None):
        '''
        - Checks is the given chain is valid.
        - Returns True if the chain is valid, False otherwise
        '''
        prev_block = self.chain[0]
        cur_block_indx = 1
        while cur_block_indx < len(self.chain):
            # check if its "prev_hash" is the correct hash of the previous block
            if self.chain[cur_block_indx]['previous_hash'] != self.hash(prev_block):
                return False
            # check if the proof of work has been done correctly for cur_block
            cur_block_hash = self.hash(self.chain[cur_block_indx])
            if cur_block_hash[:self.mining_difficulty] != "0" * self.mining_difficulty:
                return False
            # if all checks out advance to the next block
            prev_block = self.chain[cur_block_indx]
            cur_block_indx += 1
        return True
