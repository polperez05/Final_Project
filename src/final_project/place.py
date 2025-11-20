import random as rd
class Place:
    def __init__(self, place_id, host_id, city): 
        self.place_id = place_id 
        self.host_id = host_id 
        self.city = city 
    
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

    def update_occupancy(self,area, occupancy, area_rates, rates):
        self.occupancy = 0
        avg_area_rates = sum([(min+max)/2 for min, max in self.city.area_rates]) / len(self.city.area_rates) # we calculate the average rate of all the area

        if self.rate > avg_area_rates:    # in case the rate of the place is higher than the average rate of all the area it will generetate between 5 and 15 days of occupancy
            self.occupancy = rd.randint(5,15)

        else:
            self.occupancy = rd.randint(10,20) # else it will generate between 10 and 20 days of occupancy

        return self.occupancy


        







        
