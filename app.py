import random  # Used to generate random values (e.g., simulating water loss)
import numpy as np  # For numerical operations and array handling
import pandas as pd  # For managing tabular data (e.g., historical records)
from sklearn.linear_model import LinearRegression  # For creating our prediction model
from sklearn.metrics import mean_squared_error  # To evaluate prediction accuracy (error calculation)
import matplotlib.pyplot as plt  # For plotting graphs and visualizations
import seaborn as sns  # For creating attractive statistical graphics
from rich.console import Console  # For enhanced and styled console output
from rich.table import Table  # To display data in nicely formatted tables in the console
from rich.panel import Panel  # For showing information in panels
import os  # For file system operations (e.g., creating directories)

# Starting the terminal output
console = Console()

# Historical Data Section
# This is environmental details.


historical_data = {
    "wheat": {
        "yield": [300, 320, 290, 310, 315],
        "water_use": [400, 380, 410, 395, 405],
        "fertilizer": [50, 55, 48, 53, 54],
    },
    "corn": {
        "yield": [500, 520, 480, 510, 505],
        "water_use": [600, 590, 620, 605, 615],
        "fertilizer": [70, 75, 68, 72, 74],
    },
    "soy": {
        "yield": [250, 265, 240, 255, 260],
        "water_use": [350, 340, 360, 355, 345],
        "fertilizer": [40, 42, 38, 41, 39],
    },
    "rice": {
        "yield": [400, 420, 390, 410, 405],
        "water_use": [500, 490, 510, 505, 495],
        "fertilizer": [60, 65, 58, 62, 63],
    },
}

regional_data = {
    "north": {
        "rainfall": 1000,
        "climate": "temperate",
        "avg_temp": 15,
        "seasonal_variation": [200, 300, 250, 250]
    },
    "south": {
        "rainfall": 500,
        "climate": "arid",
        "avg_temp": 28,
        "seasonal_variation": [100, 120, 130, 150]
    },
    "east": {
        "rainfall": 800,
        "climate": "humid",
        "avg_temp": 20,
        "seasonal_variation": [210, 220, 190, 180]
    },
    "west": {
        "rainfall": 600,
        "climate": "semi-arid",
        "avg_temp": 22,
        "seasonal_variation": [150, 160, 145, 145]
    },
}

# Directory for static visualizations (graphs will be saved here)
visuals_dir = "terminal_visuals"
if not os.path.exists(visuals_dir):
    os.makedirs(visuals_dir)

# Feature 1: Crop Efficiency Planner

def crop_efficiency():
    console.print(Panel("[bold blue]Advanced Crop Efficiency Planner[/bold blue]"))
    crop_type = console.input("[bold green]Enter crop type (e.g., wheat, corn, soy, rice) [What crop are you planning?]: [/]")
    try:
        soil_quality = int(console.input("[bold green]Enter soil quality (1-100) [Higher = better soil]: [/]"))
        farm_size = float(console.input("[bold green]Enter farm size (in acres) [Total area for the crop]: [/]"))
        fertilizer_level = float(console.input("[bold green]Enter additional fertilizer amount (kg/acre) [Extra fertilizer to boost yield]: [/]"))
        irrigation_eff = float(console.input("[bold green]Enter irrigation efficiency (0.5-1.0) [0.5 = low efficiency, 1.0 = high efficiency]: [/]"))
    except ValueError:
        console.print("[red]Invalid input. Please enter numeric values.[/]")
        return

    if crop_type not in historical_data:
        console.print(f"[red]Error: Crop type '{crop_type}' not found! Available: {', '.join(historical_data.keys())}[/]")
        return

    crop_hist = historical_data[crop_type]
    df = pd.DataFrame({
        "yield": crop_hist["yield"],
        "water_use": crop_hist["water_use"],
        "fertilizer": crop_hist["fertilizer"],
    })

    X = df[["water_use", "fertilizer"]].values
    X = np.hstack([X, np.full((X.shape[0], 1), soil_quality * 0.1)])
    y = np.array(df["yield"])

    model = LinearRegression()
    model.fit(X, y)

    avg_water = np.mean(crop_hist["water_use"]) * (1 - (1 - irrigation_eff) * 0.02)
    avg_fert = np.mean(crop_hist["fertilizer"]) + fertilizer_level
    features = np.array([[avg_water, avg_fert, soil_quality * 0.1]])

    predicted_yield = model.predict(features)[0]
    rmse = np.sqrt(mean_squared_error(y, model.predict(X)))
    conf_interval = (predicted_yield - 1.96 * rmse, predicted_yield + 1.96 * rmse)

    console.print(f"[bold cyan]Optimized Planting Layout:[/bold cyan] {farm_size:.2f} acres of {crop_type}")
    console.print(f"[bold cyan]Predicted Yield:[/bold cyan] {predicted_yield:.2f} units")
    console.print(f"[bold cyan]95% Confidence Interval:[/bold cyan] ({conf_interval[0]:.2f}, {conf_interval[1]:.2f})")
    console.print("[bold magenta]Recommendations:[/bold magenta]")
    console.print("- Adjust fertilizer input as per soil nutrient testing.")
    console.print("- Consider micro-irrigation to boost water efficiency.")
    console.print("- Regularly update historical data for better predictions.")


# Feature 2: Water Management Tool

def water_management():
    console.print(Panel("[bold blue]Enhanced Water Management Tool[/bold blue]"))
    irrigation_method = console.input("[bold green]Enter irrigation method (e.g., drip, sprinkler) [Determines water distribution efficiency]: [/]")
    soil_type = console.input("[bold green]Enter soil type (e.g., clay, loam, sandy) [Influences water infiltration]: [/]")
    region = console.input("[bold green]Enter region (north, south, east, west) [Select your local region]: [/]")
    
    if region not in regional_data:
        console.print(f"[red]Error: Region '{region}' not found![/]")
        return

    irrigation_efficiency_map = {"drip": 0.95, "sprinkler": 0.85}
    soil_infiltration_map = {"clay": 0.7, "loam": 0.9, "sandy": 0.8}
    
    irrigation_efficiency = irrigation_efficiency_map.get(irrigation_method.lower(), 0.80)
    soil_infiltration = soil_infiltration_map.get(soil_type.lower(), 0.75)

    months = list(range(1, 13))
    monthly_rainfall = np.array(regional_data[region]["seasonal_variation"])
    if monthly_rainfall.size < 12:
        monthly_rainfall = np.resize(monthly_rainfall, 12) + np.random.randint(-10, 10, 12)
    
    water_losses = []
    for m in months:
        base_loss = random.uniform(10, 30)
        adjusted_loss = base_loss * (1 - irrigation_efficiency) * (1 - soil_infiltration)
        water_losses.append(adjusted_loss)
    
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    plt.plot(months, monthly_rainfall, marker='o', label='Monthly Rainfall (mm)', color="blue")
    plt.plot(months, water_losses, marker='s', label='Simulated Water Loss (mm)', color="red")
    plt.title(f"Seasonal Water Usage Simulation - {region.capitalize()} Region")
    plt.xlabel("Month")
    plt.ylabel("Water (mm)")
    plt.legend()
    plt.xticks(months)
    plt.tight_layout()
    
    visualization_path = os.path.join(visuals_dir, f"{region}_water_simulation_enhanced.png")
    plt.savefig(visualization_path, dpi=150)
    plt.close()
    
    console.print(f"[bold cyan]Average Monthly Rainfall:[/bold cyan] {np.mean(monthly_rainfall):.2f} mm")
    console.print(f"[bold cyan]Average Simulated Water Loss:[/bold cyan] {np.mean(water_losses):.2f} mm")
    console.print(f"[bold cyan]Visualization saved to:[/bold cyan] {visualization_path}")
    console.print("[bold magenta]Advanced Suggestions:[/bold magenta]")
    console.print("- Consider scheduling irrigation during periods with low evaporation.")
    console.print("- Upgrade to smart irrigation systems for real-time adjustments.")
    console.print("- Use weather forecast data to further fine-tune irrigation schedules.")


# Feature 3: Localized Water Data

def localized_water_data():
    console.print(Panel("[bold blue]Enhanced Localized Water Data[/bold blue]"))
    region = console.input("[bold green]Enter region (north, south, east, west) [Select your region for local data]: [/]")
    if region not in regional_data:
        console.print(f"[red]Error: Region '{region}' not found![/]")
        return
    
    region_info = regional_data[region]
    console.print(f"[bold cyan]Region:[/bold cyan] {region.capitalize()}")
    console.print(f"[bold cyan]Annual Rainfall:[/bold cyan] {region_info['rainfall']} mm")
    console.print(f"[bold cyan]Climate:[/bold cyan] {region_info['climate'].capitalize()}")
    console.print(f"[bold cyan]Average Temperature:[/bold cyan] {region_info['avg_temp']} °C")
    
    console.print("[bold cyan]Seasonal Rainfall Distribution (mm):[/bold cyan]")
    seasons = ["Spring", "Summer", "Autumn", "Winter"]
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Season")
    table.add_column("Rainfall (mm)", justify="right")
    
    for season, rain in zip(seasons, region_info["seasonal_variation"]):
        table.add_row(season, str(rain))
    console.print(table)
    
    console.print("[bold magenta]Region-Specific Recommendations:[/bold magenta]")
    if region_info['climate'] == "arid":
        console.print("- Implement rainwater harvesting techniques.")
        console.print("- Use drought-resistant crop varieties.")
    elif region_info['climate'] in ["temperate", "humid"]:
        console.print("- Optimize water distribution with smart sensors.")
        console.print("- Enhance soil moisture retention via organic mulches.")
    else:
        console.print("- Integrate seasonal forecasting into irrigation planning.")
        console.print("- Regularly assess and adjust soil moisture retention strategies.")

# Feature 4: Eco-Tips Section


def eco_tips():
    console.print(Panel("[bold blue]Eco-Tips Section[/bold blue]"))

    
    tips = [
        {
            "category": "Soil Health",
            "tip": "Compost Organic Waste",
            "description": "Enhance soil organic matter by composting kitchen and garden waste."
        },
        {
            "category": "Soil Health",
            "tip": "Practice Crop Rotation",
            "description": "Naturally manage soil nutrients and reduce pest buildup by rotating crops each season."
        },
        {
            "category": "Water Conservation",
            "tip": "Adopt Drip Irrigation",
            "description": "Minimize water waste by delivering water directly to plant roots."
        },
        {
            "category": "Water Conservation",
            "tip": "Harvest Rainwater",
            "description": "Collect and store rainwater for irrigation to reduce dependence on external water sources."
        },
        {
            "category": "Energy Efficiency",
            "tip": "Use Solar-Powered Pumps",
            "description": "Reduce energy consumption by utilizing renewable solar energy for irrigation systems."
        },
        {
            "category": "Energy Efficiency",
            "tip": "Upgrade to LED Lighting",
            "description": "Lower energy usage and costs by switching to energy-efficient LED lighting in greenhouses."
        },
        {
            "category": "Soil Conservation",
            "tip": "Minimize Tillage",
            "description": "Maintain soil structure and reduce erosion by limiting the use of tillage equipment."
        },
        {
            "category": "Soil Conservation",
            "tip": "Utilize Cover Cropping",
            "description": "Protect the soil during off-seasons with cover crops that prevent erosion and improve soil health."
        },
        {
            "category": "Pest Management",
            "tip": "Introduce Beneficial Insects",
            "description": "Control pests naturally by attracting or introducing insects that prey on harmful pests."
        },
        {
            "category": "Pest Management",
            "tip": "Use Organic Pesticides",
            "description": "Reduce chemical usage by opting for environmentally friendly pesticide alternatives."
        },
    ]

    # Create a table with categories, tips, and descriptions
    table = Table(title="Eco-Tips", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="bold green")
    table.add_column("Tip", style="bold")
    table.add_column("Description", style="italic")

    for tip in tips:
        table.add_row(tip["category"], tip["tip"], tip["description"])

    console.print(table)



# Main Menu and Application Control

def main():
    while True:
        console.print(Panel("[bold green]Sustainable Agriculture Optimization Platform[/bold green]"))
        console.print("[1] Advanced Crop Efficiency Planner")
        console.print("[2] Enhanced Water Management Tool")
        console.print("[3] Enhanced Localized Water Data")
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
