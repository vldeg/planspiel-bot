from datetime import datetime, timezone, timedelta
import requests
import config

class APIProvider:

	def __init__(self, base_url="", headers=None, timeout=30):
		self.base_url = base_url.rstrip("/")
		self.timeout = timeout
		self.session = requests.Session()
		self.session.headers.update({"Content-Type": "application/json"})
		if headers:
			self.session.headers.update(headers)

	def request(self, method, endpoint, *, params=None, data=None, headers=None):
		url = f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint
		response = self.session.request(
			method=method.upper(),
			url=url,
			params=params,
			json=data,
			headers=headers,
			timeout=self.timeout,
		)
		response.raise_for_status()
		if not response.content:
			return None
		return response.json()

	def authorize(self):
		req = self.request(
			"POST", 
			"/v-ms3/authenticate", 
			data={"userName": config.API_USERNAME, "password": config.API_PASSWORD}
		)
		if req["success"]:
			self.token = req["result"]["token"]["accessToken"]
			return self.token
		
	def get_portfolio_stats(self, portfolio_id):
		req = self.request(
			"GET", 
			f"/v-ms1/portfolio/getPortfolioWithItems?portfolioId={portfolio_id}&withItems=false&withOrderIds=false",
		    headers={"Authorization": f"Bearer {self.token}"}
        )
		return {
			"id": req["portfolio"]["id"],
			"name": req["portfolio"]["name"],
			"equity": req["portfolio"]["value"],
			"available_cash": req["portfolio"]["availableCredit"],
			"performance": req["portfolio"]["performanceAbs"]
        }
	
	def get_portfolio_items(self, portfolio_id):
		req = self.request(
			"GET", 
			f"/v-ms1/portfolio/getPortfolioWithItems?portfolioId={portfolio_id}&withItems=true&withOrderIds=true",
		    headers={"Authorization": f"Bearer {self.token}"}
		)

		items = []
		for item in req.get("items", []):
			items.append({
				"name": item["instrument"]["name"].strip(),
				"isin": item["instrument"]["isin"],
				"type": item["instrument"]["instrumentType"],
				"current_price": item["instrument"]["price"],
				"quantity": item["quantity"],
				"buy_price": item["buyPrice"],
				"buy_value": item["buyValue"],
				"buy_date": item["buyDate"],
			})
		return items

	def get_orders(self, order_status, portfolio_id):
		if order_status not in ["OPEN", "CANCELLED", "EXPIRED"]:
			raise ValueError("Invalid order status provided")
		
		return self.request(
			"GET",
			f"/v-ms1/order/getOrders?status={order_status}&portfolioId={portfolio_id}",
			headers={"Authorization": f"Bearer {self.token}"}
		)

	def place_buy_order(self, portfolio_id, isin, quantity, limit):
		return self.request(
			"POST",
			"/v-ms3/order/placeOrder",
			headers={"Authorization": f"Bearer {self.token}"},
			data={
				"idExchange": 1, # Börse Stuttgart,
				"portfolioId": portfolio_id,
				"orderType": "BUY",
				"orderSubType": "LIMIT",
				"limit": limit,
				"isin": isin,
				"quantity": quantity,
				"validUntil": (datetime.now(timezone.utc)
				               .isoformat(timespec="milliseconds")
							   .replace("+00:00", "Z")),
				"noteText": None,
			}
		)

	def place_sell_order(self, portfolio_id, isin, quantity, stop_loss):
		return self.request(
			"POST",
			"/v-ms3/order/placeOrder",
			headers={"Authorization": f"Bearer {self.token}"},
			data={
				"idExchange": 1, # Börse Stuttgart,
				"portfolioId": portfolio_id,
				"orderType": "SELL",
				"orderSubType": "STOP",
				"stop": stop_loss,
				"isin": isin,
				"quantity": quantity,
				"validUntil": ((datetime.now(timezone.utc) + timedelta(days=14))
				               .isoformat(timespec="milliseconds")
							   .replace("+00:00", "Z")),
				"noteText": None,
			}
		)
