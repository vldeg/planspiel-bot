from loguru import logger
from tinydb import Query
from api import APIProvider
from db import get_order
import config 

def check_orders():
    api = APIProvider(config.API_BASE_URL)
    try:
        api.authorize()
    except Exception:
        logger.exception("Connection to Planspiel Börse API failed.")
        return

    items = api.get_portfolio_items(config.PORTFOLIO_ID)
    if not items:
        logger.warning("Portfolio {id} doesn't own any stocks", id=config.PORTFOLIO_ID)

    stop_loss_orders = [
        order for order in api.get_orders("OPEN", config.PORTFOLIO_ID)
        if order["orderType"] == "SELL"
        and order["orderSubType"] == "STOP"
        and order["orderStatus"] == "PENDING"
    ]

    for item in items:
        isin = item["isin"]
        saved_order = get_order(isin)

        if not saved_order:
            logger.warning("No saved data found for {name} ({isin}). Skipping...", name=item["name"], isin=isin)
            continue

        stop_loss = saved_order.stop_loss

        order = next(
            (
                o for o in stop_loss_orders
                if o["instrument"]["isin"] == isin
                and int(o["stopLimit"]) == int(stop_loss)
                and float(o["quantity"]) == float(item["quantity"])
            ),
            None
        )

        if order is None:
            logger.warning("Missing Stop-Loss order for {name} ({isin}). Creating...", name=item["name"], isin=isin)
            try:
                api.place_sell_order(config.PORTFOLIO_ID, isin, item["quantity"], stop_loss)
                logger.success("Placed a Stop-Loss order for {name} ({isin}), Stop-Loss: {stop_loss} EUR", 
                               name=item["name"], 
                               isin=isin, 
                               stop_loss=stop_loss)
            except Exception:
                logger.exception("Failed to place a Stop-Loss order for {name} ({isin})", name=item["name"], isin=isin)
            
if __name__ == "__main__":
    check_orders()
    