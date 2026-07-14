# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# %%
# Load simulated database
df = pd.read_csv('operational_kri_data.csv')

# %%
# Split features and target labels
X = df[['data_payload_error_rate', 'api_latency_deviation_ms', 'sla_breach_rate_pct']]
y = df['operational_incident']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# %%
# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# %%
# Evaluate model performance
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# %%
print("Model Evaluation metrics:")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")

# %%
# Save the trained model binary
joblib.dump(model, 'predictive_risk_model.pkl')
print(" Model saved to 'predictive_risk_model.pkl'")

# %%



