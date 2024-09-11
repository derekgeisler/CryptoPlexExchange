class Order:
    def __init__(self, user, token_give, amount_give, token_get, amount_get):
        self.user = user
        self.token_give = token_give
        self.amount_give = amount_give
        self.token_get = token_get
        self.amount_get = amount_get

class DEX:
    def __init__(self):
        self.orders = []
        self.trades = []

    def place_order(self, order):
        self.orders.append(order)

    def match_orders(self):
        for i, order in enumerate(self.orders):
            for j, counterparty in enumerate(self.orders[i+1:]):
                if order.token_give == counterparty.token_get and order.token_get == counterparty.token_give:
                    if order.amount_get <= counterparty.amount_give and order.amount_give <= counterparty.amount_get:
                        self.execute_trade(order, counterparty)
                        del self.orders[i]
                        del self.orders[j]
                        break

    def execute_trade(self, order1, order2):
        trade = {
            "seller": order1.user,
            "buyer": order2.user,
            "token_sold": order1.token_give,
            "amount_sold": order1.amount_give,
            "token_bought": order1.token_get,
            "amount_bought": order1.amount_get
        }
        self.trades.append(trade)
