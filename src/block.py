from hashlib import sha256
from random import randint
from transaction import Transaction
from utxo import UTXO
import json


class Block:
    def __init__(self, prev_hash, transactions, nonce, miner):
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.transactions = transactions
        self.miner = miner
        self.add_transaction(Transaction(
            "0", "-1", "-1", UTXO.from_payment("0", 50, miner, 50)))

    def parse_block():
        pass

    def get_utxo(self, pubkey):
        for transaction in self.transactions:
            #print("checking for pubkey in tx", pubkey)
            if transaction.has_pubkey(pubkey):
                return transaction
        return None

    def add_transaction(self, transaction):
        if self.verify_transaction(transaction):
            self.transactions.append(transaction)

    def verify_transaction(self, transaction):
        return True

    def set_nonce(self, nonce):
        self.nonce = nonce

    def get_random_nonce():
        return randint(0, 1000000)

    def _hash(self):
        return sha256((
            str(self.prev_hash) +
            ",".join([tx._hash() for tx in self.transactions]) +
            str(self.nonce)).encode("utf-8")).hexdigest()
        # return sha256(json.dumps(self.serialize()).encode("utf-8")).hexdigest()

    def serialize(self):
        return {
            "hash": self._hash(),
            "prevHash": self.prev_hash,
            "nonce": self.nonce,
            "transactions": [tx.serialize() for tx in self.transactions],
            "coinbase": self.miner
        }

    def __str__(self):
        return f"""
      Hash: {self._hash()}
      Previous block: {self.prev_hash}
      Nonce: {self.nonce}
      Transactions: {self.data}
      """
