import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load dataset
def load_data():
    data = sns.load_dataset('diamonds')
    data = data[['cut', 'carat', 'price']].dropna()
    data = data[(data['cut'] == 'Premium') & (data['carat'] > 0) & (data['price'] > 0)]  # Filter for Premium cuts
    return data

# Load data
data = load_data()

# Elasticity Calculation
data['log_price'] = np.log(data['price'])
data['log_carat'] = np.log(data['carat'])

X = sm.add_constant(data['log_price'])
y = data['log_carat']
model = sm.OLS(y, X).fit()

elasticity = model.params['log_price']
print(f"\nElasticity Coefficient for Premium cuts: {elasticity:.2f}")
print("Elasticity indicates that a 1% change in price leads to a "
      f"{elasticity:.2f}% change in demand.")

# Regression summary
print("\nRegression Model Summary:")
print(model.summary())

# Visualization: Boxplot of Carat vs Price Quartiles
data['price_quartile'] = pd.qcut(data['price'], q=4, labels=["Q1 (Low)", "Q2", "Q3", "Q4 (High)"])

plt.figure(figsize=(10, 6))
sns.boxplot(x='price_quartile', y='carat', data=data, palette="coolwarm")
plt.title("Distribution of Carat Across Price Quartiles (Premium Cuts)")
plt.xlabel("Price Quartiles")
plt.ylabel("Carat (Demand)")
plt.grid(True)

# Export the plot as PNG
plt.savefig("boxplot_carat_vs_price.png", dpi=300)
plt.show()

print("Boxplot has been saved as 'boxplot_carat_vs_price.png' in the current directory.")
