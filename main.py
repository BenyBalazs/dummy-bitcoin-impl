import json

import rsa


from BlockChain import BlockChain
from Transaction import Transaction
from User import User

block_chain = BlockChain()

(publicKeyForUser1, privateKeyForUser1) = rsa.newkeys(1024)
(publicKeyForUser2, privateKeyForUser2) = rsa.newkeys(1024)
user1 = User("Bob", publicKeyForUser1, privateKeyForUser1)
user2 = User("Alice", publicKeyForUser2, privateKeyForUser2)

transaction_1_data = {
    "from": user1.name,
    "to": user2.name,
    "amount": 100
}

transaction_2_data = {
    "from": user2.name,
    "to": user1.name,
    "amount": 50
}

transaction1 = Transaction(transaction_1_data)
transaction1.sender_signature = user1.sign(transaction1)
transaction1.user_to_signature = user2.sign(transaction1)

transaction2 = Transaction(transaction_2_data)
transaction2.sender_signature = user1.sign(transaction2)
transaction2.user_to_signature = user2.sign(transaction2)

block_chain.new_transaction(transaction1)
block_chain.new_transaction(transaction2)

block_chain.add_block()

for block in block_chain.block_chain:
    print(block.toJson())
