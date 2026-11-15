import streamlit as st
import pandas as pd
from shared import apply_theme, initialize_state, sidebar_status, DATA
from backend.utils.csv_loader import load_trace
from backend.core.simulator import simulate, POLICIES
from database.db import save_run

st.set_page_config(page_title="Cache Simulator | CacheLab", page_icon="⚙️", layout="wide")
apply_theme(); initialize_state(); sidebar_status()
st.title("Cache simulator")
st.caption("Load a memory reference trace, choose a policy, and inspect every access.")

left,right = st.columns([1,1])
with left:
    sample = st.selectbox("Sample trace", ["Sequential sample","Random sample","Repeated sample","Loop-based sample","Stride-based sample"])
    sample_files = {"Sequential sample":"sequential_trace.csv","Random sample":"random_trace.csv","Repeated sample":"repeated_trace.csv","Loop-based sample":"loop_based_trace.csv","Stride-based sample":"stride_based_trace.csv"}
    if st.button("Load selected sample", use_container_width=True):
        trace,_ = load_trace(DATA/sample_files[sample])
        st.session_state.trace, st.session_state.dataset_name = trace, sample
        st.session_state.trace_source = "sample"
        st.session_state.last_result = None
        st.success(f"Loaded {len(trace)} accesses.")
with right:
    uploaded = st.file_uploader("Upload your CSV trace", type=["csv"], help="Required address column: address, memory_address, or access_address.")
    if uploaded is not None and st.button("Use uploaded CSV", use_container_width=True):
        try:
            trace, frame = load_trace(uploaded)
            st.session_state.trace = trace
            st.session_state.dataset_name = uploaded.name
            st.session_state.trace_source = "upload"
            st.session_state.last_result = None
            st.success(f"Loaded {len(trace)} addresses from {uploaded.name}.")
        except ValueError as exc:
            st.error(str(exc))

st.markdown("### Active trace")
trace = st.session_state.trace
st.write(f"**{st.session_state.dataset_name}** · {len(trace):,} memory accesses · {len(set(trace)):,} unique addresses")
preview = pd.DataFrame({"access_no":range(1,min(len(trace),12)+1),"address":[f"0x{x:X}" for x in trace[:12]],"decimal":trace[:12]})
st.dataframe(preview, use_container_width=True, hide_index=True)
policy = st.selectbox("Replacement algorithm", POLICIES, index=1)
if st.button("▶ Run cache simulation", type="primary", use_container_width=True):
    try:
        result = simulate(trace, st.session_state.config, policy)
        st.session_state.last_result = result
        run_id = save_run(st.session_state.dataset_name, result)
        st.session_state.history_count += 1
        st.success(f"Simulation completed and saved to history (ID {run_id}).")
    except Exception as exc:
        st.error(f"Simulation could not run: {exc}")

result = st.session_state.last_result
if result:
    m = result["metrics"]
    st.markdown("### Simulation results")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("L1 hit rate",f"{m['l1_hit_rate']*100:.2f}%")
    c2.metric("L2 conditional hit rate",f"{m['l2_conditional_hit_rate']*100:.2f}%")
    c3.metric("Memory miss rate",f"{m['overall_miss_rate']*100:.2f}%")
    c4.metric("AMAT",f"{m['amat']:.2f} cycles")
    df = result["dataframe"]
    st.dataframe(df[["access_no","address","block","set","tag","l1","l2","main_memory","l1_evicted","l2_evicted"]], use_container_width=True, hide_index=True)
    st.download_button("Download access-by-access results", df.to_csv(index=False).encode(), "cache_simulation_results.csv", "text/csv")
