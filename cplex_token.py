from decimal import Decimal

class CPLEXToken:
    def __init__(self, initial_supply):
        self.decimals = 8  # Add this line to define the number of decimal places
        self.total_supply = initial_supply
        self.balances = {}

    def mint(self, address, amount):
        amount = int(Decimal(amount) * 10**self.decimals)
        if address not in self.balances:
            self.balances[address] = 0
        self.balances[address] += amount
        self.total_supply += amount

    def balance_of(self, address):
        return self.balances.get(address, 0)

    def get_formatted_balance(self, address):
        balance = self.balance_of(address)
        return f"{Decimal(balance) / 10**self.decimals:.8f}"

    def transfer(self, sender, recipient, amount):
        amount = int(Decimal(amount) * 10**self.decimals)
        if self.balances.get(sender, 0) < amount:
            return False
        if sender not in self.balances:
            self.balances[sender] = 0
        if recipient not in self.balances:
            self.balances[recipient] = 0
        self.balances[sender] -= amount
        self.balances[recipient] += amount
        return True

    def allowance(self, owner, spender):
        return self.allowances.get(owner, {}).get(spender, 0)

    def transfer_from(self, sender, recipient, amount):
        amount = int(Decimal(amount) * 10**self.decimals)
        if self.allowances.get(sender, {}).get(recipient, 0) < amount:
            return False
        if self.balances.get(sender, 0) < amount:
            return False
        self.balances[sender] = self.balances.get(sender, 0) - amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount
        self.allowances[sender][recipient] -= amount
        return True

    def burn(self, account, amount):
        amount = int(Decimal(amount) * 10**self.decimals)
        if self.balances.get(account, 0) < amount:
            return False
        self.total_supply -= amount
        self.balances[account] -= amount
        return True
