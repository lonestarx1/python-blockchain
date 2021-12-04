# Blockchain build in python

class Blockchain:

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
    
    def registerBlock(self):
        '''
        Creates a new block and append it to the chain
        '''
        pass


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
