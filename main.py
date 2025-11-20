import matplotlib.pyplot as plt
import os
import random as rd

# Import the classes we created
# Note: Ensure these files are in the same directory or properly installed as a package
from final_project.city import City

def main():
    # --- CONFIGURATION ---
    # As defined in the PDF instructions [cite: 73, 76]
    SIZE = 10
    STEPS = 180
    # Rates for each area: 0, 1, 2, 3
    AREA_RATES = {
        0: (100, 200), 
        1: (50, 250), 
        2: (250, 350), 
        3: (150, 450)
    }

    # Ensure reproducibility [cite: 75]
    rd.seed(42) 

    # --- INITIALIZATION ---
    print(f"Initializing city of size {SIZE}x{SIZE}...")
    city = City(size=SIZE, area_rates=AREA_RATES)
    city.initialize()

    # Lists to store data for Graph 2 (Average Price over time)
    history_avg_prices = []
    history_steps = []

    # --- SIMULATION LOOP ---
    print(f"Starting simulation for {STEPS} monthly steps...")
    
    for step in range(STEPS):
        # Advance the city one step
        city.iterate()

        # --- DATA COLLECTION FOR GRAPH 2 ---
        # Calculate the average price of all properties in this step
        total_price = 0
        for place in city.places:
            # We get the current price. 
            # place.price is a dictionary {step: price}, we need the latest value.
            current_price = list(place.price.values())[-1]
            total_price += current_price
        
        avg_price = total_price / len(city.places)
        
        history_avg_prices.append(avg_price)
        history_steps.append(step)

    print("Simulation finished.")

    # --- DATA ANALYSIS FOR GRAPH 1 (WEALTH) ---
    # [cite: 76] Wealth = current profits + most recent sale price of all properties owned
    
    hosts_data = []

    for host in city.hosts:
        # Calculate property value
        properties_value = 0
        for place_id in host.assets:
            place = city.places[place_id]
            current_price = list(place.price.values())[-1]
            properties_value += current_price
        
        total_wealth = host.profits + properties_value
        
        hosts_data.append({
            'host_id': host.host_id,
            'wealth': total_wealth,
            'area': host.area
        })

    # Sort hosts by wealth (smallest to largest) [cite: 81]
    hosts_data.sort(key=lambda x: x['wealth'])

    # --- PLOTTING ---
    
    # Create the 'reports' folder if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # === GRAPH 1: Wealth Distribution ===
    print("Generating graph1.png...")
    
    ids = [str(d['host_id']) for d in hosts_data]
    wealths = [d['wealth'] for d in hosts_data]
    areas = [d['area'] for d in hosts_data]
    
    # Define colors for areas 0, 1, 2, 3
    colors_map = {0: 'red', 1: 'blue', 2: 'green', 3: 'orange'}
    bar_colors = [colors_map[a] for a in areas]

    plt.figure(figsize=(12, 6))
    # Create vertical bar chart [cite: 77]
    plt.bar(ids, wealths, color=bar_colors)
    
    plt.xlabel('Host ID (Sorted by Wealth)')
    plt.ylabel('Total Wealth')
    plt.title('Final Wealth of Hosts by Area')
    
    # We hide the x-ticks because 100 IDs are too many to read
    plt.xticks([]) 
    
    plt.savefig('reports/graph1.png')
    plt.close()

    # === GRAPH 2: Average Price Evolution ===
    # [cite: 82] Interesting aspect: How prices evolve over time
    print("Generating graph2_v0.png...")

    plt.figure(figsize=(10, 6))
    plt.plot(history_steps, history_avg_prices, color='purple', linewidth=2)
    
    plt.xlabel('Simulation Step (Months)')
    plt.ylabel('Average Listing Price')
    plt.title('Evolution of Average Property Prices Over Time')
    plt.grid(True)
    
    plt.savefig('reports/graph2_v0.png')
    plt.close()

    print("Done!")

if __name__ == "__main__":
    main()
