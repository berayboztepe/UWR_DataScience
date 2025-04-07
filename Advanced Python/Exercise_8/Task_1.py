import requests
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

def get_nbp_data(start_date, end_date, currency="USD"):
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency}/{start_date}/{end_date}/?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = data["rates"]
        return pd.DataFrame({
            "Date": [item["effectiveDate"] for item in rates],
            "Rate": [item["mid"] for item in rates]
        })
    else:
        raise ValueError("Error fetching data from NBP API")
    
def predict_future_values(data_combined):
    X = np.array(data_combined.index).reshape(-1, 1)
    y = data_combined["Rate"].values

    model = LinearRegression()
    model.fit(X, y)

    future_indices = np.arange(len(data_combined), len(data_combined) + 12).reshape(-1, 1)
    future_values = model.predict(future_indices)

    return future_values


data_2022 = get_nbp_data("2022-01-01", "2022-12-31")
data_2023 = get_nbp_data("2023-01-01", "2023-12-31")

data_2022["Date"] = pd.to_datetime(data_2022["Date"])
data_2022["Month"] = data_2022["Date"].dt.month

data_2023["Date"] = pd.to_datetime(data_2023["Date"])
data_2023["Month"] = data_2023["Date"].dt.month

monthly_avg_2022 = data_2022.groupby("Month")["Rate"].mean().reset_index()
monthly_avg_2023 = data_2023.groupby("Month")["Rate"].mean().reset_index()


data_combined = pd.concat([data_2022, data_2023])
future_values = predict_future_values(data_combined)
print(future_values)
future_months = np.arange(1, 13)

plt.figure(figsize=(10, 6))
plt.plot(monthly_avg_2022["Month"], monthly_avg_2022["Rate"], marker='o', label="2022")
plt.plot(monthly_avg_2023["Month"], monthly_avg_2023["Rate"], marker='s', label="2023")
plt.plot(future_months, future_values, marker='*', linestyle='--', label="Predicted 2024")

plt.xticks(range(1, 13), 
           ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.xlabel("Month")
plt.ylabel("Exchange Rate (PLN/USD)")
plt.title("Monthly Average USD Exchange Rates for 2022-2023 and Prediction for 2024")
plt.legend()
plt.grid()
plt.show()
