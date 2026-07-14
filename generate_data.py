# %%
import pandas as pd
import numpy as np

# %%
# Set random seed for identical dataset generation
np.random.seed(42)
n_partners = 1000

# %%
# 1. Generate Key Risk Indicators (KRIs)
# Data Quality KRI: Data feed error rate (0% to 10%)
payload_error_rate = np.random.uniform(0.0, 10.0, n_partners)

# %%
# Operational KRI: Average API latency deviation in milliseconds
latency_deviation_ms = np.random.normal(50, 20, n_partners)
latency_deviation_ms = np.clip(latency_deviation_ms, 0, 150)

# %%
# Compliance KRI: Contractual SLA breach rate (0% to 15%)
sla_breach_rate_pct = np.random.uniform(0.0, 15.0, n_partners)

# %%
# 2. Mathematically define the risk threshold logic (hidden ground truth)
raw_risk = (
    0.35 * (payload_error_rate / 10.0) + 
    0.40 * (latency_deviation_ms / 150.0) + 
    0.25 * (sla_breach_rate_pct / 15.0) +
    np.random.normal(0, 0.08, n_partners) # Add realistic noise
)

# %%
# If raw risk exceeds the 0.5 threshold, a critical incident is triggered
incident_occurred = (raw_risk > 0.5).astype(int)

# %%
# 3. Compile and save
df = pd.DataFrame({
    'partner_id': [f"PARTNER-{i:04d}" for i in range(1, n_partners + 1)],
    'data_payload_error_rate': np.round(payload_error_rate, 2),
    'api_latency_deviation_ms': np.round(latency_deviation_ms, 1),
    'sla_breach_rate_pct': np.round(sla_breach_rate_pct, 2),
    'operational_incident': incident_occurred
})

# %%
df.to_csv('operational_kri_data.csv', index=False)
print("Dataset successfully generated and saved to 'operational_kri_data.csv'!")

# %%



