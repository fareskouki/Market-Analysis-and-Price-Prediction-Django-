import pandas as pd

# Define the extended dataset with Huile d'olive and Dattes
data = [
    # Cereales data
    {"Year": "2020", "Product": "Blé dur", "Area (ha)": 543000, "Harvested Area (ha)": 466230, "Production (Tonnes)": 958521, "Yield (Qx/ha)": 17.6, "Production Price (DT/qx)": 82, "Collected (1000 Tonnes)": 625.97, "Import Volume (1000 Tonnes)": 653.7, "Domestic Demand (1000 Tonnes)": 823.2, "Dependence Rate (%)": 40.54},
    {"Year": "2020", "Product": "Blé tendre", "Area (ha)": 63000, "Harvested Area (ha)": 52902, "Production (Tonnes)": 84156, "Yield (Qx/ha)": 13.4, "Production Price (DT/qx)": 59, "Collected (1000 Tonnes)": 25.337, "Import Volume (1000 Tonnes)": 1195.2, "Domestic Demand (1000 Tonnes)": 1303, "Dependence Rate (%)": 93.42},
    {"Year": "2020", "Product": "Orge", "Area (ha)": 554000, "Harvested Area (ha)": 375253, "Production (Tonnes)": 465393, "Yield (Qx/ha)": 8.6, "Production Price (DT/qx)": 53, "Collected (1000 Tonnes)": 58.113, "Import Volume (1000 Tonnes)": 954.5, "Domestic Demand (1000 Tonnes)": 960, "Dependence Rate (%)": 67.22},
    {"Year": "2020", "Product": "Triticale", "Area (ha)": None, "Harvested Area (ha)": None, "Production (Tonnes)": 25969, "Yield (Qx/ha)": 22, "Production Price (DT/qx)": None, "Collected (1000 Tonnes)": None, "Import Volume (1000 Tonnes)": None, "Domestic Demand (1000 Tonnes)": None, "Dependence Rate (%)": None},
       # Potato data 
    {"Year": "2015", "Product": "Potatoes", "Area (ha)": 22900, "Production (Tonnes)": 400000, "Yield (T/ha)": 17},
    {"Year": "2016", "Product": "Potatoes", "Area (ha)": 23600, "Production (Tonnes)": 440000, "Yield (T/ha)": 19},
    {"Year": "2017", "Product": "Potatoes", "Area (ha)": 23500, "Production (Tonnes)": 420000, "Yield (T/ha)": 18},
    {"Year": "2018", "Product": "Potatoes", "Area (ha)": 22300, "Production (Tonnes)": 465000, "Yield (T/ha)": 21},
    {"Year": "2019", "Product": "Potatoes", "Area (ha)": 21380, "Production (Tonnes)": 435000, "Yield (T/ha)": 20},
    {"Year": "2020", "Product": "Potatoes", "Area (ha)": 21880, "Production (Tonnes)": 452000, "Yield (T/ha)": 21},
    # Milk data
    {"Year": "2015", "Product": "Milk", "Production (Tonnes)": 1_251_000, "Cow Productivity (Kg/cow)": 5_875, "Price (Millimes/L)": 766},
    {"Year": "2016", "Product": "Milk", "Production (Tonnes)": 1_376_000, "Cow Productivity (Kg/cow)": 5_683, "Price (Millimes/L)": 890},
    {"Year": "2017", "Product": "Milk", "Production (Tonnes)": 1_408_000, "Cow Productivity (Kg/cow)": 5_674, "Price (Millimes/L)": 945},
    {"Year": "2018", "Product": "Milk", "Production (Tonnes)": 1_424_000, "Cow Productivity (Kg/cow)": 5_952, "Price (Millimes/L)": 1_075},
    {"Year": "2019", "Product": "Milk", "Production (Tonnes)": 1_352_000, "Cow Productivity (Kg/cow)": 6_217, "Price (Millimes/L)": 1_175},
    {"Year": "2020", "Product": "Milk", "Production (Tonnes)": 1_392_000, "Cow Productivity (Kg/cow)": 5_944, "Price (Millimes/L)": 1_175},
 
    # Huile d'olive data
    {"Year": "2020", "Product": "Huile d'olive", "Area (ha)": 1877000, "Harvested Area (ha)": None, "Production (Tonnes)": 350000, "Yield (Qx/ha)": 2, "Production Price (DT/qx)": None, "Collected (1000 Tonnes)": None, "Import Volume (1000 Tonnes)": 500, "Domestic Demand (1000 Tonnes)": 150000, "Dependence Rate (%)": None},
    {"Year": "2021", "Product": "Huile d'olive", "Area (ha)": 1875000, "Harvested Area (ha)": None, "Production (Tonnes)": 240000, "Yield (Qx/ha)": 1.5, "Production Price (DT/qx)": None, "Collected (1000 Tonnes)": None, "Import Volume (1000 Tonnes)": 300, "Domestic Demand (1000 Tonnes)": 140000, "Dependence Rate (%)": None},
    
    # Dattes data
    {"Year": "2020", "Product": "Dattes", "Area (ha)": 63400, "Harvested Area (ha)": None, "Production (Tonnes)": 340000, "Yield (Qx/ha)": 53.6, "Production Price (DT/qx)": 8, "Collected (1000 Tonnes)": None, "Import Volume (1000 Tonnes)": None, "Domestic Demand (1000 Tonnes)": 65000, "Dependence Rate (%)": None},
    {"Year": "2021", "Product": "Dattes", "Area (ha)": 63400, "Harvested Area (ha)": None, "Production (Tonnes)": 320000, "Yield (Qx/ha)": 50.5, "Production Price (DT/qx)": 7.8, "Collected (1000 Tonnes)": None, "Import Volume (1000 Tonnes)": None, "Domestic Demand (1000 Tonnes)": 64000, "Dependence Rate (%)": None},

    # Meat production data
    {"Year": "2016", "Type of Meat": "Bovine", "Production (Tonnes)": 54800, "Growth Rate (%)": None},
    {"Year": "2016", "Type of Meat": "Ovine", "Production (Tonnes)": 55700, "Growth Rate (%)": None},
    {"Year": "2016", "Type of Meat": "Caprine", "Production (Tonnes)": 10700, "Growth Rate (%)": None},
    {"Year": "2017", "Type of Meat": "Bovine", "Production (Tonnes)": 56200, "Growth Rate (%)": 3.65},
    {"Year": "2017", "Type of Meat": "Ovine", "Production (Tonnes)": 55700, "Growth Rate (%)": 0.0},
    {"Year": "2017", "Type of Meat": "Caprine", "Production (Tonnes)": 10000, "Growth Rate (%)": -6.54},
    {"Year": "2018", "Type of Meat": "Bovine", "Production (Tonnes)": 60000, "Growth Rate (%)": 6.73},
    {"Year": "2018", "Type of Meat": "Ovine", "Production (Tonnes)": 57000, "Growth Rate (%)": 2.53},
    {"Year": "2018", "Type of Meat": "Caprine", "Production (Tonnes)": 9500, "Growth Rate (%)": -5.0},
    {"Year": "2019", "Type of Meat": "Bovine", "Production (Tonnes)": 61000, "Growth Rate (%)": 1.67},
    {"Year": "2019", "Type of Meat": "Ovine", "Production (Tonnes)": 59000, "Growth Rate (%)": 3.51},
    {"Year": "2019", "Type of Meat": "Caprine", "Production (Tonnes)": 10000, "Growth Rate (%)": 5.26},
    {"Year": "2020", "Type of Meat": "Bovine", "Production (Tonnes)": 65000, "Growth Rate (%)": 6.56},
    {"Year": "2020", "Type of Meat": "Ovine", "Production (Tonnes)": 60000, "Growth Rate (%)": 1.69},
    {"Year": "2020", "Type of Meat": "Caprine", "Production (Tonnes)": 10200, "Growth Rate (%)": 2.0},
]

# Create the DataFrame
df = pd.DataFrame(data)

# Display the DataFrame

df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel("agriculture_data_with_olive_and_dattes.xlsx", index=False)
print("Data saved to agriculture_data_with_olive_and_dattes.xlsx")
