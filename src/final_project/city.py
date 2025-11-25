import pandas as pd
from typing import Dict, List

# Imports the Host and Place classes in this file
from final_project.host import Host
from final_project.place import Place

class City:

    def __init__(self, size, area_rates, rule_version=0): 
        self.size = size 
        self.area_rates = area_rates 
        self.rule_version = rule_version 
        self.step = 0 
        self.places = []
        self.hosts = []

    def initialize(self): 
        n = self.size 
        # Initialize Places
        self.places = [Place(place_id=x, host_id=x, city=self) for x in range(n*n)] 
        
        # Run .setup() (Created in place.py) for each Place object
        for place in self.places:
            place.setup()
            
        # Initialize Hosts
        self.hosts = [Host(host_id=x, place=self.places[x], city=self) for x in range(n*n)] 

    def approve_bids(self, bids: List[dict]):
        if not bids:
            return []
        
        df = pd.DataFrame(bids)
        # We Sort by spread in descending order and clean the index
        df = df.sort_values(by="spread", ascending=False).reset_index(drop=True)

        # Create lists to track accepted bids, used buyers and sold places
        approved = []
        buyers_used = set() 
        places_sold = set() 

        # we set the correct type for each column
        for _, row in df.iterrows():
            place_id = int(row["place_id"])
            buyer_id = int(row["buyer_id"])
            seller_id = int(row["seller_id"])
            bid_price = float(row["bid_price"])

            # Check availability and skip if already occupied
            if buyer_id in buyers_used:
                continue
            if place_id in places_sold:
                continue

            # Record of the approved bids
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
        
        # Process each approved transaction and extract ID and price
        for tx in transactions:
            place_id = tx["place_id"]
            buyer_id = tx["buyer_id"]
            seller_id = tx["seller_id"]
            price = float(tx["bid_price"])

            # Retrieve objects
            buyer = self.hosts[buyer_id]
            seller = self.hosts[seller_id]
            place = self.places[place_id]

            # Transfer funds 
            buyer.profits -= price
            seller.profits += price

            # Update ownership
            seller.assets.discard(place_id)
            buyer.assets.add(place_id)
            place.host_id = buyer_id

            # Record price history [cite: 65]
            place.price[self.step] = price

    def clear_market(self):
        # We will create a new list and then run for each host and record their bids 
        all_bids = []

        for host in self.hosts: 
            all_bids.extend(host.make_bids())

        # Pass all colected bids to approve_bids to sort and filter them
        approved = self.approve_bids(all_bids)

        # Execute transactions
        if approved:
            self.execute_transactions(approved)

        return approved
    
    def iterate(self):
        # Update occupancy for each place
        for place in self.places:
            place.update_occupancy()

        # Update profits for each host
        for host in self.hosts:
            host.update_profits()

        #  Clear market
        transactions = self.clear_market()

        # 4. Advance one step
        self.step += 1

        return transactions
