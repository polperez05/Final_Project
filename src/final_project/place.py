import random as rd
class Place:
    def __init__(self, place_id, host_id, city): 
        self.place_id = place_id 
        self.host_id = host_id 
        self.city = city 
        self.occupancy = 0
    
    def setup(self):
        n = self.city.size  # set the size of the "city"
        x = self.place_id % n # it give us the column
        y = self.place_id // n # it give us the row
        neighbours = [(x-1,y-1), (x,y-1), (x+1,y-1), 
                      (x-1,y  ),            (x+1,y),    # we create the structure of neighbours by giving them coordinates
                      (x-1,y+1), (x,y+1), (x+1,y+1)] 
        neighbours = [i + j*n for i, j in neighbours 
        if 0<=i<n and 0<=j<n] # preventing the coordinates from going out of bounds

        self.neighbours = neighbours 

        self.area = (x >= n/2) + 2 * (y >= n/2) # we define the area of the city (0,1,2,3)

        min, max = self.city.area_rates[self.area] # we separate the contraint in min and max of the area
        self.rate = rd.randint(min, max)  # we can use uniform to get a float value

        self.price = {0: 900*self.rate} # set the stating steps(keys) and price(values)

        return self.neighbours, self.area, self.rate, self.price

    def update_occupancy(self):
        
        # Calculate the average rate of all areas in the city
        avg_area_rates = sum([(min_val+max_val)/2 for min_val, max_val in self.city.area_rates.values()]) / len(self.city.area_rates) 

        # Determine occupancy based on the listing's rate compared to the average
        if self.rate > avg_area_rates:    
            # If rate is higher than average, occupancy is lower (5 to 15 days)
            self.occupancy = rd.randint(5,15)
        else:
            # If rate is lower/equal, occupancy is higher (10 to 20 days)
            self.occupancy = rd.randint(10,20) 

        return self.occupancy


        







        
