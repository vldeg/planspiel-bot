from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from dataclasses import dataclass

db = TinyDB(
    "data/orders.json",
    storage=JSONStorage
)

orders = db.table("orders")

@dataclass
class OrderRecord:
    isin: str
    name: str
    amount: float
    order_volume: float
    stop_loss: float
    limit: float

def create_order(order: OrderRecord):
    orders.upsert({
        "isin": order.isin,
        "name": order.name,
        "amount": order.amount,
        "order_volume": order.order_volume,
        "stop_loss": order.stop_loss,
        "limit": order.limit
    }, Query().isin == order.isin)

def get_order(isin: str):
    Order = Query()
    res = orders.get(Order.isin == isin)
    
    if res:
        return OrderRecord(**res)
    
    return None
