import streamlit as st
import pandas as pd
from shared import apply_theme, initialize_state, sidebar_status
from backend.prediction.predictor import analyze_trace

st.set_page_config(page_title="Memory Prediction | CacheLab", page_icon="🔎", layout="wide")
apply_theme(); initialize_state(); sidebar_status()
st.title("Memory access prediction")
st.caption("Lightweight mathematical heuristics over your active memory trace.")
result=analyze_trace(st.session_state.trace,st.session_state.config["block_size"])
a,b,c=st.columns(3)
a.metric("Detected pattern",result["pattern"])
b.metric("Most common stride", "N/A" if result["stride"] is None else f"{result['stride']} blocks")
c.metric("Prediction confidence",f"{result['confidence']*100:.1f}%")
if result["next"] is not None:
    st.metric("Predicted next address",f"0x{result['next']:X}")
else:
    st.metric("Predicted next address","No reliable estimate")
st.markdown("### Frequently accessed blocks")
if result["frequent"]:
    st.dataframe(pd.DataFrame(result["frequent"]),use_container_width=True,hide_index=True)
st.caption(result["details"])
st.markdown("### Pattern interpretation")
explanations={
"Sequential":"Consecutive memory blocks are accessed in order. Hardware prefetchers often benefit from this locality.",
"Stride-based":"A repeated non-zero difference between consecutive block numbers was detected.",
"Repeated access":"A small set of blocks accounts for a large share of references.",
"Loop-based":"A recent block sequence repeats, suggesting a loop-like working set.",
"Random / irregular":"No strong regular pattern was detected using the selected heuristics."
}
st.write(explanations.get(result["pattern"],"Load a trace to begin."))
