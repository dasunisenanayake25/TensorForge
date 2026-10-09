import streamlit as st
import requests
import pandas as pd
import json

# Page Configuration & Styling
st.set_page_config(
    page_title="Team Cylix - TensorForge 2.0 MVP",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Team Cylix - Customer Support Routing Dashboard")
st.caption("TensorForge 2.0 Phase 2 MVP - Live Model Inference & Ticket Evaluation")

# Sidebar Configuration for API Base URL and Authentication Key
st.sidebar.header("🔑 System Credentials")
api_base_url = st.sidebar.text_input(
    "API Base URL", 
    value="http://localhost:8000",
    help="FastAPI backend host URL"
)
api_key = st.sidebar.text_input(
    "API Key", 
    value="tf2_0b0b7dc05ae49ce296bbd0d1fb596980a2b7dba11e4d6e80", 
    type="password",
    help="Assigned API key for Team Cylix"
)

# Request Headers
headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

# Create Navigation Tabs for Evaluation
tab_single, tab_batch, tab_async, tab_health = st.tabs([
    "🎯 Single Prediction", 
    "📦 Sync Batch Predict", 
    "🔄 Async Job Management", 
    "🏥 Health Status"
])

# ==========================================
# TAB 1: Single Ticket Prediction (/predict)
# ==========================================
with tab_single:
    st.subheader("Single Ticket Live Inference")
    st.write("Enter individual ticket details to perform immediate classification and team routing.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        ticket_id = st.text_input("Ticket ID", value="TICK-1001")
    with col2:
        ticket_text = st.text_area(
            "Ticket Description", 
            value="I was charged twice for my subscription payment on checkout.",
            height=120
        )
    
    if st.button("Classify Ticket", type="primary"):
        if not ticket_text.strip():
            st.warning("Please provide ticket content.")
        else:
            payload = {"id": ticket_id, "text": ticket_text}
            try:
                response = requests.post(
                    f"{api_base_url}/predict", 
                    headers=headers, 
                    json=payload, 
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("Classification Successful!")
                    
                    res_col1, res_col2 = st.columns(2)
                    res_col1.metric("Predicted Category", data.get("category", "N/A"))
                    res_col2.metric("Routed Team", data.get("team", "N/A"))
                    
                    st.json(data)
                else:
                    st.error(f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

# ==========================================
# TAB 2: Synchronous Batch Predict (/predict/batch)
# ==========================================
with tab_batch:
    st.subheader("Synchronous Batch Processing (1 - 100 Tickets)")
    st.write("Upload a CSV file containing `id` and `text` columns for direct batch predictions.")
    
    uploaded_file = st.file_uploader("Upload Batch CSV", type=["csv"], key="sync_csv")
    
    if uploaded_file is not None:
        df_input = pd.read_csv(uploaded_file)
        st.write("Preview Input Data:", df_input.head())
        
        if st.button("Run Sync Batch Prediction"):
            if "id" not in df_input.columns or "text" not in df_input.columns:
                st.error("CSV must contain 'id' and 'text' headers.")
            elif len(df_input) > 100:
                st.warning("Synchronous batch is intended for <= 100 tickets. Use Async Jobs for larger payloads.")
            else:
                payload = {"tickets": df_input.to_dict(orient="records")}
                try:
                    response = requests.post(
                        f"{api_base_url}/predict/batch", 
                        headers=headers, 
                        json=payload, 
                        timeout=30
                    )
                    if response.status_code == 200:
                        results = response.json().get("predictions", [])
                        st.success(f"Successfully processed {len(results)} tickets.")
                        st.dataframe(pd.DataFrame(results))
                    else:
                        st.error(f"HTTP {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

# ==========================================
# TAB 3: Asynchronous Jobs (/batch/jobs)
# ==========================================
with tab_async:
    st.subheader("Asynchronous Large Batch Evaluation (> 2000 Tickets)")
    st.write("Submit large datasets to background processing queue and poll status.")
    
    job_file = st.file_uploader("Upload Evaluation Dataset (CSV)", type=["csv"], key="async_csv")
    
    if job_file is not None:
        df_job = pd.read_csv(job_file)
        st.write(f"Loaded {len(df_job)} records.")
        
        if st.button("Submit Async Job"):
            payload = {"tickets": df_job.to_dict(orient="records")}
            try:
                response = requests.post(
                    f"{api_base_url}/batch/jobs", 
                    headers=headers, 
                    json=payload, 
                    timeout=30
                )
                if response.status_code in [200, 202]:
                    job_data = response.json()
                    st.success(f"Job Created! Job ID: `{job_data.get('job_id')}`")
                    st.json(job_data)
                else:
                    st.error(f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Submission failed: {e}")
                
    st.divider()
    st.subheader("Job Status & Results Retriever")
    query_job_id = st.text_input("Enter Job ID to Check Status / Results")
    
    if query_job_id and st.button("Poll Job Details"):
        try:
            status_res = requests.get(
                f"{api_base_url}/batch/jobs/{query_job_id}", 
                headers=headers, 
                timeout=10
            )
            if status_res.status_code == 200:
                st.json(status_res.json())
            else:
                st.error(f"HTTP {status_res.status_code}: {status_res.text}")
        except Exception as e:
            st.error(f"Failed to fetch job details: {e}")

# ==========================================
# TAB 4: Public Health Check (/health)
# ==========================================
with tab_health:
    st.subheader("System Health Monitoring")
    st.write("The `/health` endpoint is publicly accessible and doesn't require authentication.")
    
    if st.button("Check Service Health"):
        try:
            health_res = requests.get(f"{api_base_url}/health", timeout=5)
            if health_res.status_code == 200:
                st.success("Backend Service is Operational!")
                st.json(health_res.json())
            else:
                st.error(f"Service Unhealthy (HTTP {health_res.status_code}): {health_res.text}")
        except Exception as e:
            st.error(f"Could not reach backend: {e}")