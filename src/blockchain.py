# Blockchain build in python

class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
    def registerBlock(self):
        '''
        Creates a new block and append it to the chain
        '''
        pass


    def registerTransaction(self):
        '''
        Adds a new transaction to the list of transactions pending to be converted into a block
        '''
        pass

    
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
