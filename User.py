import json

import rsa

import Transaction as Transaction


class User:
    def __init__(self,name, privatekey, publickey):
        self.name = name
        self.privatekey = privatekey
        self.publickey = publickey

    def sign(self, transaction: Transaction):
        return rsa.sign(json.dumps(transaction.transaction_data).encode('utf-8'), self.publickey, 'SHA-256')
