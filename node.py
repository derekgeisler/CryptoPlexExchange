import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from blockchain import Blockchain, Block
from wallet import Wallet
from dex import DEX, Order
from smart_contracts import TokenSwapContract

class Node:
    def __init__(self):
        self.blockchain = Blockchain()
        self.wallet = Wallet()
        self.dex = DEX()
        self.token_swap_contract = TokenSwapContract("TOKEN1", "TOKEN2")

    def create_block(self, data):
        latest_block = self.blockchain.get_latest_block()
        new_block = Block(latest_block.index + 1, latest_block.hash, int(time.time()), data, "")
        self.blockchain.add_block(new_block)

    def place_order(self, token_give, amount_give, token_get, amount_get):
        order = Order(self.wallet.address, token_give, amount_give, token_get, amount_get)
        self.dex.place_order(order)

    def swap_tokens(self, token_in, amount_in):
        amount_out = self.token_swap_contract.swap(self.wallet.address, token_in, amount_in)
        return amount_out

    def add_liquidity(self, amount1, amount2):
        self.token_swap_contract.add_liquidity(self.wallet.address, amount1, amount2)

    def process_trades(self):
        self.dex.match_orders()
        for trade in self.dex.trades:
            self.create_block(trade)
def main():
    try:
        print("Starting application...")
        app = QApplication(sys.argv)
        print("QApplication created")
        gui = CryptoPlexGUI()
        print("GUI instance created")
        gui.show()
        print("GUI shown")
        print("Entering main event loop...")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Traceback:")
        traceback.print_exc()

import traceback

if __name__ == '__main__':
    try:
        # Your main node execution code here
        pass
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error(traceback.format_exc())

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt

class CryptoPlexGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.setProperty("_q_styled_item_has_no_animation", True)
        # ... rest of your __init__ method ...

    def event(self, event):
        if event.type() == Qt.ApplicationStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.accept()
                return True
        return super().event(event)

import logging
import traceback

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
