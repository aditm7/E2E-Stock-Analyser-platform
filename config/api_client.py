from requests import Session
import os
import json

class ApiClient:
  base_url = f"http://127.0.0.1:{os.environ.get("PORT")}/api"
  _routes = {
    "market_data": "/stocks/{}",
    "all_companies":"/company/all",
    "specific_company":"/company/{}"
  }
  def __init__(self):
    self.s = Session()
    h = {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "accept": "application/json",
      }
    self.s.headers.update(h)

  def get(self,route,payload={},stock_code=None): # example usage get("market_data",payload={},stock_code="")
    if stock_code is not None:
      url = f"{self.base_url}{self._routes[route].format(stock_code)}"
    else:
      url = self.base_url + self._routes[route]
    r = self.s.get(url, params=payload)
    return r.json()