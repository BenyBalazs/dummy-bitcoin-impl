import hashlib
import time
import sqlite3
import json

from merkletools import MerkleTools

from Transaction import Transaction

def calculate_hash(index, previous_hash, timestamp, data):
    return hashlib.sha256(
        (str(index) + str(previous_hash) + str(timestamp) + json.dumps(data)).encode('utf-8')).hexdigest()


class Block:

    def __init__(self, index, transaction_list, merkelTree, merkelTreeRoot, timestamp, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transaction_list = transaction_list
        self.merkelTree = merkelTree
        self.merkelTreeRoot = merkelTreeRoot
        self.previous_hash = previous_hash
        self.hash = calculate_hash(index, timestamp, merkelTreeRoot, previous_hash)
        self.proof = proof

    def calculate_hash(self):
        return hashlib.sha256(
            str(self.index) + str(self.previous_hash) + str(self.timestamp) + json.dumps(
                self.merkelTreeRoot)).hexdigest()

    def toJson(self):
        return json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "merkelTreeRoot": self.merkelTreeRoot,
                "previous_hash": self.previous_hash,
                "hash": self.hash,
                "proof": self.proof,
            }
        )

    def to_json_no_proof(self):
        return json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "merkelTreeRoot": self.merkelTreeRoot,
                "previous_hash": self.previous_hash,
                "hash": self.hash
            }
        )


def buildTree(transactions: list[Transaction]):
    mt = MerkleTools(hash_type="md5")
    for t in transactions:
        mt.add_leaf(t.toJson(), True)
        print(t)
    mt.make_tree()
    return mt.get_merkle_root(), mt


def validate_transactions(transactions: list[Transaction], mt: MerkleTools):
    hash_function = mt.hash_function
    for t in transactions:
        v = t.toJson().encode('utf-8')
        v = hash_function(v).hexdigest()
        v = bytearray.fromhex(v)
        if v not in mt.leaves:
            raise Exception("Invalid transaction in the list")
