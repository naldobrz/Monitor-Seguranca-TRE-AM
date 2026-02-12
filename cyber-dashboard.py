import streamlit as st
import pandas as pd
import plotly.express as px
import glob
from datetime import datetime
import os

st.set_page_config(page_title="Monitor de Segurança - TRE-AM", layout="wide")
st.title("🛡 Monitor de Segurança - TRE-AM")
st.markdown("**Dashboard de Cibersegurança para TRE-AM**")

@st.cache_data(ttl=300)
def load_data():
    csv_files = glob.glob("/workspace/cyber-alerts-*.csv")
    if not csv_files:
        return pd.DataFrame()
    df = pd.concat([pd.read_csv(f) for f in csv_files[-7:]], ignore_index=True)
    return df

df = load_data()

if df.empty:
    st.info("📊 Aguardando dados do agente cyber-monitor...")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("🔴 Total CVEs", len(df))
col2.metric("🚨 Críticas", len(df[df.get('CVSS', 0) >= 9.0]))
col3.metric("⚠️ Altas", len(df[(df.get('CVSS', 0) >= 7.0) & (df.get('CVSS', 0) < 9.0)]))

st.subheader("📋 Vulnerabilidades Detectadas")
st.dataframe(df, use_container_width=True)

if not df.empty:
    fig = px.line(df, x='Data' if 'Data' in df else df.columns, y='CVSS' if 'CVSS' in df else df.columns[1], title="📈 Evolução Riscos")
    st.plotly_chart(fig, use_container_width=True)

st.caption("🛡 Monitor de Segurança TRE-AM | Alimentado pelo agente cyber-monitor-tribunal")
