class Host():
    """
    This class represents a host that owns properties in the city.
    The host class manages the properties, the profits and the bids of the host in the Airbnb market simulation.
    """
    def __init__(self, host_id, place, city, profits = 0):
        """
        Initialize a Host instance.

        Arguments: 
            host_id: unique identifier for each host.
            place: initial Place owned by the host.
            city: it refers to the City environment of the simulation.
            profits: initial funds available (set initially to 0).
        """
        self.host_id = host_id
        self.city = city
        self.profits = profits
        # The host's area is the are of its initial place.
        self.area = place.area
        # The host's assets are the set of all place_id's owned by the host taken form the Place class.
        self.assets = set([place.place_id])

    def update_profits(self):
        """
        Increases the host's profits depending on the rate and the occupancy (one iteration for each place_id the host owns).
        """
        monthly_earnings = 0
        # For each place_id the host owns.
        for place_id in self.assets:
            # Retrieve the place object from the City class.
            place = self.city.places[place_id]
            # Update the host's monthly earnings for each iteration.
            monthly_earnings = monthly_earnings + place.rate * place.occupancy
        # Update the host's profits by adding the total monthly_earnings from all the listings he/she owns.
        self.profits = self.profits + monthly_earnings
    
    def make_bids(self):
        """
        Defines the host's behaviour in the market.

        Identifies listings adjacent to the initial place and makes bids for them if they can be acquired.

        Returns:
        List of dictionaries with the information of the bids he/she makes.
        """
        bids = []
        opportunities = set()
        
        # Identify neighbouring listings to the listings he/she owns but are not owned by anyone.
        for my_place_id in self.assets:
            my_place = self.city.places[my_place_id]
            # Of each property the hosts owns, we check if the neighbouring properties are owned. If they are not, we add them
            # to the opportunities set.
            for adjacent_id in my_place.neighbours:
                adjacent_place = self.city.places[adjacent_id]
                if adjacent_place.host_id != self.host_id:
                    opportunities.add(adjacent_id)
        # For each opportunity, create a bid if the current profits are greater than the ask price.
        for pid in opportunities:
            place = self.city.places[pid]
            ask_price = list(place.price.values())[-1]

        # Version 0: Hosts bid all their profits.
            
            if self.profits >= ask_price:
                bid = {
                    'place_id': pid,
                    'seller_id': place.host_id,
                    'buyer_id': self.host_id,
                    'spread': self.profits - ask_price,
                    'bid_price': self.profits
                }
                bids.append(bid)

        # Version 1: Hosts bid the asking price + 10%
                
            if self.city.rule_version == 1:
                bid_price = ask_price * 1.10
                # If we cannot afford the moderate bid, we don't bid
                if self.profits < bid_price:
                    continue
        
        # Return a list with all the bids the host will make.
        return bids
