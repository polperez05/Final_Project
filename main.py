import sys
import os
import random as rd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from final_project.city import City

def run_simulation(rule_version):
    """
    Runs a full simulation with the specified rule version.
    Returns the city object, the steps list, and the price history.
    """
    # Configuration
    SIZE = 10
    STEPS = 180
    AREA_RATES = {0: (100, 200), 1: (50, 250), 2: (250, 350), 3: (150, 450)}

    # Reset seed for fair comparison
    rd.seed(42) 

    print(f"Initializing city (Rule Version {rule_version})...")
    # We pass the rule_version to the City class
    city = City(size=SIZE, area_rates=AREA_RATES, rule_version=rule_version)
    city.initialize()

    history_avg_prices = []
    history_steps = []

    print(f"Running {STEPS} steps...")
    for step in range(STEPS):
        city.iterate()

        # Collect data for Price Graph
        total_price = 0
        for place in city.places:
            current_price = list(place.price.values())[-1]
            total_price += current_price
        
        avg_price = total_price / len(city.places)
        history_avg_prices.append(avg_price)
        history_steps.append(step)
    
    return city, history_steps, history_avg_prices

def main():
    # Create reports folder if needed
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Version 0: Host bid all their profits
    
    print("\n--- SCENARIO 0: Original Rules ---")
    city_v0, steps_v0, prices_v0 = run_simulation(rule_version=0)

    # --- GRAPH 1: Wealth Distribution (from v0) ---
    print("Generating graph1.png...")
    hosts_data = []
    for host in city_v0.hosts:
        properties_value = 0
        for place_id in host.assets:
            place = city_v0.places[place_id]
            current_price = list(place.price.values())[-1]
            properties_value += current_price
        
        total_wealth = host.profits + properties_value
        hosts_data.append({'host_id': host.host_id, 'wealth': total_wealth, 'area': host.area})

    hosts_data.sort(key=lambda x: x['wealth'])

    ids = [str(d['host_id']) for d in hosts_data]
    wealths = [d['wealth'] for d in hosts_data]
    areas = [d['area'] for d in hosts_data]
    colors_map = {0: 'red', 1: 'blue', 2: 'green', 3: 'orange'}
    bar_colors = [colors_map[a] for a in areas]

    plt.figure(figsize=(12, 6))
    # Width 0.8 for space between bars
    plt.bar(ids, wealths, color=bar_colors, width=0.8)
    # Remove extra margins
    plt.xlim(-0.6, len(ids) - 0.4)
    # Log scale to see everyone
    plt.yscale('log')
    
    plt.xlabel('Host ID (Sorted by Wealth)')
    plt.ylabel('Total Wealth (Log Scale)')
    plt.title('Final Wealth of Hosts by Area (Original Rules)')

    legend_handles = [
        mpatches.Patch(color='red', label='Area 0'),
        mpatches.Patch(color='blue', label='Area 1'),
        mpatches.Patch(color='green', label='Area 2'),
        mpatches.Patch(color='orange', label='Area 3')
    ]
    plt.legend(handles=legend_handles, title="City Areas")
    plt.xticks([])
    plt.savefig('reports/graph1.png')
    plt.close()

    # --- GRAPH 2 v0: Price Evolution ---
    print("Generating graph2_v0.png...")
    plt.figure(figsize=(10, 6))
    plt.plot(steps_v0, prices_v0, color='purple', linewidth=2)
    plt.xlabel('Simulation Step (Month)')
    plt.ylabel('Average Listing Price')
    plt.title('Evolution of Prices (Version 0: Host bid all their profits)')
    plt.grid(True)
    plt.savefig('reports/graph2_v0.png')
    plt.close()

    # Version 1: Modified Rules (Bid = Asking price + 10%)

    print("\n--- SCENARIO 1: Modified Rules (+10% Bid) ---")
    city_v1, steps_v1, prices_v1 = run_simulation(rule_version=1)

    # --- GRAPH 2 v1: Price Evolution ---
    print("Generating graph2_v1.png...")
    plt.figure(figsize=(10, 6))
    plt.plot(steps_v1, prices_v1, color='green', linewidth=2)
    plt.xlabel('Simulation Step (Month)')
    plt.ylabel('Average Listing Price')
    plt.title('Evolution of Prices (Version 1: Bid Asking + 10%)')
    plt.grid(True)
    plt.savefig('reports/graph2_v1.png')
    plt.close()

    print("\nDone! Check the reports folder.")

if __name__ == "__main__":
    main()
