import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# Load the dataset
file_path = './uploads/oil_prices.csv'  # Replace with the correct path to your file
data = pd.read_csv(file_path, skiprows=3)

# Check and rename columns for consistency
if 'Country Name' in data.columns:
    # Filter for Tunisia data only and keep years 1960 to 2023
    tunisia_data = data[data['Country Name'] == 'Tunisia'].loc[:, '1960':'2023'].T
    tunisia_data.columns = ['Inflation Rate']
    tunisia_data.dropna(inplace=True)  # Drop rows with NaN values
else:
    print("Expected column 'Country Name' not found in the data.")

# Convert the index to integer type for year representation
tunisia_data.index = tunisia_data.index.astype(int)

# Prepare the data for modeling
# Shift the 'Inflation Rate' column to create a supervised learning problem where each year's rate predicts the next year's rate
tunisia_data['Next Year Inflation Rate'] = tunisia_data['Inflation Rate'].shift(-1)
tunisia_data.dropna(inplace=True)

# Separate features (X) and target (y)
X = tunisia_data[['Inflation Rate']]
y = tunisia_data['Next Year Inflation Rate']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the Model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Save the Model for Later Use
joblib.dump(model, './tunisia_inflation_model.pkl')
print("Model saved as 'tunisia_inflation_model.pkl'")

# Plot the Actual vs Predicted inflation rates
plt.figure(figsize=(10, 6))
plt.plot(y_test.index, y_test, label='Actual Inflation Rate', color='blue')
plt.plot(y_test.index, y_pred, label='Predicted Inflation Rate', color='red')
plt.xlabel('Year')
plt.ylabel('Inflation Rate (%)')
plt.title('Predicted vs Actual Inflation Rate in Tunisia')
plt.legend()
plt.show()
