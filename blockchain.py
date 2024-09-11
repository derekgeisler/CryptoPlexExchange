import hashlib
import time
from decimal import Decimal
from cplex_token import CPLEXToken

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = hash

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.data) + str(self.nonce)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 50  # Initial mining reward
        self.halving_interval = 210000  # Number of blocks for halving
        self.max_supply = 50000000  # Maximum supply of CPLEX tokens
        self.current_supply = 0
        self.cplex_token = CPLEXToken(initial_supply=0)

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "Genesis Block", 0, self.calculate_hash(0, "0", int(time.time()), "Genesis Block", 0))

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = self.calculate_hash(block.index, block.previous_hash, block.timestamp, block.data, block.nonce)
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = self.calculate_hash(block.index, block.previous_hash, block.timestamp, block.data, block.nonce)
        return computed_hash

    @staticmethod
    def calculate_hash(index, previous_hash, timestamp, data, nonce):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data) + str(nonce)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def add_cplex_transaction(self, sender, recipient, amount):
        if self.cplex_token.transfer(sender, recipient, amount):
            self.pending_transactions.append({
                "type": "CPLEX_transfer",
                "from": sender,
                "to": recipient,
                "amount": amount
            })
            return True
        return False

    def mine_pending_transactions(self, miner_address):
        if self.current_supply >= self.max_supply:
            print("Maximum supply reached. No more tokens can be mined.")
            return False

        reward = self.get_mining_reward()
        if self.current_supply + reward > self.max_supply:
            reward = self.max_supply - self.current_supply

        reward_transaction = {
            "from": "Network",
            "to": miner_address,
            "amount": reward
        }
        self.pending_transactions.append(reward_transaction)

        new_block = Block(len(self.chain), self.get_latest_block().hash, int(time.time()), self.pending_transactions, 0, "")
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.current_supply += reward
        self.cplex_token.mint(miner_address, str(reward))  # Convert reward to string
        self.pending_transactions = []
        return True

    def get_mining_reward(self):
        halvings = len(self.chain) // self.halving_interval
        return Decimal(self.mining_reward) / (2 ** halvings)

    def get_cplex_balance(self, address):
        return self.cplex_token.get_formatted_balance(address)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True