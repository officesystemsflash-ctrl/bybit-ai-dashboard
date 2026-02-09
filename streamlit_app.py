import streamlit as st
from supabase import create_client
import pandas as pd
import os

st.set_page_config(page_title="Bybit AI Bot Dashboard", layout="wide")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🤖 Bybit AI Trading Bot Dashboard")

tab1, tab2, tab3 = st.tabs(["Trades", "Signals", "Statistics"])

# ================= TRADES =================
with tab1:
    st.subheader("Trades History")

    data = supabase.table("trades").select("*").order("created_at", desc=True).execute()

    if data.data:
        df = pd.DataFrame(data.data)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export CSV", csv, "trades.csv", "text/csv")
    else:
        st.info("No trades yet.")

# ================= SIGNALS =================
with tab2:
    st.subheader("Signals History")

    data = supabase.table("signals").select("*").order("created_at", desc=True).execute()

    if data.data:
        df = pd.DataFrame(data.data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No signals yet.")

# ================= STATS =================
with tab3:
    st.subheader("Statistics")

    trades = supabase.table("trades").select("*").execute().data or []

    total_trades = len(trades)
    total_pnl = sum(t.get("pnl", 0) for t in trades)
    wins = len([t for t in trades if t.get("pnl", 0) > 0])

    winrate = (wins / total_trades * 100) if total_trades else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trades", total_trades)
    col2.metric("Total PnL", f"${total_pnl:.2f}")
    col3.metric("Winrate", f"{winrate:.1f}%")
