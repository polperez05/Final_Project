import pandas as pd
from typing import Dict, List

# Imports assume all files are in the final_project package
from final_project.host import Host
from final_project.place import Place

class City:

    def __init__(self, size, area_rates, version=0): 
        self.size = size 
        self.area_rates = area_rates 
        self.version = version 
        self.step = 0 
        self.places = []
        self.hosts = []

    def initialize(self): 
        n = self.size 
        # Initialize Places
        self.places = [Place(place_id=x, host_id=x, city=self) for x in range(n*n)] 
        
        # Setup each place (neighbours, area, etc.)
        for place in self.places:
            place.setup()
            
        # Initialize Hosts
        self.hosts = [Host(host_id=x, place=self.places[x], city=self) for x in range(n*n)] 

    def approve_bids(self, bids: List[dict]):
        if not bids:
            return []
        
        df = pd.DataFrame(bids)
        # Sort by spread descending [cite: 57]
        df = df.sort_values(by="spread", ascending=False).reset_index(drop=True)

        approved = []
        buyers_used = set() 
        places_sold = set() 

        for _, row in df.iterrows():
            place_id = int(row["place_id"])
            buyer_id = int(row["buyer_id"])
            seller_id = int(row["seller_id"])
            bid_price = float(row["bid_price"])

            # Check availability [cite: 58]
            if buyer_id in buyers_used:
                continue
            if place_id in places_sold:
                continue

            approved.append({
                "place_id": place_id,
                "seller_id": seller_id,
                "buyer_id": buyer_id,
                "bid_price": bid_price,
            })

            buyers_used.add(buyer_id)
            places_sold.add(place_id)

        return approved
    
    def execute_transactions(self, transactions: List[Dict]):
        for tx in transactions:
            place_id = tx["place_id"]
            buyer_id = tx["buyer_id"]
            seller_id = tx["seller_id"]
            price = float(tx["bid_price"])

            # Retrieve objects. Since list index = ID, we can access directly.
            buyer = self.hosts[buyer_id]
            seller = self.hosts[seller_id]
            place = self.places[place_id]

            # Transfer funds [cite: 64]
            buyer.profits -= price
            seller.profits += price

            # Update ownership [cite: 64]
            seller.assets.discard(place_id)
            buyer.assets.add(place_id)
            place.host_id = buyer_id

            # Record price history [cite: 65]
            place.price[self.step] = price

    def clear_market(self):
        # Collect all bids [cite: 67]
        all_bids = []
        # self.hosts is a list, so we iterate directly (no .values())
        for host in self.hosts: 
            all_bids.extend(host.make_bids())

        # Approve bids
        approved = self.approve_bids(all_bids)

        # Execute transactions [cite: 68]
        if approved:
            self.execute_transactions(approved)

        return approved
    
    def iterate(self):
        # 1. Update occupancy
        # Note: place.update_occupancy in your partner's code has too many arguments.
        # It should ideally be just place.update_occupancy(). 
        # Assuming your partner fixes it, or uses default args:
        for place in self.places:
            # We assume the method signatures are fixed in place.py
            # If not, this line might need arguments like (place.area, ..., ...)
            place.update_occupancy(place.area, 0, self.area_rates, 0) 

        # 2. Update profits
        for host in self.hosts:
            host.update_profits()

        # 3. Clear market
        transactions = self.clear_market()

        # 4. Advance step [cite: 70]
        self.step += 1

        return transactions
