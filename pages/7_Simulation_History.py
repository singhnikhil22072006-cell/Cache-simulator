import streamlit as st
import pandas as pd
import json
from shared import apply_theme, initialize_state, sidebar_status
from database.db import list_runs, get_run

st.set_page_config(page_title="Simulation History | CacheLab", page_icon="🗂️", layout="wide")
apply_theme(); initialize_state(); sidebar_status()
st.title("Simulation history")
st.caption("Completed simulations are stored locally in SQLite.")
runs=list_runs()
if not runs:
    st.info("No saved simulations yet. Run a simulation from the Cache Simulator page.")
else:
    display=[]
    for r in runs:
        m=json.loads(r["metrics"]); cfg=json.loads(r["config"])
        display.append({"ID":r["id"],"Date / time":r["created_at"],"Dataset":r["dataset"],"Algorithm":r["policy"],
                        "L1 / L2":f"{cfg['l1_size']} / {cfg['l2_size']} B",
                        "Hit rate":f"{m['overall_hit_rate']*100:.2f}%","Miss rate":f"{m['overall_miss_rate']*100:.2f}%",
                        "AMAT":f"{m['amat']:.2f} cycles"})
    st.dataframe(pd.DataFrame(display),use_container_width=True,hide_index=True)
    selected=st.selectbox("View saved simulation", [r["id"] for r in runs])
    record=get_run(selected)
    if record:
        metrics=json.loads(record["metrics"]); rows=json.loads(record["rows_json"])
        st.markdown(f"### Simulation #{selected} · {record['dataset']}")
        c1,c2,c3=st.columns(3)
        c1.metric("Overall hit rate",f"{metrics['overall_hit_rate']*100:.2f}%")
        c2.metric("Main-memory miss rate",f"{metrics['overall_miss_rate']*100:.2f}%")
        c3.metric("AMAT",f"{metrics['amat']:.2f} cycles")
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        st.download_button("Export saved access report",pd.DataFrame(rows).to_csv(index=False).encode(),f"simulation_{selected}.csv","text/csv")
