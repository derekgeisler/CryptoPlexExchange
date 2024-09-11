import sys
import traceback
from decimal import Decimal

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QTabWidget, QComboBox
from PyQt5.QtCore import Qt
from blockchain import Blockchain
from wallet import Wallet

class CryptoPlexGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.blockchain = Blockchain()
        self.wallet = Wallet()
        try:
            self.init_ui()
        except Exception as e:
            print(f"Error initializing UI: {e}")
            traceback.print_exc()

    def init_ui(self):
        self.setWindowTitle('CryptoPlex Blockchain')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Wallet Info
        wallet_info_layout = QHBoxLayout()
        wallet_info_layout.addWidget(QLabel(f"Address: {self.wallet.address}"))
        try:
            balance = self.blockchain.get_cplex_balance(self.wallet.address)
            print(f"Retrieved balance: {balance}")
        except Exception as e:
            print(f"Error getting balance: {e}")
            traceback.print_exc()
            balance = "0.00000000"
        self.balance_label = QLabel(f"CPLEX Balance: {balance}")
        wallet_info_layout.addWidget(self.balance_label)
        main_layout.addLayout(wallet_info_layout)

        # Tabs
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Transfer Tab
        transfer_tab = QWidget()
        transfer_layout = QVBoxLayout()
        transfer_tab.setLayout(transfer_layout)

        recipient_layout = QHBoxLayout()
        recipient_layout.addWidget(QLabel("Recipient:"))
        self.recipient_input = QLineEdit()
        recipient_layout.addWidget(self.recipient_input)
        transfer_layout.addLayout(recipient_layout)

        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("Amount:"))
        self.amount_input = QLineEdit()
        amount_layout.addWidget(self.amount_input)
        transfer_layout.addLayout(amount_layout)

        transfer_button = QPushButton("Transfer CPLEX")
        transfer_button.clicked.connect(self.transfer_cplex)
        transfer_layout.addWidget(transfer_button)

        tabs.addTab(transfer_tab, "Transfer")

        # Mine Tab
        mine_tab = QWidget()
        mine_layout = QVBoxLayout()
        mine_tab.setLayout(mine_layout)

        mine_button = QPushButton("Mine New Block")
        mine_button.clicked.connect(self.mine_block)
        mine_layout.addWidget(mine_button)

        self.mining_info = QLabel("Current Mining Reward: 50 CPLEX")
        mine_layout.addWidget(self.mining_info)

        self.supply_info = QLabel("Current Supply: 0 / 50,000,000 CPLEX")
        mine_layout.addWidget(self.supply_info)

        tabs.addTab(mine_tab, "Mine")

        # DEX Tab
        dex_tab = QWidget()
        dex_layout = QVBoxLayout()
        dex_tab.setLayout(dex_layout)

        # Token selection
        token_layout = QHBoxLayout()
        token_layout.addWidget(QLabel("Token:"))
        self.token_combo = QComboBox()
        self.token_combo.addItems(["CPLEX", "ETH", "BTC"]) # Add more tokens as needed
        token_layout.addWidget(self.token_combo)
        dex_layout.addLayout(token_layout)

        # Buy/Sell amount
        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("Amount:"))
        self.dex_amount_input = QLineEdit()
        amount_layout.addWidget(self.dex_amount_input)
        dex_layout.addLayout(amount_layout)

        # Buy/Sell buttons
        button_layout = QHBoxLayout()
        buy_button = QPushButton("Buy")
        buy_button.clicked.connect(self.buy_token)
        sell_button = QPushButton("Sell")
        sell_button.clicked.connect(self.sell_token)
        button_layout.addWidget(buy_button)
        button_layout.addWidget(sell_button)
        dex_layout.addLayout(button_layout)

        tabs.addTab(dex_tab, "DEX")

        # Blockchain Tab
        blockchain_tab = QWidget()
        blockchain_layout = QVBoxLayout()
        blockchain_tab.setLayout(blockchain_layout)

        self.blockchain_text = QTextEdit()
        self.blockchain_text.setReadOnly(True)
        blockchain_layout.addWidget(self.blockchain_text)

        refresh_button = QPushButton("Refresh Blockchain")
        refresh_button.clicked.connect(self.refresh_blockchain)
        blockchain_layout.addWidget(refresh_button)

        tabs.addTab(blockchain_tab, "Blockchain")

        self.refresh_blockchain()

    def transfer_cplex(self):
        recipient = self.recipient_input.text()
        amount = float(self.amount_input.text())
        if self.blockchain.add_cplex_transaction(self.wallet.address, recipient, amount):
            self.recipient_input.clear()
            self.amount_input.clear()
            self.update_balance()

    def mine_block(self):
        print("Mining new block...")
        try:
            if self.blockchain.mine_pending_transactions(self.wallet.address):
                print("Block mined successfully")
                old_balance = self.blockchain.get_cplex_balance(self.wallet.address)
                self.update_balance()
                new_balance = self.blockchain.get_cplex_balance(self.wallet.address)
                print(f"Balance changed from {old_balance} to {new_balance}")
                self.refresh_blockchain()
                self.update_mining_info()
            else:
                print("Mining failed. Maximum supply might have been reached.")
        except Exception as e:
            print(f"Error during mining: {e}")
            traceback.print_exc()

    def update_mining_info(self):
        reward = self.blockchain.get_mining_reward()
        self.mining_info.setText(f"Current Mining Reward: {reward} CPLEX")
        self.supply_info.setText(f"Current Supply: {self.blockchain.current_supply} / {self.blockchain.max_supply} CPLEX")

    def update_balance(self):
        balance = self.blockchain.get_cplex_balance(self.wallet.address)
        print(f"Updating balance: {balance}")
        self.balance_label.setText(f"CPLEX Balance: {balance}")

    def refresh_blockchain(self):
        self.blockchain_text.clear()
        for block in self.blockchain.chain:
            self.blockchain_text.append(f"Block #{block.index}")
            self.blockchain_text.append(f"Hash: {block.hash}")
            self.blockchain_text.append(f"Previous Hash: {block.previous_hash}")
            self.blockchain_text.append(f"Nonce: {block.nonce}")
            self.blockchain_text.append(f"Transactions: {block.data}")
            self.blockchain_text.append("---")
        self.update_mining_info()

    def buy_token(self):
        # Implement buy token logic here
        pass

    def sell_token(self):
        # Implement sell token logic here
        pass

def main():
    app = QApplication(sys.argv)
    gui = CryptoPlexGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()