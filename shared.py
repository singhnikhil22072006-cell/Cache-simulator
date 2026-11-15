from pathlib import Path
import streamlit as st
from backend.utils.csv_loader import load_trace
from database.db import count_runs

ROOT = Path(__file__).parent
DATA = ROOT / "data"

DEFAULT_CONFIG = {
    "l1_size": 1024, "l2_size": 8192, "block_size": 16, "associativity": 2,
    "l1_latency": 1, "l2_latency": 8, "memory_latency": 100
}

def initialize_state():
    if "config" not in st.session_state:
        st.session_state.config = DEFAULT_CONFIG.copy()
    if "trace" not in st.session_state:
        trace, _ = load_trace(DATA / "sequential_trace.csv")
        st.session_state.trace = trace
        st.session_state.dataset_name = "Sequential sample"
        st.session_state.trace_source = "sample"
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "comparison" not in st.session_state:
        st.session_state.comparison = None
    st.session_state.history_count = count_runs()

def apply_theme():
    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def sidebar_status():
    st.sidebar.markdown("### WORKSPACE")
    st.sidebar.markdown(f"**Trace:** {st.session_state.dataset_name}")
    st.sidebar.markdown(f"**Accesses:** {len(st.session_state.trace):,}")
    cfg = st.session_state.config
    st.sidebar.markdown(f"**L1 / L2:** {cfg['l1_size']} B / {cfg['l2_size']} B")
    st.sidebar.markdown(f"**Block:** {cfg['block_size']} B · **Ways:** {cfg['associativity']}")
    st.sidebar.markdown("---")
    st.sidebar.caption("CacheLab · Trace-driven COA simulator")
