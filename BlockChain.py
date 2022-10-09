import hashlib
import time
import sqlite3
import json

from Block import Block, buildTree, validate_transactions
from Transaction import Transaction


def genesis_block():
    return Block(0, {"starter": "yes"}, None, [], time.time(), 0, 100)


class BlockChain:

    def __init__(self):
        self.block_chain: list[Block] = [genesis_block()]
        self.pending_transaction: list[Transaction] = []
        self.nonce: str = "0000"

    def get_latest_block(self):
        return self.block_chain[-1]

    def get_last_proof(self):
        return self.get_latest_block().proof

    def new_transaction(self, transaction: Transaction):
        if transaction.user_to_signature and transaction.sender_signature:
            self.pending_transaction.append(transaction)
        else:
            raise Exception("Transaction has faulty signature! ")

    def add_block(self):
        (merkel_tree_root, merkel_tree) = buildTree(self.pending_transaction)
        new_block = Block(len(self.block_chain), self.pending_transaction, merkel_tree, merkel_tree_root, time.time(),
                          self.get_latest_block().hash, self.proof_of_work(self.get_last_proof()))
        validate_transactions(self.pending_transaction, new_block.merkelTree)
        self.block_chain.append(new_block)
        self.pending_transaction = []

    def get_first_proof(self):
        return self.block_chain[0].proof

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == self.nonce

    def proof_of_work(self, last_proof):
        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def toJson(self):
        json_obj = json.dumps(
            {
                "transaction_data": self.block_chain,
            }
        )
        return json_obj
