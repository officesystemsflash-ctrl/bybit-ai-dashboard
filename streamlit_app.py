import streamlit as st
from supabase import create_client
import pandas as pd

st.set_page_config(page_title="Bybit AI Bot Dashboard", layout="wide")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🤖 Bybit AI Trading Bot Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["Trades", "Orders", "Signals", "Stats"])

def load_table(table: str, order_col: str):
    try:
        res = supabase.table(table).select("*").order(order_col, desc=True).limit(500).execute()
        data = res.data or []
        if not data:
            return None
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading {table}: {e}")
        return None

# ===== TRADES =====
with tab1:
    st.subheader("Trades (ultimele 500)")
    df = load_table("trades", "open_ts")
    if df is None:
        st.info("Nu sunt trades încă.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export Trades CSV", csv, "trades.csv", "text/csv")

# ===== ORDERS =====
with tab2:
    st.subheader("Orders (ultimele 500)")
    df = load_table("orders", "ts")
    if df is None:
        st.info("Nu sunt orders încă.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export Orders CSV", csv, "orders.csv", "text/csv")

# ===== SIGNALS =====
with tab3:
    st.subheader("Signals (ultimele 500)")
    df = load_table("signals", "ts")
    if df is None:
        st.info("Nu sunt signals încă.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export Signals CSV", csv, "signals.csv", "text/csv")

# ===== STATS =====
with tab4:
    st.subheader("Statistici rapide")
    try:
        trades = supabase.table("trades").select("pnl_usdt").execute().data or []
        total_trades = len(trades)
        total_pnl = sum(float(t.get("pnl_usdt") or 0) for t in trades)
        wins = len([t for t in trades if float(t.get("pnl_usdt") or 0) > 0])
        winrate = (wins / total_trades * 100) if total_trades else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Trades", total_trades)
        c2.metric("Total PnL (USDT)", f"{total_pnl:.2f}")
        c3.metric("Winrate", f"{winrate:.1f}%")
    except Exception as e:
        st.error(f"Eroare la stats: {e}")
