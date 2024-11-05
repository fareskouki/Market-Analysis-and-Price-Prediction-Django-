import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Load Data Function
def load_data(climate_file, demand_supply_price_file, new_data_file):
    # Load the climate data and keep only the relevant columns
    climate_df = pd.read_excel(climate_file, usecols=['Year', 'TMM', 'TNM'])
    
    # Load the demand/supply price data
    demand_supply_price_df = pd.read_excel(demand_supply_price_file)
    
    # Load the new data
    new_data_df = pd.read_excel(new_data_file)

    # Clean column names
    climate_df = clean_column_names(climate_df)
    demand_supply_price_df = clean_column_names(demand_supply_price_df)
    new_data_df = clean_column_names(new_data_df)

    # Print column names to check for 'Year'
    print("Climate Data Columns:", climate_df.columns)
    print("Demand/Supply Price Data Columns:", demand_supply_price_df.columns)
    print("New Data Columns:", new_data_df.columns)

    # Ensure 'Year' columns are integers, handling any potential extra spaces
    for df in [climate_df, demand_supply_price_df]:
        if 'Year' in df.columns:
            df['Year'] = df['Year'].astype(int)

    return climate_df, demand_supply_price_df, new_data_df

# Clean column names
def clean_column_names(df):
    df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace
    return df

# Clean Numerical Column Function
def clean_numerical_column(df, column_name):
    # Ensure the column is treated as string, handle NaNs
    df[column_name] = df[column_name].astype(str).str.replace(',', '', regex=False)
    
    # Convert to numeric, forcing errors to NaN
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    # Check if conversion was successful
    if df[column_name].isnull().any():
        print(f"Warning: There are NaN values in the {column_name} column after conversion.")

    return df

# Prepare Data Function
def prepare_data(climate_df, demand_supply_price_df):
    # Merge all DataFrames based on Year
    merged_df = demand_supply_price_df.merge(climate_df, on='Year', how='left')
    print(f"After merging demand_supply_price and climate: {merged_df.shape}")  # Check shape
    
    # Print the merged DataFrame to inspect its content
    print("Merged DataFrame Head:\n", merged_df.head())  # Inspect the first few rows of the merged DataFrame

    # Drop rows with NaN values if any
    merged_df.dropna(inplace=True)
    print(f"After dropping NaN values: {merged_df.shape}")  # Check shape

    # Clean the 'Price per ton (TND)' column
    merged_df = clean_numerical_column(merged_df, 'Price per ton (TND)')

    # Check data types
    print("Data Types:\n", merged_df.dtypes)

    return merged_df

# EDA Function
def perform_eda(data):
    # Group by 'Year' and calculate average TMM
    yearly_tmm = data.groupby('Year')['TMM'].mean().reset_index()

    # Plot the line graph for average TMM per year
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=yearly_tmm, x='Year', y='TMM', marker='o')
    plt.title('Évolution de la Température Moyenne (TMM) par Année')
    plt.xlabel('Année')
    plt.ylabel('Température Moyenne (TMM)')
    plt.xticks(rotation=45)  # Rotate x-ticks for better readability
    plt.grid()
    plt.show()

    # Group by 'Year' and calculate average TMM and production
    yearly_data = data.groupby('Year').agg(
        average_tmm=('TMM', 'mean'),
        total_production=('Price per ton (TND)', 'sum')  # Replace with the correct column for production
    ).reset_index()

    # Plot temperature vs. production
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=yearly_data, x='average_tmm', y='total_production', alpha=0.7)
    sns.regplot(data=yearly_data, x='average_tmm', y='total_production', scatter=False, color='red')
    plt.title('Relation entre Température Moyenne (TMM) et Production')
    plt.xlabel('Température Moyenne (TMM)')
    plt.ylabel('Production Totale')
    plt.grid()
    plt.show()

    # Scatter plot of Temperature vs. Price
    temperature_column = 'TMM'  # Change this to a single string
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x=temperature_column, y='Price per ton (TND)', alpha=0.7)
    sns.regplot(data=data, x=temperature_column, y='Price per ton (TND)', scatter=False, color='red')
    plt.title(f'Price vs. Temperature ({temperature_column})')
    plt.xlabel(temperature_column)  # Corrected this to use temperature_column
    plt.ylabel('Price per ton (TND)')
    plt.grid()
    plt.show()

    # Group by Year to analyze average price and temperature
    yearly_data_price_temp = data.groupby('Year').agg(
        average_price=('Price per ton (TND)', 'mean'),
        average_TMM=('TMM', 'mean'),
        average_TNM=('TNM', 'mean')
    ).reset_index()

    # Plot yearly average price vs. average temperature
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=yearly_data_price_temp, x='Year', y='average_price', label='Average Price', marker='o')
    plt.title('Yearly Average Price')
    plt.xlabel('Year')
    plt.ylabel('Average Price (TND)')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()

# Build Model Function
def build_model(data):
    # Prepare feature matrix (X) and target vector (y)
    feature_columns = ['TMM', 'TNM']
    X = data[feature_columns]
    y = data['Price per ton (TND)']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and fit the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    print(f'R² Score: {r2}')

    return model

# Main Execution
if __name__ == "__main__":
    project_dir = os.getcwd()  # Change this if your project directory is different

    # Correct file paths
    climate_file_path = os.path.join(project_dir, 'normales_1981_2010.xlsx')
    demand_supply_price_file_path = os.path.join(project_dir, 'demand_supply_price.csv.xlsx')  # Ensure this is the correct path
    new_data_file_path = os.path.join(project_dir, 'agriculture_data_with_olive_and_dattes.xlsx')

    # Load the data
    climate_df, demand_supply_price_df, new_data_df = load_data(
        climate_file_path,
        demand_supply_price_file_path,
        new_data_file_path
    )

    # Prepare the data
    prepared_data = prepare_data(climate_df, demand_supply_price_df)

    # Perform EDA
    perform_eda(prepared_data)

    # Build and evaluate the model
    model = build_model(prepared_data)

    # Future Predictions
    future_data = pd.DataFrame({
        'TMM': [20, 22, 24],  # Average temperature for future years
        'TNM': [15, 17, 19]
    })

    future_predictions = model.predict(future_data)
    print("Future Predictions (Price per ton):", future_predictions)
