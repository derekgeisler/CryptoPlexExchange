import hashlib
import ecdsa

class Wallet:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()

    def generate_address(self):
        public_key_bytes = self.public_key.to_string()
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        return hashlib.sha256(ripemd160_hash).hexdigest()

    def sign_transaction(self, transaction):
        transaction_string = str(transaction)
        signature = self.private_key.sign(transaction_string.encode('utf-8'))
        return signature
