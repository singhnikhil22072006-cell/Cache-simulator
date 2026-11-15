import streamlit as st
from shared import apply_theme, initialize_state, sidebar_status

st.set_page_config(page_title="CacheLab | Memory Intelligence", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")
apply_theme()
initialize_state()

st.sidebar.markdown("# 🧠 CacheLab")
st.sidebar.caption("MEMORY INTELLIGENCE PLATFORM")
st.sidebar.markdown("---")
st.sidebar.markdown("Use the pages in this sidebar to explore the cache hierarchy, run simulations, compare policies, and inspect history.")
sidebar_status()

st.markdown("""
<div class="hero">
  <div class="eyebrow">COMPUTER ORGANIZATION & ARCHITECTURE</div>
  <h1>Dynamic Multi-Level Cache<br><span>Optimization & Prediction</span></h1>
  <p>Explore memory hierarchy behavior with trace-driven simulation, transparent metrics, and practical access-pattern analysis.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Start exploring")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="panel"><div class="panel-icon">⚡</div><h3>Simulate</h3><p>Run every memory reference through L1, L2, and main memory with configurable cache geometry.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="panel"><div class="panel-icon">📊</div><h3>Compare</h3><p>Evaluate FIFO, LRU, LFU, and adaptive replacement on the exact same trace.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="panel"><div class="panel-icon">🔎</div><h3>Predict</h3><p>Detect sequential, stride, repeated, loop-like, and irregular access patterns.</p></div>', unsafe_allow_html=True)

st.markdown("### Current workspace")
a, b, c = st.columns(3)
a.metric("Trace accesses", f"{len(st.session_state.trace):,}")
b.metric("Dataset", st.session_state.dataset_name)
c.metric("Saved simulations", str(st.session_state.history_count))
st.info("Tip: Open **Cache Simulator** to upload a CSV or choose one of the five included sample traces. Your selected trace and configuration are shared across all pages.")
