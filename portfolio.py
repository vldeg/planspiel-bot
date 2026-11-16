import config 

class Portfolio:
    def __init__(self, equity, available_cash):
        self.equity = equity
        self.available_cash = available_cash
        self.min_cash_reserve = config.MIN_CASH_RESERVE
        self.risk_per_trade = config.RISK_PER_TRADE
        self.atr_factor = config.ATR_FACTOR
        self.fee_percentage = config.FEE_PERCENTAGE
        self.min_fee = config.MIN_FEE

    def calculate_fee(self, order_volume):
        return max(self.min_fee, self.fee_percentage * order_volume)

    def calculate_limit_and_stop_loss(self, close, atr14, eur_to_usd_rate):
        limit = close + (self.atr_factor * atr14)
        stop_loss = limit - (2.0 * atr14)
        return {
            "limit": limit / eur_to_usd_rate, 
            "stop_loss": stop_loss / eur_to_usd_rate
        }

    def calculate_position_size(self, limit, stop_loss):
        max_loss_eur = self.equity * self.risk_per_trade  
        risk_per_share = limit - stop_loss

        amount = int(max_loss_eur // risk_per_share)
        order_volume = amount * limit
        fee = self.calculate_fee(order_volume)
        total_cost = order_volume + (fee * 2)

        if total_cost + self.min_cash_reserve > self.available_cash:
            print(f"Not enough available cash to place the order. Available: {self.available_cash}, Required: {total_cost}")
            return None
        
        self.available_cash -= total_cost
        return {
            "amount": amount, 
            "order_volume": order_volume,
            "fee": fee,
            "total_fees": fee * 2,
            "total_cost": total_cost,
            "available_cash": self.available_cash
        }
