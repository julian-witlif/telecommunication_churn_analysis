import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import textwrap
import numpy as np


# Load the Excel file
df = pd.read_excel('Customer Churn.xlsx', sheet_name='Telco_Churn')

# Clean 'Total Charges' (convert empty values to 0)
df['Total Charges'] = pd.to_numeric(df['Total Charges'], errors='coerce').fillna(0)

# Mapping for binary features
binary_mappings = {
    'Senior Citizen': {'Yes': 1, 'No': 0},
    'Partner': {'Yes': 1, 'No': 0},
    'Dependents': {'Yes': 1, 'No': 0},
    'Phone Service': {'Yes': 1, 'No': 0},
    'Paperless Billing': {'Yes': 1, 'No': 0},
    'Gender': {'Male': 1, 'Female': 0}
}
for col, mapping in binary_mappings.items():
    df[col] = df[col].map(mapping)

# Define features (excluding IDs, geo-data, Churn Reason)
# Exclude 'Total Charges' strongly dependent on Monthly Charges * Tenure Months, could confuse model
# Exclude Churn Reason, because customers with a churn reason already churned
features = [
    'Gender', 'Senior Citizen', 'Partner', 'Dependents', 'Tenure Months',
    'Phone Service', 'Multiple Lines', 'Internet Service', 'Online Security',
    'Online Backup', 'Device Protection', 'Tech Support', 'Streaming TV',
    'Streaming Movies', 'Contract', 'Paperless Billing', 'Payment Method',
    'Monthly Charges'
]
cat_features = [col for col in features if df[col].dtype == 'object']
num_features = [col for col in features if col not in cat_features]

# Target (Churn Label as 0/1)
df['Churn'] = df['Churn Label'].map({'Yes':1, 'No':0})
y = df['Churn']
X = df[features]

# Split into Train/Test (for training)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessor (scaling + encoding)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
    ])

# Model pipeline
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('classifier', LogisticRegression(max_iter=1000))])

# Train the model
model.fit(X_train, y_train)

# Calculate probabilities for all customers
df['Churn_Probability'] = model.predict_proba(X)[:, 1].round(2)  # Column with probability (0-1) for Churn=Yes

# Save as CSV: original columns + new probability
df.to_csv('churn_predictions.csv', index=False)

print(df.head(5)[['CustomerID', 'Churn Label', 'Churn_Probability']])

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Extract coefficients
coef = model.named_steps['classifier'].coef_[0]

# Get the feature names
feature_names = model.named_steps['preprocessor'].get_feature_names_out()

importance = pd.DataFrame({'Feature': feature_names, 'Coefficient': coef})

# Add absolute coefficients for ranking
importance['Abs_Coefficient'] = abs(importance['Coefficient'])

# Sort in descending order
importance = importance.sort_values(by='Abs_Coefficient', ascending=False)


print(importance)


################################################## Plotting ##################################################

number_of_coefficients_plot = 10

# Create a list of colors based on the sign of the original coefficient
colors = ['red' if coef > 0 else 'green' for coef in importance['Coefficient'].head(number_of_coefficients_plot)]

# Plot the top 20 features as a bar chart
plt.figure(figsize=(11, 8))
plt.barh(importance['Feature'].head(number_of_coefficients_plot),
         importance['Abs_Coefficient'].head(number_of_coefficients_plot), color=colors)
plt.xlabel('Absolute Coefficient')
plt.ylabel('Feature')
plt.title(f'Top {number_of_coefficients_plot} Feature Importance\'s for Churn by Absolute Coefficient')
plt.gca().invert_yaxis()  # Highest on top

# Adjust left margin to prevent label cutoff
plt.subplots_adjust(left=0.25)

# Wrapping long names y-axis
wrapped_labels = [textwrap.fill(label, width=30) for label in importance['Feature'].head(number_of_coefficients_plot)]
plt.gca().set_yticklabels(wrapped_labels)

from matplotlib.lines import Line2D

# Legend
red_patch = mpatches.Patch(color='red', label='Increase Churn probability')
green_patch = mpatches.Patch(color='green', label='Decrease Churn probability')

cat_desc = Line2D([], [], linestyle='none', label='cat__ →  specific category of a feature')
num_desc = Line2D([], [], linestyle='none', label='num__ → numeric value')

plt.legend(
    handles=[red_patch, green_patch, cat_desc, num_desc],
)

plt.show()



# Plot the distribution of Churn Probabilities for non-churned customers (Churn Label == 'No')
non_churned = df[df['Churn Label'] == 'No']['Churn_Probability']

plt.figure(figsize=(10, 6))
bins = np.arange(0, 1.1, 0.1)
plt.hist(non_churned, bins=bins, color='blue', edgecolor='black')
plt.title('Distribution of Churn Probabilities for Non-Churned Customers')
plt.xlabel('Churn Probability')
plt.ylabel('Number of Customers')
plt.grid(True)
plt.show()


