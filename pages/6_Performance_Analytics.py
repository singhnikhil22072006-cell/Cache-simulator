import streamlit as st
import pandas as pd
import plotly.express as px
from shared import apply_theme, initialize_state, sidebar_status
from backend.core.simulator import simulate, POLICIES

st.set_page_config(page_title="Performance Analytics | CacheLab", page_icon="📈", layout="wide")
apply_theme(); initialize_state(); sidebar_status()
st.title("Performance analytics")
st.caption("Charts are generated from real simulations of the active trace.")
if st.session_state.last_result is None:
    st.info("No single-policy simulation saved in this session yet. Running an LRU baseline for this view.")
    baseline=simulate(st.session_state.trace,st.session_state.config,"LRU")
else: baseline=st.session_state.last_result
m=baseline["metrics"]
if st.session_state.comparison is None:
    comp=[simulate(st.session_state.trace,st.session_state.config,p) for p in POLICIES]
else: comp=st.session_state.comparison
summary=pd.DataFrame([{"Level":"L1 hits","Count":m["l1_hits"]},{"Level":"L2 hits","Count":m["l2_hits"]},{"Level":"Main memory","Count":m["memory_misses"]}])
a,b=st.columns(2)
with a:
    fig=px.pie(summary,names="Level",values="Count",hole=.55,title="Access outcome distribution")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#d9e8f7")
    st.plotly_chart(fig,use_container_width=True)
with b:
    levels=pd.DataFrame([{"Metric":"L1 hit rate","Rate":m["l1_hit_rate"]*100},{"Metric":"L1 miss rate","Rate":m["l1_miss_rate"]*100},
                         {"Metric":"L2 conditional hit rate","Rate":m["l2_conditional_hit_rate"]*100},
                         {"Metric":"L2 conditional miss rate","Rate":m["l2_conditional_miss_rate"]*100}])
    fig=px.bar(levels,x="Metric",y="Rate",title="Level hit / miss rates (%)")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#d9e8f7")
    st.plotly_chart(fig,use_container_width=True)
st.markdown("### AMAT by replacement policy")
amat=pd.DataFrame([{"Algorithm":r["policy"],"AMAT (cycles)":r["metrics"]["amat"]} for r in comp])
fig=px.bar(amat,x="Algorithm",y="AMAT (cycles)",text_auto=".2f")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#d9e8f7")
st.plotly_chart(fig,use_container_width=True)
st.caption(f"Single-policy metrics above use {baseline['policy']}; policy comparison uses the same active trace and configuration.")
