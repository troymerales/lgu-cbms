import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Placeholder for reading the data file
# Change 'your_data.xlsx' to your actual file path
file_path = 'ppd.xlsx'
data = pd.read_excel(file_path)


# Define the logistic function
def logistic(z):
    return 1 / (1 + np.exp(-z))

# Prepare X and y
# Placeholder columns - replace or modify based on your actual data structure
# Assume postpartum depression symptoms is binary target column named 'PPD'
# And all others are predictors (some may require encoding and preprocessing)

predictor_cols = [
    'Age', 'Living with', 'Monthly income', 'Work', 'Educational Attainment', 
    'Hx of Psych', 'Hx Medical', 'FHx Psych', 'Gravidity', 'AOG delivery', 
    'Planned Pregnancy', 'Number PNC', 'Mode Delivery', 'Status Baby', 'Complication ', 
    'Congenital Dse', 'Breast Feeding', 'Vaping', 'Drinking', 'Physical Abuse', 
    'Verbal Abuse', 'Sexual Abuse', 'Family Death', 'Support partner', 'Support Family'
]

y = data['postpartum depression symptoms'].astype(int).values  # binary target
X = data[predictor_cols].copy()

# -- preprocessing placeholder --
# For categorical variables, convert them to dummy variables or encoded values
# Drop the target column from predictors if present
predictor_cols_existing = [col for col in predictor_cols if col in data.columns]
X = data[predictor_cols_existing].copy()

# Encode categorical variables
X = pd.get_dummies(X, drop_first=True)

# Fill missing values with 0
X = X.fillna(0)

# Add intercept
X.insert(0, 'Intercept', 1)

# Convert to numeric NumPy array
X = X.values.astype(float)

# Target
y = data['postpartum depression symptoms'].astype(int).values

# For now, assume all are numeric or preprocessed

X = pd.get_dummies(X, drop_first=True)
X = X.fillna(0)

# Add intercept while still a DataFrame
X.insert(0, 'Intercept', 1)

# Convert to NumPy array
X = X.values.astype(float)


# Add intercept
X.insert(0, 'Intercept', 1)
X = X.values

# Initialize coefficients
beta_init = np.zeros(X.shape[1])

# Define the negative log likelihood
def neg_log_likelihood(beta, X, y):
    z = np.dot(X, beta)
    p = logistic(z)
    # Avoid log(0) by clipping
    p = np.clip(p, 1e-10, 1 - 1e-10)
    ll = y * np.log(p) + (1 - y) * np.log(1 - p)
    return -np.sum(ll)

# Fit the model using MLE via minimize
result = minimize(neg_log_likelihood, beta_init, args=(X, y), method='BFGS')

beta_hat = result.x

print("Fitted coefficients:")
for name, coef in zip(['Intercept'] + predictor_cols, beta_hat):
    print(f"{name}: {coef}")

# Function to predict probabilities
def predict_proba(X, beta):
    return logistic(np.dot(X, beta))

# Predict probabilities for the data
probs = predict_proba(X, beta_hat)

# Predicted class with threshold 0.5
predicted_class = (probs >= 0.5).astype(int)

# Output example of first 5 predictions
print("\nFirst 5 predicted probabilities:", probs[:5])
print("First 5 predicted classes:", predicted_class[:5])