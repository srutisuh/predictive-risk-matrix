# %%
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os

# %%
# 1. Page Config
st.set_page_config(page_title="Predictive Operational Risk Matrix", page_icon="🛡️", layout="wide")

st.title("🛡️ Predictive Operational Risk Matrix & EWS")
st.markdown(
    """
    This early warning system translates real-time **Key Risk Indicators (KRIs)** into predictive risk metrics, 
    automatically mapping exposure onto a dynamic 5x5 Risk Assessment Matrix.
    """
)
st.write("---")

# %%
# 2. Smart Fallback Model Loader (Prevents crashes)
@st.cache_resource
def load_risk_model():
    model_path = 'predictive_risk_model.pkl'
    if not os.path.exists(model_path):
        # Programmatically train a quick fallback model if user runs app.py directly
        from sklearn.ensemble import RandomForestClassifier
        X_dummy = np.random.uniform(0, 10, (200, 3))
        y_dummy = (X_dummy[:, 0]*0.35 + X_dummy[:, 1]*0.4 + X_dummy[:, 2]*0.25 > 5).astype(int)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_dummy, y_dummy)
        joblib.dump(model, model_path)
    return joblib.load(model_path)

model = load_risk_model()

# %%
# 3. Sidebar UI - Parameter Stress Testing
st.sidebar.header("🧪 KRI Stress-Testing Inputs")

payload_err = st.sidebar.slider("Payload Error Rate (%)", 0.0, 10.0, 3.2, help="Data Quality KRI")
latency_dev = st.sidebar.slider("Latency Deviation (ms)", 0.0, 150.0, 45.0, help="Operational Latency KRI")
sla_breach = st.sidebar.slider("SLA Breach Rate (%)", 0.0, 15.0, 2.5, help="Compliance KRI")

st.sidebar.write("---")

# %%
# Business Impact is subjective and manually assessed by Risk Officers
business_impact = st.sidebar.slider("Assessed Business Impact", 1, 5, 3, 
                                    help="1: Negligible, 2: Minor, 3: Moderate, 4: Major, 5: Critical")

# %%
# 4. Predict Risk Probability
input_data = pd.DataFrame([[payload_err, latency_dev, sla_breach]], 
                          columns=['data_payload_error_rate', 'api_latency_deviation_ms', 'sla_breach_rate_pct'])

predicted_prob = model.predict_proba(input_data)[0][1]

# %%
# Map ML probability (0 to 1) directly to Likelihood axis (1 to 5)
likelihood_score = 1 + (predicted_prob * 4)

# %%
# 5. Core Metrics Dashboard
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("ML Predicted Incident Probability", f"{predicted_prob:.1%}")
with col2:
    st.metric("Calculated Likelihood Score (Y-Axis)", f"{likelihood_score:.2f} / 5.0")
with col3:
    # Determine risk category
    risk_product = likelihood_score * business_impact
    if risk_product <= 6:
        status = "🟢 LOW RISK"
    elif risk_product <= 12:
        status = "🟡 MEDIUM RISK"
    else:
        status = "🔴 CRITICAL RISK"
    st.metric("System Risk Severity", status)

st.write("---")

# %%
# 6. Render the 5x5 Interactive Risk Matrix
# Define color bounds: 1=Green, 2=Yellow, 3=Red
matrix_z = [
    [1, 1, 1, 1, 2],  # Likelihood = 1
    [1, 1, 2, 2, 2],  # Likelihood = 2
    [1, 2, 2, 2, 3],  # Likelihood = 3
    [1, 2, 2, 3, 3],  # Likelihood = 4
    [2, 2, 3, 3, 3]   # Likelihood = 5
]

fig = go.Figure()

# Background heatmap representing the risk levels
fig.add_trace(go.Heatmap(
    z=matrix_z,
    x=[1, 2, 3, 4, 5],
    y=[1, 2, 3, 4, 5],
    colorscale=[[0.0, '#C1E1C1'], [0.5, '#FDFD96'], [1.0, '#FF6961']], # Pastel Green, Yellow, Red
    showscale=False,
    hoverinfo='skip'
))

# Interactive scatter point tracking active risk state
fig.add_trace(go.Scatter(
    x=[business_impact],
    y=[likelihood_score],
    mode='markers+text',
    marker=dict(color='#1A1A1A', size=20, symbol='circle-dot', line=dict(color='white', width=3)),
    name='Active Risk Coordinates',
    text=['<b>⚠️ Active Risk State</b>'],  # Added HTML bold tags for extra pop
    textposition='top center',
    textfont=dict(color='#1A1A1A', size=14),  # Explicitly forces a dark, readable color and larger font
    hoverinfo='text'
))

fig.update_layout(
    title="Real-Time Predictive Risk Positioning",
    xaxis=dict(title="Assessed Business Impact", tickvals=[1,2,3,4,5], range=[0.5, 5.5]),
    yaxis=dict(title="Model Predicted Likelihood (Scale 1-5)", tickvals=[1,2,3,4,5], range=[0.5, 5.5]),
    height=500,
    template="plotly_white",
    showlegend=False
)

chart_col, text_col = st.columns([3, 2])
with chart_col:
    st.plotly_chart(fig, use_container_width=True)

with text_col:
    st.subheader("📋 Prescriptive Response Framework")
    st.markdown("Automated trigger protocols based on current risk vector calculations:")
    
    if status == "🔴 CRITICAL RISK":
        st.error(
            "🚨 **CRITICAL MITIGATION REQUIRED (SLA Rule 104):**\n\n"
            "* Initiate secondary pipeline replication immediately.\n"
            "* Pause bulk non-essential data migrations with this partner.\n"
            "* Flag to executive risk committee. Automated alert dispatched to Ops Director."
        )
    elif status == "🟡 MEDIUM RISK":
        st.warning(
            "⚠️ **ELEVATED MONITORING PROTOCOL (SLA Rule 102):**\n\n"
            "* Increase logging resolution on this partner's microservices.\n"
            "* Schedule a routine data accuracy review within 48 hours.\n"
            "* Continuous alert status active in engineering console."
        )
    else:
        st.success(
            "🟢 **STANDARD CONTROL STATUS (SLA Rule 101):**\n\n"
            "* Operations proceeding within normal thresholds.\n"
            "* Standard nightly audits active.\n"
            "* No manual intervention required."
        )

# %%



