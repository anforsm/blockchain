class UTXO:
    def __init__(self, pubkey1, amount1, pubkey2, amount2):
        self.balances = {}
        self.balances[pubkey1] = amount1
        self.balances[pubkey2] = amount2

    @staticmethod
    def from_payment(from_pubkey, total, to_pubkey, to_amount):
        return UTXO(from_pubkey, total-to_amount, to_pubkey, to_amount)

    def get_balance(self, pubkey):
        if pubkey not in self.balances:
            return False
        return self.balances[pubkey]

    def has_pubkey(self, pubkey):
        return pubkey in self.balances

    def serialize(self):
        return [
            {
                "pubkey": key,
                "amount": self.get_balance(key)
            } for key in self.balances
        ]
