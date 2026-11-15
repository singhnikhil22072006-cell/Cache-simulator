import streamlit as st
from shared import apply_theme, initialize_state, sidebar_status
from backend.core.simulator import validate_config

st.set_page_config(page_title="Configuration | CacheLab", page_icon="🛠️", layout="wide")
apply_theme(); initialize_state(); sidebar_status()
st.title("Cache configuration")
st.caption("Configure cache geometry and access latency. Changes apply to future simulations.")
cfg = st.session_state.config.copy()
with st.form("config_form"):
    a,b = st.columns(2)
    with a:
        st.markdown("### Cache geometry")
        l1 = st.number_input("L1 cache size (bytes)", min_value=16, max_value=1_048_576, value=int(cfg["l1_size"]), step=16)
        l2 = st.number_input("L2 cache size (bytes)", min_value=16, max_value=16_777_216, value=int(cfg["l2_size"]), step=16)
        block = st.selectbox("Block size (bytes)", [4,8,16,32,64,128], index=[4,8,16,32,64,128].index(cfg["block_size"]) if cfg["block_size"] in [4,8,16,32,64,128] else 2)
        ways = st.selectbox("Associativity (ways)", [1,2,4,8], index=[1,2,4,8].index(cfg["associativity"]) if cfg["associativity"] in [1,2,4,8] else 1)
    with b:
        st.markdown("### Access latency")
        l1lat = st.number_input("L1 access latency (cycles)", min_value=1, max_value=100, value=int(cfg["l1_latency"]))
        l2lat = st.number_input("L2 access latency (cycles)", min_value=1, max_value=500, value=int(cfg["l2_latency"]))
        memlat = st.number_input("Main memory latency (cycles)", min_value=1, max_value=2000, value=int(cfg["memory_latency"]))
        st.info("Latency values are modeled cycle costs. They are inputs to the AMAT calculation, not measured hardware timings.")
    submitted = st.form_submit_button("Save configuration", type="primary", use_container_width=True)
if submitted:
    candidate = {"l1_size":int(l1),"l2_size":int(l2),"block_size":int(block),"associativity":int(ways),
                 "l1_latency":int(l1lat),"l2_latency":int(l2lat),"memory_latency":int(memlat)}
    try:
        validate_config(candidate)
        st.session_state.config = candidate
        st.session_state.last_result = None
        st.success("Configuration saved. Run a new simulation to refresh all metrics.")
    except ValueError as exc:
        st.error(str(exc))
st.markdown("### Parameter guide")
st.markdown("- **Cache size:** Total data capacity of the cache level.\n- **Block size:** Number of bytes transferred as one cache line.\n- **Associativity:** Number of candidate lines in each set. `1` is direct-mapped; equal to total lines is fully associative.\n- **Latency:** Time cost, in modeled clock cycles, to access that level.")
