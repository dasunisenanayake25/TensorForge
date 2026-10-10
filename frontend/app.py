import os

import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="TensorForge | Support Routing",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    /* Foundation and responsive page surface. */
    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap");
    :root {
        --tf-navy: #0b1220;
        --tf-blue: #2563eb;
        --tf-cyan: #22d3ee;
        --tf-violet: #8b5cf6;
        --tf-ink: #172033;
        --tf-muted: #64748b;
        --tf-surface: rgba(255, 255, 255, 0.72);
        --tf-border: rgba(148, 163, 184, 0.25);
        --tf-shadow: 0 18px 50px rgba(15, 23, 42, 0.1);
    }
    html, body, [class*="css"] {
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    h1, h2, h3, h4, [data-testid="stMetricLabel"] {
        font-family: "Space Grotesk", Inter, system-ui, sans-serif;
    }
    .stApp {
        color: var(--tf-ink);
        background:
            radial-gradient(circle at 12% 8%, rgba(37, 99, 235, 0.09), transparent 28rem),
            radial-gradient(circle at 92% 22%, rgba(139, 92, 246, 0.08), transparent 26rem),
            linear-gradient(135deg, #f8fafc 0%, #eef4ff 52%, #f8fafc 100%);
        background-size: 150% 150%;
    }
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        opacity: 0.22;
        background-image: radial-gradient(rgba(37, 99, 235, 0.2) 0.7px, transparent 0.7px);
        background-size: 28px 28px;
    }
    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3.5rem;
    }

    /* Hero header with layered glow, grid texture, and intentional motion. */
    .hero {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        min-height: 170px;
        padding: 2.25rem 2.5rem;
        border: 1px solid rgba(147, 197, 253, 0.25);
        border-radius: 1.35rem;
        background:
            linear-gradient(110deg, rgba(11, 18, 32, 0.98), rgba(23, 37, 84, 0.96) 46%, rgba(37, 99, 235, 0.94)),
            linear-gradient(120deg, #172554, #2563eb);
        background-size: 180% 180%;
        box-shadow: 0 24px 60px rgba(23, 37, 84, 0.2);
        color: white;
        margin-bottom: 1.65rem;
    }
    .hero::before {
        content: "";
        position: absolute;
        inset: 0;
        z-index: -1;
        opacity: 0.16;
        background-image:
            linear-gradient(rgba(255, 255, 255, 0.2) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.2) 1px, transparent 1px);
        background-size: 28px 28px;
    }
    .hero::after {
        content: "";
        position: absolute;
        width: 240px;
        height: 240px;
        right: 9%;
        top: -105px;
        z-index: -1;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(34, 211, 238, 0.42), transparent 68%);
        filter: blur(8px);
    }
    .hero-orb {
        position: absolute;
        width: 120px;
        height: 120px;
        right: 25%;
        bottom: -72px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.5), transparent 68%);
        filter: blur(10px);
        pointer-events: none;
    }
    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        color: #a5f3fc;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }
    .hero h1 {
        margin: 0;
        color: white;
        font-size: clamp(2rem, 4vw, 3.2rem);
        letter-spacing: -0.045em;
        line-height: 1.05;
    }
    .hero p {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin: 0.8rem 0 0;
        color: #dbeafe;
        font-size: 1rem;
    }
    .live-dot {
        width: 0.55rem;
        height: 0.55rem;
        flex: 0 0 auto;
        border-radius: 50%;
        background: var(--tf-cyan);
        box-shadow: 0 0 0 0 rgba(34, 211, 238, 0.65);
    }

    /* Pill tabs and stable Streamlit widget surfaces. */
    [data-baseweb="tab-list"] {
        gap: 0.45rem;
        padding: 0.35rem;
        border: 1px solid var(--tf-border);
        border-radius: 999px;
        background: rgba(226, 232, 240, 0.56);
    }
    [data-baseweb="tab"] {
        min-height: 2.45rem;
        border-radius: 999px;
        color: var(--tf-muted);
        font-weight: 600;
        transition: color 180ms ease, background 180ms ease, transform 180ms ease;
    }
    [data-baseweb="tab"]:hover {
        color: var(--tf-blue);
        background: rgba(255, 255, 255, 0.72);
        transform: translateY(-1px);
    }
    [aria-selected="true"][data-baseweb="tab"] {
        color: white;
        background: linear-gradient(110deg, var(--tf-blue), var(--tf-violet));
        box-shadow: 0 5px 16px rgba(37, 99, 235, 0.22);
    }
    [data-baseweb="tab-highlight"] {
        display: none;
    }
    [data-testid="stForm"] {
        padding: 1.35rem;
        border: 1px solid var(--tf-border);
        border-radius: 1.1rem;
        background: var(--tf-surface);
        box-shadow: var(--tf-shadow);
        backdrop-filter: blur(16px);
    }
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stFileUploaderDropzone"] {
        border-radius: 0.75rem;
        border-color: rgba(148, 163, 184, 0.42);
        background: rgba(255, 255, 255, 0.7);
        transition: border-color 180ms ease, box-shadow 180ms ease;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--tf-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
    }

    /* Glass metric cards, result containers, and dataframes. */
    [data-testid="stMetric"] {
        position: relative;
        overflow: hidden;
        border: 1px solid var(--tf-border);
        border-radius: 1rem;
        padding: 1rem 1.15rem;
        background: var(--tf-surface);
        box-shadow: var(--tf-shadow);
        backdrop-filter: blur(14px);
        transition: transform 180ms ease, box-shadow 180ms ease;
    }
    [data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 4px;
        background: linear-gradient(180deg, var(--tf-cyan), var(--tf-violet));
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 22px 42px rgba(37, 99, 235, 0.16);
    }
    [data-testid="stDataFrame"] {
        overflow: hidden;
        border: 1px solid var(--tf-border);
        border-radius: 1rem;
        background: var(--tf-surface);
        box-shadow: var(--tf-shadow);
        backdrop-filter: blur(12px);
    }
    [data-testid="stAlert"] {
        border: 1px solid currentColor;
        border-radius: 0.85rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
    }

    /* Gradient buttons with a restrained hover shimmer. */
    .stButton > button,
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stDownloadButton"] button {
        position: relative;
        overflow: hidden;
        border: 0;
        border-radius: 0.75rem;
        color: white;
        background: linear-gradient(110deg, #2563eb, #22d3ee);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.22);
        font-weight: 700;
        transition: transform 160ms ease, box-shadow 160ms ease;
    }
    .stButton > button::after,
    [data-testid="stFormSubmitButton"] button::after,
    [data-testid="stDownloadButton"] button::after {
        content: "";
        position: absolute;
        inset: 0;
        transform: translateX(-120%);
        background: linear-gradient(105deg, transparent 25%, rgba(255, 255, 255, 0.35), transparent 75%);
        transition: transform 450ms ease;
    }
    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover,
    [data-testid="stDownloadButton"] button:hover {
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35);
        transform: translateY(-2px);
    }
    .stButton > button:hover::after,
    [data-testid="stFormSubmitButton"] button:hover::after,
    [data-testid="stDownloadButton"] button:hover::after {
        transform: translateX(120%);
    }
    .stButton > button:active,
    [data-testid="stFormSubmitButton"] button:active,
    [data-testid="stDownloadButton"] button:active {
        transform: scale(0.98);
    }

    /* Sidebar styling remains available for Streamlit's optional sidebar. */
    [data-testid="stSidebar"] {
        background: linear-gradient(165deg, #0b1220, #172554 70%, #1d4ed8);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #dbeafe;
    }

    /* Motion is opt-in and uses composited transform/opacity properties. */
    @media (prefers-reduced-motion: no-preference) {
        .stApp { animation: tf-mesh 18s ease-in-out infinite alternate; }
        .hero { animation: tf-gradient 12s ease-in-out infinite alternate; }
        .hero h1, .hero p, .hero-kicker { animation: tf-rise 650ms ease-out both; }
        .hero p { animation-delay: 90ms; }
        .hero-orb { animation: tf-float 8s ease-in-out infinite; }
        .live-dot { animation: tf-pulse 2s ease-out infinite; }
        [data-testid="stForm"] { animation: tf-rise 500ms ease-out both; }
        [data-testid="stMetric"] { animation: tf-fade 550ms ease-out both; }
        [data-testid="stAlert"] { animation: tf-slide 420ms ease-out both; }
    }
    @keyframes tf-gradient {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    @keyframes tf-mesh {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }
    @keyframes tf-rise {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes tf-fade {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes tf-slide {
        from { opacity: 0; transform: translateX(-12px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes tf-float {
        0%, 100% { transform: translate3d(0, 0, 0); }
        50% { transform: translate3d(-18px, -12px, 0); }
    }
    @keyframes tf-pulse {
        0% { box-shadow: 0 0 0 0 rgba(34, 211, 238, 0.65); }
        70% { box-shadow: 0 0 0 8px rgba(34, 211, 238, 0); }
        100% { box-shadow: 0 0 0 0 rgba(34, 211, 238, 0); }
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --tf-ink: #e2e8f0;
            --tf-muted: #94a3b8;
            --tf-surface: rgba(15, 23, 42, 0.72);
            --tf-border: rgba(148, 163, 184, 0.2);
            --tf-shadow: 0 18px 50px rgba(0, 0, 0, 0.24);
        }
        .stApp {
            background: radial-gradient(circle at 12% 8%, rgba(37, 99, 235, 0.16), transparent 28rem),
                linear-gradient(135deg, #070d18, #0f172a 55%, #111827);
        }
        [data-baseweb="tab-list"] { background: rgba(30, 41, 59, 0.72); }
        [data-baseweb="tab"]:hover { background: rgba(51, 65, 85, 0.72); }
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stFileUploaderDropzone"] {
            background: rgba(15, 23, 42, 0.72);
            color: #e2e8f0;
        }
    }
    @media (max-width: 700px) {
        .block-container { padding: 1rem 0.85rem 2.5rem; }
        .hero { padding: 1.6rem 1.35rem; }
        [data-baseweb="tab-list"] { overflow-x: auto; justify-content: flex-start; }
        [data-baseweb="tab"] { white-space: nowrap; }
    }
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
        <span class="hero-orb" aria-hidden="true"></span>
        <div class="hero-kicker">⚡ TensorForge workspace</div>
        <h1>Support routing, intelligently delivered.</h1>
        <p><span class="live-dot" aria-hidden="true"></span>Classify customer tickets and route them to the right support team.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_base_url = os.getenv("TENSORFORGE_API_BASE_URL", "http://localhost:8000").strip().rstrip("/")
api_key = os.getenv("TENSORFORGE_API_KEY", "")

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
