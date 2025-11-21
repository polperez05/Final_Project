import sys
import os
import random as rd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # Import necesario para la leyenda

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from final_project.city import City

def main():
    # --- CONFIGURATION ---
    SIZE = 10
    STEPS = 180
    AREA_RATES = {
        0: (100, 200), 
        1: (50, 250), 
        2: (250, 350), 
        3: (150, 450)
    }

    rd.seed(42) 

    # --- INITIALIZATION ---
    print(f"Initializing city of size {SIZE}x{SIZE}...")
    city = City(size=SIZE, area_rates=AREA_RATES)
    city.initialize()

    history_avg_prices = []
    history_steps = []

    # --- SIMULATION LOOP ---
    print(f"Starting simulation for {STEPS} monthly steps...")
    
    for step in range(STEPS):
        city.iterate()

        # Data for Graph 2
        total_price = 0
        for place in city.places:
            current_price = list(place.price.values())[-1]
            total_price += current_price
        
        avg_price = total_price / len(city.places)
        history_avg_prices.append(avg_price)
        history_steps.append(step)

    print("Simulation finished.")

    # --- DATA ANALYSIS FOR GRAPH 1 ---
    hosts_data = []
    for host in city.hosts:
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

    # Ordenar de menor a mayor riqueza
    hosts_data.sort(key=lambda x: x['wealth'])

    # --- PLOTTING ---
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # === GRAPH 1: Wealth Distribution ===
    print("Generating graph1.png...")
    
    ids = [str(d['host_id']) for d in hosts_data]
    wealths = [d['wealth'] for d in hosts_data]
    areas = [d['area'] for d in hosts_data]
    
    # Mapa de colores
    colors_map = {0: 'red', 1: 'blue', 2: 'green', 3: 'orange'}
    bar_colors = [colors_map[a] for a in areas]

    plt.figure(figsize=(12, 6))
    
    plt.bar(ids, wealths, color=bar_colors)
    plt.yscale('log') 
    plt.xlabel('Host ID (Sorted by Wealth)')
    plt.ylabel('Total Wealth (Log Scale)')
    plt.title('Final Wealth of Hosts by Area')
    
    # Legend
    
    legend_handles = [
        mpatches.Patch(color='red', label='Area 0 (Low)'),
        mpatches.Patch(color='blue', label='Area 1 (Mid-Low)'),
        mpatches.Patch(color='green', label='Area 2 (Mid-High)'),
        mpatches.Patch(color='orange', label='Area 3 (High)')
    ]
    plt.legend(handles=legend_handles, title="City Areas")
    
    plt.xticks([]) # Ocultamos los números del eje X para que quede limpio
    
    plt.savefig('reports/graph1.png')
    plt.close()

    # === GRAPH 2: Average Price Evolution ===
    print("Generating graph2_v0.png...")
    plt.figure(figsize=(10, 6))
    plt.plot(history_steps, history_avg_prices, color='purple', linewidth=2)
    plt.xlabel('Simulation Step (Month)')
    plt.ylabel('Average Listing Price')
    plt.title('Evolution of Average Property Prices Over Time')
    plt.grid(True)
    plt.savefig('reports/graph2_v0.png')
    plt.close()

    print("Done! Check the 'reports' folder.")

if __name__ == "__main__":
    main()
