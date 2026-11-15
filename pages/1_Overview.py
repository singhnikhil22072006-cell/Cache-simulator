import streamlit as st
import plotly.graph_objects as go
from shared import apply_theme, initialize_state, sidebar_status
from backend.core.simulator import simulate

st.set_page_config(page_title="Overview | CacheLab", page_icon="📊", layout="wide")
apply_theme(); initialize_state(); sidebar_status()
st.title("Overview dashboard")
st.caption("A live snapshot of your current trace and cache hierarchy.")

if st.session_state.last_result is None:
    result = simulate(st.session_state.trace, st.session_state.config, "LRU")
else:
    result = st.session_state.last_result
m = result["metrics"]
cols = st.columns(4)
cols[0].metric("Memory accesses", f"{m['total_accesses']:,}")
cols[1].metric("L1 hit rate", f"{m['l1_hit_rate']*100:.2f}%")
cols[2].metric("Main-memory miss rate", f"{m['overall_miss_rate']*100:.2f}%")
cols[3].metric("AMAT", f"{m['amat']:.2f} cycles")
st.markdown("### Memory hierarchy")
fig = go.Figure()
labels = ["CPU", "L1 CACHE", "L2 CACHE", "MAIN MEMORY"]
sub = ["Request generator", f"{st.session_state.config['l1_size']} B · fastest", f"{st.session_state.config['l2_size']} B · larger", f"{st.session_state.config['memory_latency']} cycle penalty"]
for i,(label,desc) in enumerate(zip(labels,sub)):
    fig.add_trace(go.Scatter(x=[i], y=[0], mode="markers+text", marker=dict(size=70, color=["#4fc3e8","#2789b7","#176184","#334b65"][i], line=dict(width=2,color="#8adcf0")), text=[label], textposition="middle center", textfont=dict(color="white",size=12), hovertext=desc, hoverinfo="text", showlegend=False))
fig.add_trace(go.Scatter(x=[0,1,2,3],y=[0,0,0,0],mode="lines",line=dict(color="#4b7894",width=3),showlegend=False))
fig.update_layout(height=220, xaxis=dict(visible=False,range=[-.5,3.5]), yaxis=dict(visible=False,range=[-.5,.5]), margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig,use_container_width=True)
a,b = st.columns(2)
with a:
    st.markdown("### How each level works")
    st.markdown("- **L1:** Smallest and fastest cache, checked first.\n- **L2:** Larger secondary cache, checked after an L1 miss.\n- **Main memory:** Largest storage; accessed when both caches miss.")
with b:
    st.markdown("### Current simulation")
    st.write(f"Replacement policy: **{result['policy']}**")
    st.write(f"L1 hits: **{m['l1_hits']:,}** · L1 misses: **{m['l1_misses']:,}**")
    st.write(f"L2 hits after L1 miss: **{m['l2_hits']:,}**")
    st.write(f"Main-memory accesses: **{m['memory_misses']:,}**")
st.info("The overview uses your last completed simulation; before the first run, it computes an LRU baseline from the active trace.")
