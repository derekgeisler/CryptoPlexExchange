from blockchain import Blockchain
from wallet import Wallet

def main():
    blockchain = Blockchain()
    alice_wallet = Wallet()
    bob_wallet = Wallet()
    charlie_wallet = Wallet()

    # Mint some initial CPLEX tokens to Alice
    blockchain.cplex_token.mint(alice_wallet.address, 1000)

    print(f"Alice's initial CPLEX balance: {blockchain.get_cplex_balance(alice_wallet.address)}")
    print(f"Bob's initial CPLEX balance: {blockchain.get_cplex_balance(bob_wallet.address)}")

    # Alice sends 100 CPLEX to Bob
    blockchain.add_cplex_transaction(alice_wallet.address, bob_wallet.address, 100)

    # Mine the pending transactions
    blockchain.mine_pending_transactions(charlie_wallet.address)

    print(f"Alice's CPLEX balance after transfer: {blockchain.get_cplex_balance(alice_wallet.address)}")
    print(f"Bob's CPLEX balance after transfer: {blockchain.get_cplex_balance(bob_wallet.address)}")
    print(f"Charlie's CPLEX balance after mining: {blockchain.get_cplex_balance(charlie_wallet.address)}")

    # Verify the blockchain
    print(f"Is blockchain valid? {blockchain.is_chain_valid()}")

    # Print the blockchain
    for block in blockchain.chain:
        print(f"Block #{block.index}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Nonce: {block.nonce}")
        print(f"Transactions: {block.data}")
        print("---")

if __name__ == "__main__":
    main()
