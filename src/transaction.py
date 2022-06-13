from hashlib import sha256
import ecdsa
import json


class Transaction:
    def __init__(self, from_pubkey, from_block, from_tx, utxos, signature=""):
        self.from_pubkey = from_pubkey
        self.from_block = from_block
        self.from_tx = from_tx

        self.utxos = utxos

        self.signature = signature

    def sign(self, privkey):
        self.signature = bytes.hex(privkey.sign(
            bytes.fromhex(self._hash())))

    def has_pubkey(self, pubkey):
        return self.utxos.has_pubkey(pubkey)

    def verify_signature(self):
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(
            self.from_pubkey, curve=ecdsa.SECP256k1, hashfunc=sha256))
        return vk.verify(bytes.fromhex(self.signature), self._hash())

    def get_balance(self, pubkey):
        return self.utxos.get_balance(pubkey)

    def get_utxo_pubkeys(self):
        pubkeys = []
        for utxo in self.utxos:
            pubkeys.append(utxo.pubkey)
        return pubkeys

    def get_utxo_sum(self):
        tot = 0
        for utxo in self.utxos:
            tot += utxo.amount
        return tot

    def get_utxo(self, pubkey):
        for utxo in self.utxos:
            if utxo.pubkey == pubkey:
                return utxo
        return None

    def serialize(self):
        return {
            "hash": self._hash(),
            "from": self.from_pubkey,
            "utxos": self.utxos.serialize(),
            "sign": self.signature
        }

    def _hash(self):
        return sha256((str(self.from_pubkey) + str(self.from_tx) + str(self.from_block) + json.dumps(self.utxos.serialize())).encode("utf-8")).hexdigest()
