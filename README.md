🏥 AI-Powered Hospital SIEM & IoMT Monitor
The Problem
Traditional SIEMs rely on static rules, failing to catch "Zero-Day" ransomware or subtle HIPAA breaches (snooping). In healthcare, security must be proactive, private, and understandable to non-technical staff.

The Solution
This project is an intelligent SIEM prototype that monitors hospital logs—ranging from EHR access to Medical IoT (IoMT) telemetry. It replaces rigid "if-then" logic with Unsupervised Machine Learning to detect anomalies based on behavior rather than signatures.

🛠 Core Engineering Features
Behavioral Detection: Uses Isolation Forests to identify outliers in high-dimensional log data (access times, packet sizes, failed logins).

Automated Ingestion: Programmatically pulls healthcare-specific datasets via kagglehub for reproducible research.

HIPAA-First Pipeline: Built-in modularity for PII Scrubbing and data anonymization before model training.

Explainable AI (XAI): A custom Natural Language Generation (NLG) engine translates mathematical anomaly scores into Plain English Reports for clinical managers.

Live UI: Built with Gradio for rapid deployment and real-time visualization on Hugging Face Spaces.

🚀 Why it Matters 
Unsupervised Advantage: Identifies novel threats without requiring labeled attack data.

Modular Architecture: Separation of ingestion, detection, and reporting allows for easy scaling to real-time streams (e.g., Kafka).

Human-in-the-Loop: Bridges the gap between SOC analysts and hospital floor staff via interpretable reporting.
