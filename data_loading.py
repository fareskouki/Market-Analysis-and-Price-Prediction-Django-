import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

def load_data(production_path, climate_path, demand_supply_price_path, new_data_path):
    # Load production data
    production_df = pd.read_csv(production_path, sep=';', encoding='latin1')
    production_df.columns = production_df.columns.str.strip()

    # Ensure the 'Year' column exists and is in datetime format
    if 'Year' not in production_df.columns:
        raise KeyError("'Year' column not found in production DataFrame")
    production_df['Year'] = pd.to_datetime(production_df['Year'], format='%Y').dt.year

    # Load climate data
    if not os.path.isfile(climate_path):
        raise FileNotFoundError(f"The file '{climate_path}' does not exist.")
    climate_df = pd.read_excel(climate_path)

    # Print climate data to debug
    print("Climate Data Head:\n", climate_df.head())
    print("Unique Years in Climate Data:", climate_df['Year'].unique())

    # Ensure the Year column is an integer
    climate_df['Year'] = pd.to_numeric(climate_df['Year'], errors='coerce')
    print("Parsed Years in Climate Data:", climate_df['Year'].unique())
    print("Missing Year Values in Climate Data:", climate_df['Year'].isnull().sum())

    # Load demand, supply, and price data
    demand_supply_price_df = pd.read_excel(demand_supply_price_path)
    demand_supply_price_df = demand_supply_price_df[demand_supply_price_df['Produit'] == 'potatoes']
    for col in ['Production (Supply, liters)', 'Exports (Demand, liters)', 'Price per ton (TND)']:
        demand_supply_price_df[col] = pd.to_numeric(
            demand_supply_price_df[col].astype(str).str.replace(',', '').str.strip(),
            errors='coerce'
        )
    mean_values = demand_supply_price_df[['Production (Supply, liters)', 'Exports (Demand, liters)', 'Price per ton (TND)']].mean()
    demand_supply_price_df.fillna(mean_values, inplace=True)

    # Load new data
    if not os.path.isfile(new_data_path):
        raise FileNotFoundError(f"The file '{new_data_path}' does not exist.")
    new_data_df = pd.read_excel(new_data_path)
    new_data_df['Year'] = pd.to_numeric(new_data_df['Year'], errors='coerce')
    new_data_df.columns = new_data_df.columns.str.strip()
    new_data_df['Price'] = pd.to_numeric(
        new_data_df['Production Price (DT/qx)'].astype(str).str.replace(',', '').str.strip(),
        errors='coerce'
    )

    combined_df = pd.concat(
        [demand_supply_price_df,
         new_data_df[['Year', 'Price']].rename(columns={'Price': 'Price per ton (TND)'})],
        ignore_index=True
    )
    combined_df['Price per ton (TND)'] = combined_df['Price per ton (TND)'].ffill()
    
    return production_df, climate_df, combined_df

def visualize_production(production_df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=production_df, x='Year', y='Production', hue='Gouvernorat', marker='o')
    plt.title('Potato Production Over Years by Gouvernorat')
    plt.xlabel('Year')
    plt.ylabel('Production (Tonnes)')
    plt.xticks(rotation=45)
    plt.legend(title='Gouvernorat', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def visualize_climate_and_production(climate_df, production_df):
    # Ensure Year columns are correctly formatted
    climate_df['Year'] = pd.to_numeric(climate_df['Year'], errors='coerce')
    production_df['Year'] = pd.to_numeric(production_df['Year'], errors='coerce')

    # Check unique years before filtering
    print("Unique Years in Climate Data (before filtering):", climate_df['Year'].unique())
    print("Unique Years in Production Data (before filtering):", production_df['Year'].unique())

    # Merge climate and production data on Year
    climate_production_df = pd.merge(
        climate_df[['Year', 'TMM', 'TXM', 'TNM']],
        production_df[['Year', 'Production']],
        on='Year',
        how='inner'
    )

    # Check if the merged dataframe has data
    if climate_production_df.empty:
        print("No data available for the selected years after merging.")
        return

    print(climate_production_df.head())  # Display the merged DataFrame

    plt.figure(figsize=(12, 6))
    
    # Create a line plot for production
    sns.lineplot(data=climate_production_df, x='Year', y='Production', label='Production', color='blue')

    # Create a secondary y-axis for temperature
    ax2 = plt.gca().twinx()
    sns.lineplot(data=climate_production_df, x='Year', y='TXM', label='Max Temperature (TXM)', color='orange', ax=ax2)  # Change to curve
    ax2.set_ylabel('Temperature (°C)')  # Set y-axis label for temperature
    ax2.legend(loc='upper right')

    plt.title('Climate and Production Over Years')
    plt.xlabel('Year')
    plt.ylabel('Production (Tonnes)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def visualize_demand_supply_price(demand_supply_price_df):
    plt.figure(figsize=(14, 7))
    # Filter to start from the year 2000
    demand_supply_price_df = demand_supply_price_df[demand_supply_price_df['Year'] >= 2000]

    # Create a line plot for production
    sns.lineplot(data=demand_supply_price_df, x='Year', y='Production (Supply, liters)', label='Production', marker='o')
    # Create a line plot for demand
    sns.lineplot(data=demand_supply_price_df, x='Year', y='Exports (Demand, liters)', label='Demand', marker='o')

    # Create a secondary y-axis for price
    ax2 = plt.gca().twinx()
    
    # Use lineplot with a smooth curve for price
    sns.lineplot(data=demand_supply_price_df, x='Year', y='Price per ton (TND)', label='Price', color='red', ax=ax2)

    ax2.set_ylabel('Price per ton (TND)')  # Set y-axis label for price
    ax2.legend(loc='upper right')

    plt.title('Development of Production, Demand, and Price Over Years')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def make_price_prediction(demand_supply_price_df):
    X = demand_supply_price_df[['Year']]
    y = demand_supply_price_df['Price per ton (TND)']
    
    # Remove rows with missing values
    combined_df = pd.concat([X, y], axis=1).dropna()
    X = combined_df[['Year']]
    y = combined_df['Price per ton (TND)']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    xgb_model = XGBRegressor()
    xgb_model.fit(X_train, y_train)

    future_years = pd.DataFrame({'Year': pd.date_range(start='2024', periods=5, freq='Y').year})
    
    linear_predictions = linear_model.predict(future_years)
    xgb_predictions = xgb_model.predict(future_years)

    print("Linear Regression Predictions:")
    for year, price in zip(future_years['Year'], linear_predictions):
        print(f"Year {year}: Predicted Price = {price:.2f} Mil.TND")
        
    print("\nXGBoost Predictions:")
    for year, price in zip(future_years['Year'], xgb_predictions):
        print(f"Year {year}: Predicted Price = {price:.2f} Mil.TND")

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    production_file_path = os.path.join(project_dir, 'evolution_de_production_de_pommes_de_terre_de_saison_en_tonnes_.csv')
    climate_file_path = os.path.join(project_dir, 'normales_1981_2010.xlsx')
    demand_supply_price_file_path = os.path.join(project_dir, 'demand_supply_price.csv.xlsx')
    new_data_file_path = os.path.join(project_dir, 'agriculture_data_with_olive_and_dattes.xlsx')

    try:
        production_df, climate_df, combined_df = load_data(
            production_file_path,
            climate_file_path,
            demand_supply_price_file_path,
            new_data_file_path
        )
        visualize_production(production_df)
        visualize_climate_and_production(climate_df, production_df)
        visualize_demand_supply_price(combined_df)
        make_price_prediction(combined_df)
    except Exception as e:
        print(f"An error occurred: {e}")
