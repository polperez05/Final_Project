import random
import numpy as np
import pandas as pd
from typing import Dict, List, Set
import matplotlib.pyplot as plt

def __init__(self, size: int, area_rates: Dict[int, tuple]):
  self.size = size
  self.area_rates = area_rates
  # precompute area mean rates for occupancy decisions
  self.area_mean_rate = {a: (low + high) / 2.0 for a, (low, high) in area_rates.items()}
  self.step = 0
  self.places: List[Place] = []
  self.hosts: Dict[int, Host] = {}

def initialize(self):
    # create places
    n = self.size * self.size
    self.places = [Place(place_id=i, host_id=i, city=self) for i in range(n)]
    # call setup to initialize area, neighbours, rate, price
    for p in self.places:
        p.setup()

    # create hosts: 1 host per initial place; host_id = place_id
    self.hosts = {}
    for p in self.places:
        h = Host(host_id=p.place_id, place=p, city=self, profits=0.0)
        self.hosts[h.host_id] = h

def update_occupancies(self):
    for p in self.places:
        p.update_occupancy()

def update_profits(self):
    for host in self.hosts.values():
        host.update_profits()

def make_all_bids(self):
    all_bids = []
    for host in self.hosts.values():
        all_bids.extend(host.make_bids())
    return all_bids

def approve_bids(self, bids: List[dict]):
    if len(bids) == 0:
        return []
    df = pd.DataFrame(bids)
    # sort by spread desc (more competitive first)
    df = df.sort_values(by="spread", ascending=False).reset_index(drop=True)

    approved = []
    buyers_used = set()
    places_sold = set()

    for _, row in df.iterrows():
        pid = int(row["place_id"])
        buyer = int(row["buyer_id"])
        seller = int(row["seller_id"])
        bid_price = float(row["bid_price"])

        # check both buyer and place are still available
        if buyer in buyers_used:
            continue
        if pid in places_sold:
            continue
        # also ensure buyer still has enough profits (profits may change if we had earlier transactions)
        if self.hosts[buyer].profits < bid_price:
            continue

        # approve
        approved.append({
            "place_id": pid,
            "seller_id": seller,
            "buyer_id": buyer,
            "bid_price": bid_price
        })
        buyers_used.add(buyer)
        places_sold.add(pid)
    return approved

def execute_transactions(self, transactions: List[dict]):
    for tx in transactions:
        pid = tx["place_id"]
        seller_id = tx["seller_id"]
        buyer_id = tx["buyer_id"]
        price = float(tx["bid_price"])

        seller = self.hosts[seller_id]
        buyer = self.hosts[buyer_id]
        place = self.places[pid]

        # transfer money
        buyer.profits -= price
        seller.profits += price

        # transfer ownership
        seller.assets.discard(pid)
        buyer.assets.add(pid)
        place.host_id = buyer_id

        # record sale price at current step
        place.price[self.step] = price

def step_once(self):
    # 1) Update occupancies for all places (occupancy depends only on rate vs area mean)
    self.update_occupancies()
    # 2) Update profits (hosts earn money from occupancy this month)
    self.update_profits()
    # 3) Hosts make bids
    bids = self.make_all_bids()
    # 4) Approve bids
    approved = self.approve_bids(bids)
    # 5) Execute transactions
    self.execute_transactions(approved)
    # 6) increment step
    self.step += 1

def run(self, n_steps: int):
    for _ in range(n_steps):
        self.step_once()

def compute_host_wealth(self):
    # wealth = current profits + sum(most recent sale price of all properties owned)
    records = []
    for host in self.hosts.values():
        prop_vals = 0.0
        for pid in host.assets:
            place = self.places[pid]
            latest_price = place.price[max(place.price.keys())]
            prop_vals += latest_price
        wealth = host.profits + prop_vals
        records.append({
            "host_id": host.host_id,
            "wealth": wealth,
            "profits": host.profits,
            "n_assets": len(host.assets)
        })
    return pd.DataFrame(records).set_index("host_id")


