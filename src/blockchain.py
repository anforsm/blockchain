from block import Block
from transaction import Transaction


class Blockchain:
    def __init__(self, debug=False):
        self.debug = debug
        if self.debug:
            print("Created new blockchain")
        self.genesis = Block("0", [], 0, "1")
        self.last = self.genesis

        self.blockchain = [self.genesis]
        self.blocks = {}
        self.blocks[self.genesis._hash()] = self.genesis

        self.difficulty = 2**256
        self.difficulty -= 2**239

    def get_latest_utxo(self, pubkey):
        block = self.last
        while not block._hash() == self.genesis._hash():
            tx = block.get_utxo(pubkey)
            #print("checked block ", block._hash())
            # print(pubkey)
            # print(tx.serialize())
            if tx is not None:
                return [block, tx]
            block = self.blocks[block.prev_hash]
        return None

    def get_all_utxo(self, pubkey):
        utxos = []
        block = self.last
        while not block._hash() == self.genesis._hash():
            tx = block.get_utxo(pubkey)
            if tx is not None:
                utxos.append([block, tx])
            block = self.blocks[block.prev_hash]
        return utxos

    def get_blockchain(self):
        return self.blockchain

    def add_block(self, prev_block, block):
        if not self.validate_block(prev_block, block):
            return False

        self.last = block
        self.blockchain.append(block)
        self.blocks[block._hash()] = block

        if self.debug:
            print("Added new block to change...")
            print(f"""========= Block: {len(self.blocks)} =======
            {self.last}""")

        return True

    def validate_block(self, prev_block, block):
        target = 2 ** 256 - 1 - self.difficulty
        return prev_block._hash() == block.prev_hash and int(block._hash(), 16) < target

    def serialize(self):
        return [block.serialize() for block in self.blockchain]

    def get_block(self, block_hash):
        return self.blocks[block_hash]

    def verify_transaction(self, transaction):
        if not transaction.verify_signature():
            return False

        if not transaction.from_block in self.blocks:
            return False

        block = self.get_block(transaction.from_block)
        if transaction.from_hash not in block.get_transactions():
            return False

        transaction = block.get_transaction(block.from_hash)
        if transaction.from_pubkey not in transaction.get_utxo_pubkeys():
            return False

        utxo = transaction.get_utxo(transaction.from_pubkey)
        if not utxo == transaction.get_utxo_sum():
            return False

        return True

    def mine(self, transactions, pubkey="0"):
        nonce = 0
        proposed_block = Block(
            self.last._hash(), transactions, nonce, pubkey)

        while not self.validate_block(self.last, proposed_block):
            nonce += 1
            proposed_block.set_nonce(nonce)

        if self.debug:
            print("Found new block, adding to chain...")

        return self.add_block(self.last, proposed_block)
