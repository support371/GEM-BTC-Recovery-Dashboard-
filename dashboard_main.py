import streamlit as st
import requests
import networkx as nx
from pyvis.network import Network
import tempfile
import os
from datetime import datetime

# ---------------------------------
# Header with GEM + BTC Branding
# ---------------------------------
st.markdown("""
<div style='display: flex; align-items: center; justify-content: center; gap: 20px; padding: 15px;'>
    <!-- Replace with your hosted GEM logo -->
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" width="70">
    <img src="https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg" width="70">
    <div>
        <h1 style='margin-bottom: 0;'>BTC Recovery & Tracking Dashboard</h1>
        <h4 style='margin-top: 0;'>Powered by GEM — Digital Asset Recovery & Compliance</h4>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

# Compliance notice
st.info("🔒 This platform adheres to strict KYC/AML standards. "
        "All recovery actions are logged, auditable, and subject to compliance review.")

# ---------------------------------
# Sidebar Navigation
# ---------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Recovery Phase", "$300 BTC Wallet Fraud Recovery"])

# ---------------------------------
# Page 1 - Recovery Phase
# ---------------------------------
if page == "Recovery Phase":
    st.title("🕵️ Recovery Phase — Locked Cases")
    st.write("These cases are marked for tracking but require compliance setup before analysis can begin.")

    # Case 1: Cash App Screenshot
    st.markdown("### 🚧 Case 1: Cash App Screenshot")
    st.info("This case is pending compliance setup. Please log in to the Recovery Portal to continue.")
    st.markdown(
        "[👉 Go to Recovery Profile](https://d5c428cd-8075-4caf-90f0-c548989ce06b-00-1l2b22r2zdduc.riker.replit.dev/){target='_blank'}",
        unsafe_allow_html=True
    )

    # Case 2: Sundew Scam
    st.markdown("### 🚧 Case 2: Sundew Scam")
    st.info("This case is pending compliance setup. Please log in to the Recovery Portal to continue.")
    st.markdown(
        "[👉 Go to Recovery Profile](https://d5c428cd-8075-4caf-90f0-c548989ce06b-00-1l2b22r2zdduc.riker.replit.dev/){target='_blank'}",
        unsafe_allow_html=True
    )

    st.warning("⚠️ These cases require login and specialist contact before tracking can begin.")

# ---------------------------------
# Page 2 - $300 BTC Wallet Fraud Recovery
# ---------------------------------
elif page == "$300 BTC Wallet Fraud Recovery":
    st.title("💰 $300 BTC Wallet Fraud Recovery Dashboard")

    # Case metadata
    st.markdown("""
    **Case ID:** GEM-0001  
    **Reported Loss:** ≈ $300 BTC send-out fraud  
    **Status:** 🟢 Active Investigation  
    """)

    st.write("This dashboard traces wallet transactions, detects exchanges/mixers, "
             "and applies compliance hold simulations.")

    # Input field for BTC Address / TXID
    address_or_txid = st.text_input("Enter a BTC Address or Transaction ID:")

    if st.button("Start Trace"):
        if not address_or_txid.strip():
            st.error("Please enter a valid BTC address or TXID.")
        else:
            st.success(f"✅ Tracing started for: {address_or_txid}")
            # Fetch data from Blockchair
            api_url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address_or_txid}"
            api_key = os.getenv("BLOCKCHAIR_API_KEY", "")
            headers = {"x-api-key": api_key} if api_key else {}
            try:
                resp = requests.get(api_url, headers=headers, timeout=15)
                resp.raise_for_status()
                data = resp.json()

                st.subheader("📊 Raw Transaction Data")
                st.json(data.get("data", {}))

                # --- Simple Graph Visualization ---
                G = nx.DiGraph()
                for addr, details in data.get("data", {}).items():
                    txs = details.get("transactions", [])
                    for tx in txs:
                        G.add_node(addr)
                        G.add_edge(addr, tx, weight=1)

                if G.number_of_nodes() > 0:
                    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")
                    net.from_nx(G)

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
                        net.save_graph(tmp_file.name)
                        st.components.v1.html(open(tmp_file.name, "r").read(), height=500)
                else:
                    st.warning("No transaction graph data found.")

            except Exception as e:
                st.error(f"Error fetching data: {e}")

    # Compliance Hold Simulation
    st.subheader("💼 Compliance Overlay Simulation")

    if "audit_log" not in st.session_state:
        st.session_state["audit_log"] = []

    if st.button("Withdraw"):
        st.error("⚠️ Withdrawal Pending — Compliance Review Required")
        st.markdown("> This withdrawal request is temporarily on hold pending compliance review.")
        st.write("Case ID: GEM-0001 — Audit log created.")

        # Append to audit log
        st.session_state["audit_log"].append(
            {"timestamp": datetime.utcnow().isoformat(), "action": "Withdraw Attempt", "status": "On Hold"}
        )

    # Display Audit Log
    if st.session_state["audit_log"]:
        st.subheader("📜 Audit Log")
        for log in st.session_state["audit_log"]:
            st.write(f"- {log['timestamp']} | {log['action']} → {log['status']}")
