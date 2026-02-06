import gradio as gr
import pandas as pd
import numpy as np
import kagglehub
import os
from sklearn.ensemble import IsolationForest
from huggingface_hub import InferenceClient

# --- 1. CONFIGURATION & AI CLIENT ---
# Accessing the HF_TOKEN from your Space Secrets
hf_token = os.getenv("HF_TOKEN")
# Using Llama-3-8B for reasoning capabilities
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=hf_token)

# --- 2. THE AGENTIC COMPONENT ---
def ai_agent_analysis(threat_data):
    """The AI Agent analyzes the ML output to explain risks to hospital staff."""
    if not hf_token:
        return "⚠️ AGENT OFFLINE: Please add 'HF_TOKEN' to Space Secrets to enable AI reasoning."
    
    prompt = f"""
    [ROLE] You are a Senior Hospital Cybersecurity Analyst.
    [CONTEXT] Our ML model detected the following anomalous logs:
    {threat_data}
    
    [TASK] Provide a concise (2-3 sentence) summary for medical staff explaining:
    1. What the suspicious activity is.
    2. The potential risk to patient data.
    3. A suggested immediate action.
    """
    
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Agent was unable to process the logs. Technical Error: {str(e)}"

# --- 3. SIEM ML PIPELINE ---
def run_siem_audit():
    """Ingests Kaggle data, runs Isolation Forest, and triggers the Agent."""
    try:
        # Download healthcare dataset
        path = kagglehub.dataset_download("programmer3/secure-healthcare-iot-monitoring-dataset")
        csv_file = [f for f in os.listdir(path) if f.endswith('.csv')][0]
        df = pd.read_csv(f"{path}/{csv_file}")
    except Exception:
        # Robust fallback for demo stability
        df = pd.DataFrame({
            'device_id': [f"Device_{i}" for i in range(50)],
            'failed_logins': np.random.randint(0, 20, 50),
            'data_transfer_mb': np.random.randint(10, 500, 50)
        })

    # ML Detection
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    model = IsolationForest(contamination=0.04, random_state=42)
    df['anomaly_score'] = model.fit_predict(df[numeric_cols].fillna(0))
    
    # Identify top threats
    threats = df[df['anomaly_score'] == -1].head(3)
    threat_string = threats.to_string()
    
    # Trigger the Agentic Analysis
    agent_report = ai_agent_analysis(threat_string)
    
    return df.head(10), threats, agent_report

# --- 4. GRADIO INTERFACE ---
with gr.Blocks(theme=gr.themes.Soft(), title="Agentic Hospital SIEM") as demo:
    gr.Markdown("# 🏥 Agentic Hospital SIEM Dashboard")
    gr.Markdown("Combining **Isolation Forest ML** for detection and **Llama-3 AI** for agentic reasoning.")
    
    run_btn = gr.Button("🚀 Run Global Security Scan", variant="primary")
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 🤖 AI Agent Security Analysis")
            agent_out = gr.Markdown("Click 'Run Scan' to consult the AI Agent...")
        with gr.Column(scale=1):
            gr.Markdown("### 🚩 Detected Threat Samples")
            threat_out = gr.DataFrame()
            
    with gr.Accordion("View Raw Telemetry Data", open=False):
        raw_out = gr.DataFrame()

    run_btn.click(run_siem_audit, outputs=[raw_out, threat_out, agent_out])

if __name__ == "__main__":
    demo.launch()
