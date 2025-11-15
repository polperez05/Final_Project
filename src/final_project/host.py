class Host():
    def __init__(self, host_id, place, city, profits = 0):
        self.host_id = host_id
        self.city = city
        self.profits = profits
        self.area = place.area
        self.assets = set([place.place_id])

    def update_profits(self):
        monthly_earnings = 0
        for place_id in self.assets:
            place = self.city.places[place_id]
            monthly_earnings = monthly_earnings + place.rate * place.occupancy
        self.profits = self.profits + monthly_earnings
    
    def make_bids(self):
        bids = []
        opportunities = {()}
        
        for my_place_id in self.assets:
            my_place = self.city.places[my_place_id]
            for adjacent_id in my_place.neighbours:
                adjacent_place = self.city.places[adjacent_id]
                if adjacent_place.host_id != self.host_id:
                    opportunities.add(adjacent_id)
        
        for pid in opportunities:
            place = self.city.places[pid]
            ask_price = {place.price.values()}[-1]
            if self.profits >= ask_price:
                bid = {
                    'place_id' = pid,
                    'seller_id' = place.host_id,
                    'buyer_id' = self.host_id,
                    'spread' = self.profits - ask_price,
                    'bid_price' = self.profits
                }
                bids.append(bid)
        return bids