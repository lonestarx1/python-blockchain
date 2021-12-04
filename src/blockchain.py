# Blockchain build in python
import time


class Blockchain:

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
    
    def registerBlock(self, proof, previous_hash=None):
        '''
        - Creates a new block, append it to the chain and reset pending transactions
        - Returns the newly created block
        '''
        block = {
            'indx': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]), # todo: check is re-calculating the hash always is better
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
        last_block =  self.retrieveLastBlock()
        return last_block['indx'] + 1

    
    @staticmethod
    def hash(block):
        '''
        Hashes a block of transactions
        '''
        pass


    def retrieveLastBlock(self):
        '''
        Returns the last block in the chain
        '''
        pass
