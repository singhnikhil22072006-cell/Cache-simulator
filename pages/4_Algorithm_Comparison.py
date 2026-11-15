import streamlit as st
import pandas as pd
import plotly.express as px
from shared import apply_theme, initialize_state, sidebar_status
from backend.core.simulator import simulate, POLICIES

st.set_page_config(page_title="Algorithm Comparison | CacheLab", page_icon="⚖️", layout="wide")
apply_theme(); initialize_state(); sidebar_status()
st.title("Algorithm comparison")
st.caption("All four policies run against the same active trace and cache configuration.")
st.write(f"**Dataset:** {st.session_state.dataset_name} · **Accesses:** {len(st.session_state.trace):,}")
if st.button("Compare all algorithms", type="primary", use_container_width=True):
    try:
        results = [simulate(st.session_state.trace, st.session_state.config, p) for p in POLICIES]
        st.session_state.comparison = results
        st.success("All algorithms completed on the same input.")
    except Exception as exc:
        st.error(str(exc))
results = st.session_state.comparison
if results:
    records = []
    for r in results:
        m=r["metrics"]
        records.append({"Algorithm":r["policy"],"Hit count":m["overall_hits"],"Miss count":m["memory_misses"],
                        "Hit rate (%)":m["overall_hit_rate"]*100,"Miss rate (%)":m["overall_miss_rate"]*100,
                        "AMAT (cycles)":m["amat"],"Total accesses":m["total_accesses"]})
    df=pd.DataFrame(records)
    best=df.loc[df["AMAT (cycles)"].idxmin(),"Algorithm"]
    st.success(f"Lowest AMAT for this trace and configuration: {best} ({df['AMAT (cycles)'].min():.2f} cycles).")
    st.dataframe(df.round(3),use_container_width=True,hide_index=True)
    c1,c2=st.columns(2)
    with c1:
        fig=px.bar(df,x="Algorithm",y="AMAT (cycles)",title="Average memory access time",text_auto=".2f")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#d9e8f7")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        long=df.melt(id_vars="Algorithm",value_vars=["Hit rate (%)","Miss rate (%)"],var_name="Metric",value_name="Rate")
        fig=px.bar(long,x="Algorithm",y="Rate",color="Metric",barmode="group",title="Hit and miss rates")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#d9e8f7")
        st.plotly_chart(fig,use_container_width=True)
    st.download_button("Download comparison CSV",df.to_csv(index=False).encode(),"algorithm_comparison.csv","text/csv")
else:
    st.info("Run the comparison to populate charts with actual simulation results.")
