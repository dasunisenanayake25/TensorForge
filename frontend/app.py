import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="TensorForge | Support Routing",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    [data-testid="stMetric"] {
        background: #f7f9fc;
        border: 1px solid #e7ebf2;
        border-radius: 0.75rem;
        padding: 0.75rem 1rem;
    }
    .hero {
        padding: 1.5rem 1.75rem;
        border-radius: 1rem;
        background: linear-gradient(110deg, #172554 0%, #2563eb 100%);
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 { margin: 0; color: white; }
    .hero p { margin: 0.4rem 0 0; color: #dbeafe; }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_api_error(response: requests.Response, action: str) -> None:
    """Show a readable API error without hiding useful backend details."""
    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    st.error(f"{action} failed (HTTP {response.status_code}).")
    if detail:
        st.caption(str(detail))


def read_csv(uploaded_file, label: str) -> pd.DataFrame | None:
    """Read an uploaded CSV and report user-correctable file errors."""
    try:
        frame = pd.read_csv(uploaded_file)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
        st.error(f"Could not read {label}. Please upload a valid UTF-8 CSV file.")
        st.caption(str(error))
        return None

    missing_columns = {"id", "text"} - set(frame.columns)
    if missing_columns:
        st.error(f"{label} must contain these columns: `id` and `text`.")
        return None
    if frame.empty:
        st.warning(f"{label} does not contain any tickets.")
        return None
    if frame[["id", "text"]].isna().any().any():
        st.warning("Every ticket must have both an `id` and `text` value.")
        return None
    return frame


st.markdown(
    """
    <div class="hero">
        <h1> TensorForge Support Routing</h1>
        <p>Classify customer tickets and route them to the right support team.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Connection")
    api_base_url = st.text_input(
        "Backend URL",
        value="http://localhost:8000",
        help="The address where the TensorForge API is running.",
    ).strip().rstrip("/")
    api_key = st.text_input(
        "API key",
        value="tf2_0b0b7dc05ae49ce296bbd0d1fb596980a2b7dba11e4d6e80",
        type="password",
        help="Used for prediction and batch endpoints. Health checks do not need it.",
    )
    st.divider()
    st.markdown("**Quick guide**")
    st.caption("1. Check the backend connection in Health.")
    st.caption("2. Classify one ticket or upload a CSV.")
    st.caption("3. Download batch predictions for further analysis.")

headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

tab_single, tab_batch, tab_async, tab_health = st.tabs(
    [" Single ticket", " Batch predictions", " Async jobs", " Health"]
)

with tab_single:
    st.subheader("Classify a single ticket")
    st.write("Get an immediate category and routing team for one customer request.")

    with st.form("single_ticket_form"):
        ticket_id = st.text_input("Ticket ID", value="TICK-1001")
        ticket_text = st.text_area(
            "Ticket description",
            value="I was charged twice for my subscription payment on checkout.",
            height=130,
            placeholder="Describe the customer's issue...",
        )
        classify_ticket = st.form_submit_button("Classify ticket", type="primary")

    if classify_ticket:
        if not ticket_id.strip():
            st.warning("Please enter a ticket ID.")
        elif not ticket_text.strip():
            st.warning("Please enter a ticket description.")
        else:
            with st.spinner("Classifying ticket..."):
                try:
                    response = requests.post(
                        f"{api_base_url}/predict",
                        headers=headers,
                        json={"id": ticket_id.strip(), "text": ticket_text.strip()},
                        timeout=10,
                    )
                except requests.RequestException as error:
                    st.error("Could not connect to the backend.")
                    st.caption(str(error))
                else:
                    if response.ok:
                        data = response.json()
                        st.success("Ticket classified successfully.")
                        result_col1, result_col2 = st.columns(2)
                        result_col1.metric("Predicted category", data.get("category", "N/A"))
                        result_col2.metric("Routed team", data.get("team", "N/A"))
                        with st.expander("View full response"):
                            st.json(data)
                    else:
                        show_api_error(response, "Ticket classification")

with tab_batch:
    st.subheader("Process a batch of tickets")
    st.write("Upload a CSV with `id` and `text` columns. Synchronous batches support up to 100 tickets.")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        key="sync_csv",
        help="Example: id,text",
    )

    if uploaded_file is not None:
        df_input = read_csv(uploaded_file, "The CSV")
        if df_input is not None:
            st.caption(f"{len(df_input):,} ticket(s) ready")
            st.dataframe(df_input.head(10), use_container_width=True, hide_index=True)
            if len(df_input) > 100:
                st.warning("This file has more than 100 tickets. Use Async jobs for larger datasets.")
            elif st.button("Run batch prediction", type="primary"):
                with st.spinner(f"Processing {len(df_input):,} ticket(s)..."):
                    try:
                        response = requests.post(
                            f"{api_base_url}/predict/batch",
                            headers=headers,
                            json={"tickets": df_input.to_dict(orient="records")},
                            timeout=30,
                        )
                    except requests.RequestException as error:
                        st.error("Could not connect to the backend.")
                        st.caption(str(error))
                    else:
                        if response.ok:
                            results = response.json().get("predictions", [])
                            results_df = pd.DataFrame(results)
                            st.success(f"Processed {len(results):,} ticket(s) successfully.")
                            st.dataframe(results_df, use_container_width=True, hide_index=True)
                            st.download_button(
                                "Download predictions as CSV",
                                results_df.to_csv(index=False).encode("utf-8"),
                                "tensorforge-predictions.csv",
                                "text/csv",
                            )
                        else:
                            show_api_error(response, "Batch prediction")

with tab_async:
    st.subheader("Run a large dataset in the background")
    st.write("Use an async job when your dataset is too large for synchronous processing.")
    job_file = st.file_uploader("Choose an evaluation CSV", type=["csv"], key="async_csv")

    if job_file is not None:
        df_job = read_csv(job_file, "The evaluation CSV")
        if df_job is not None:
            st.info(f"{len(df_job):,} ticket(s) loaded and ready to submit.")
            if st.button("Submit async job", type="primary"):
                with st.spinner("Submitting job..."):
                    try:
                        response = requests.post(
                            f"{api_base_url}/batch/jobs",
                            headers=headers,
                            json={"tickets": df_job.to_dict(orient="records")},
                            timeout=30,
                        )
                    except requests.RequestException as error:
                        st.error("Could not connect to the backend.")
                        st.caption(str(error))
                    else:
                        if response.ok:
                            job_data = response.json()
                            st.success(f"Job created: `{job_data.get('job_id', 'unknown')}`")
                            st.json(job_data)
                        else:
                            show_api_error(response, "Async job submission")

    st.divider()
    st.subheader("Check an existing job")
    query_job_id = st.text_input("Job ID", placeholder="Paste a job ID here")
    if st.button("Check job status"):
        if not query_job_id.strip():
            st.warning("Please enter a job ID.")
        else:
            with st.spinner("Fetching job status..."):
                try:
                    response = requests.get(
                        f"{api_base_url}/batch/jobs/{query_job_id.strip()}",
                        headers=headers,
                        timeout=10,
                    )
                except requests.RequestException as error:
                    st.error("Could not connect to the backend.")
                    st.caption(str(error))
                else:
                    if response.ok:
                        st.json(response.json())
                    else:
                        show_api_error(response, "Job status request")

with tab_health:
    st.subheader("Backend health")
    st.write("Check whether the TensorForge API is reachable and ready to accept requests.")
    if st.button("Check connection", type="primary"):
        with st.spinner("Checking backend..."):
            try:
                response = requests.get(f"{api_base_url}/health", timeout=5)
            except requests.RequestException as error:
                st.error("Backend is unreachable.")
                st.caption(str(error))
            else:
                if response.ok:
                    st.success("Backend is online.")
                    with st.expander("View health response", expanded=True):
                        st.json(response.json())
                else:
                    show_api_error(response, "Health check")
