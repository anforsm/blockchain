from blockchain import Blockchain
from transaction import Transaction
from utxo import UTXO
import ecdsa


class Wallet:
    def __init__(self):
        self.blockchain = Blockchain()
        self.privkey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.pubkey = self.privkey.get_verifying_key()
        self.pubkeystring = self.pubkey.to_string().hex()

    def get_latest_utxo(self):
        utxo = self.blockchain.get_latest_utxo(self.pubkeystring)
        return utxo

    def get_all_utxo(self):
        return self.blockchain.get_all_utxo(self.pubkeystring)

    def balance(self):
        utxos = self.get_all_utxo()
        tot = 0
        for utxo in utxos:
            tot += utxo[1].get_balance(self.pubkeystring)
        return tot

    def pay(self, to_pubkey, amount):
        block, utxo = self.blockchain.get_latest_utxo(self.pubkeystring)
        tx = Transaction(self.pubkeystring, block._hash(), utxo._hash(), UTXO.from_payment(
            self.pubkeystring, self.balance(), to_pubkey, amount))
        tx.sign(self.privkey)

        self.blockchain.mine([tx], self.pubkeystring)

    def mine(self):
        self.blockchain.mine([], self.pubkeystring)
