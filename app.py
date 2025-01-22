import random  # For generating random water loss values
import numpy as np  # For numerical operations
from sklearn.linear_model import LinearRegression  # For predictive modeling
import matplotlib.pyplot as plt  # For data visualization
from rich.console import Console  # For styled terminal output
from rich.table import Table  # For tabular data in terminal
from rich.panel import Panel  # For styled panels in terminal
import os  # For file system operations

# Initialize rich console for styled terminal output
console = Console()

# Mock data for demonstration
historical_data = {  # Historical crop yield and water use data
    "wheat": {"yield": [300, 320, 290], "water_use": [400, 380, 410]},
    "corn": {"yield": [500, 520, 480], "water_use": [600, 590, 620]},
}

regional_data = {  # Regional rainfall and climate data
    "north": {"rainfall": 1000, "climate": "temperate"},
    "south": {"rainfall": 500, "climate": "arid"},
    "east": {"rainfall": 800, "climate": "humid"},
    "west": {"rainfall": 600, "climate": "semi-arid"},
}

# Create directory for static visualizations
if not os.path.exists("terminal_visuals"):
    os.makedirs("terminal_visuals")


def crop_efficiency():
    """Custom Crop Efficiency Planner"""
    console.print(Panel("Custom Crop Efficiency Planner", style="bold blue"))
    crop_type = console.input("[bold green]Enter crop type (e.g., wheat, corn): [/]")
    soil_quality = int(console.input("[bold green]Enter soil quality (1-100): [/]"))
    farm_size = float(console.input("[bold green]Enter farm size (in acres): [/]"))
    
    # Check if crop type exists
    if crop_type not in historical_data:
        console.print(f"[red]Error: Crop type '{crop_type}' not found![/]")
        return

    # Predict future yield using Linear Regression
    past_yield = historical_data[crop_type]["yield"]
    X = np.array(range(len(past_yield))).reshape(-1, 1)
    y = np.array(past_yield)
    model = LinearRegression()
    model.fit(X, y)
    future_yield = model.predict([[len(past_yield)]])[0] + soil_quality * 0.05

    # Output results
    console.print(f"[bold cyan]Optimized Planting Layout: [/bold cyan]{farm_size} acres of {crop_type}")
    console.print(f"[bold cyan]Predictive Yield: [/bold cyan]{round(future_yield, 2)} units")


def water_management():
    """Water Management Tool"""
    console.print(Panel("Water Management Tool", style="bold blue"))
    irrigation_method = console.input("[bold green]Enter irrigation method (e.g., drip, sprinkler): [/]")
    soil_type = console.input("[bold green]Enter soil type (e.g., clay, loam, sandy): [/]")
    region = console.input("[bold green]Enter region (north, south, east, west): [/]")
    
    # Validate region
    if region not in regional_data:
        console.print(f"[red]Error: Region '{region}' not found![/]")
        return

    # Simulate water loss and visualize data
    water_loss = random.uniform(10, 30)  # Random water loss value
    rainfall = regional_data[region]["rainfall"]

    plt.figure(figsize=(8, 5))
    plt.bar(["Rainfall", "Water Loss"], [rainfall, water_loss], color=["blue", "red"])
    plt.title("Water Usage Simulation")
    plt.ylabel("Water (mm)")
    visualization_path = f"terminal_visuals/{region}_water_simulation.png"
    plt.savefig(visualization_path)
    plt.close()

    # Display results
    console.print(f"[bold cyan]Water Loss: [/bold cyan]{round(water_loss, 2)} mm")
    console.print(f"[bold cyan]Visualization saved to: [/bold cyan]{visualization_path}")
    console.print("[bold cyan]Suggestions:[/bold cyan]")
    console.print("- Use drip irrigation to reduce water waste.")
    console.print("- Mulch soil to retain moisture.")
    console.print("- Harvest rainwater for irrigation.")


def localized_water_data():
    """Localized Water Data"""
    console.print(Panel("Localized Water Data", style="bold blue"))
    region = console.input("[bold green]Enter region (north, south, east, west): [/]")
    
    # Check if region exists
    if region not in regional_data:
        console.print(f"[red]Error: Region '{region}' not found![/]")
        return

    region_info = regional_data[region]
    console.print(f"[bold cyan]Region: [/bold cyan]{region}")
    console.print(f"[bold cyan]Rainfall: [/bold cyan]{region_info['rainfall']} mm")
    console.print(f"[bold cyan]Climate: [/bold cyan]{region_info['climate']}")
    console.print("[bold cyan]Suggestions:[/bold cyan]")
    console.print("- Harvest rainwater for irrigation.")
    console.print("- Use conservation techniques for soil moisture retention.")


def eco_tips():
    """Eco-Tips Section"""
    console.print(Panel("Eco-Tips Section", style="bold blue"))
    tips = [
        "Compost organic waste to improve soil health.",
        "Practice crop rotation to reduce pests.",
        "Adopt renewable energy sources for irrigation.",
        "Minimize tilling to maintain soil structure.",
    ]
    table = Table(title="Eco-Tips", show_header=True, header_style="bold magenta")
    table.add_column("Tip No.")
    table.add_column("Suggestion")
    for idx, tip in enumerate(tips, start=1):
        table.add_row(str(idx), tip)
    console.print(table)


def main():
    """Main Menu"""
    while True:
        console.print(Panel("Sustainable Agriculture Optimization Platform", style="bold green"))
        console.print("[1] Custom Crop Efficiency Planner")
        console.print("[2] Water Management Tool")
        console.print("[3] Localized Water Data")
        console.print("[4] Eco-Tips Section")
        console.print("[5] Exit")
        
        choice = console.input("[bold yellow]Enter your choice: [/]")
        if choice == "1":
            crop_efficiency()
        elif choice == "2":
            water_management()
        elif choice == "3":
            localized_water_data()
        elif choice == "4":
            eco_tips()
        elif choice == "5":
            console.print("[bold red]Exiting... Goodbye![/]")
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/]")


if __name__ == "__main__":
    main()
