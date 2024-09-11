class TokenSwapContract:
    def __init__(self, token1, token2):
        self.token1 = token1
        self.token2 = token2
        self.liquidity_pool = {token1: 0, token2: 0}

    def add_liquidity(self, user, amount1, amount2):
        self.liquidity_pool[self.token1] += amount1
        self.liquidity_pool[self.token2] += amount2

    def swap(self, user, token_in, amount_in):
        if token_in not in [self.token1, self.token2]:
            raise ValueError("Invalid token")

        token_out = self.token2 if token_in == self.token1 else self.token1
        
        k = self.liquidity_pool[self.token1] * self.liquidity_pool[self.token2]
        y = self.liquidity_pool[token_out]
        x = self.liquidity_pool[token_in]
        
        amount_out = y - (k / (x + amount_in))
        
        self.liquidity_pool[token_in] += amount_in
        self.liquidity_pool[token_out] -= amount_out
        
        return amount_out
