import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Kelly Criterion Planner",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for iPad/Retina Look
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Card styling */
    .metric-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    .hero-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Typography */
    .hero-title {
        font-size: 0.875rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .hero-value {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0.5rem 0;
        color: #60A5FA;
    }
    
    .bilingual-label {
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 0.25rem;
    }
    </style>
    """, unsafe_allow_value=True)

# 3. Sidebar Inputs
with st.sidebar:
    st.title("🎯 Parameters / 参数")
    st.markdown("---")
    
    funds = st.number_input("Available Funds / 可用资金", min_value=0.0, value=1000000.0, step=1000.0, format="%.2f")
    
    st.markdown("### Price Levels / 价格位")
    entry = st.number_input("Entry Price / 入场价", min_value=0.001, value=2.795, format="%.3f")
    target = st.number_input("Target Price / 止盈价", min_value=0.001, value=3.119, format="%.3f")
    stop = st.number_input("Stop-Loss / 止损价", min_value=0.001, value=2.498, format="%.3f")
    
    st.markdown("### Probability / 胜率")
    win_rate = st.slider("Win Probability (%) / 预测胜率", 1, 99, 80)
    
    st.markdown("### Strategy / 策略")
    risk_mode = st.select_slider(
        "Kelly Fraction / 凯利比例",
        options=[0.25, 0.5, 1.0],
        value=1.0,
        format_func=lambda x: "Full (1.0)" if x==1 else ("Half (0.5)" if x==0.5 else "Quarter (0.25)")
    )

# 4. Logic Calculations
p = win_rate / 100.0
q = 1.0 - p
gain_per_share = target - entry
loss_per_share = entry - stop

if gain_per_share <= 0 or loss_per_share <= 0:
    st.error("❌ Invalid Price Configuration: Target > Entry > Stop-Loss required.")
else:
    b = gain_per_share / loss_per_share
    raw_f = (p * b - q) / b
    kelly_f = max(0, raw_f)
    adjusted_f = kelly_f * risk_mode
    
    investment = funds * adjusted_f
    shares = int(investment / entry)
    total_profit = shares * gain_per_share
    total_loss = shares * loss_per_share

    # 5. Main Content Rendering
    st.title("Kelly Criterion Planner")
    st.markdown(f"**Strategy:** {risk_mode} Kelly | **Reward/Risk (b):** {b:.3f}")

    # Hero Section
    st.markdown(f"""
        <div class="hero-card">
            <div class="hero-title">Suggested Investment / 建议投入金额</div>
            <div class="hero-value">${investment:,.2f}</div>
            <div style="display: flex; gap: 20px; margin-top: 10px;">
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Allocation</div>
                    <div style="font-size: 1.5rem; font-weight: 700;">{adjusted_f*100:.2f}%</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Shares</div>
                    <div style="font-size: 1.5rem; font-weight: 700;">{shares:,}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_value=True)

    # P&L Projection Columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="color: #10B981; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">Potential Profit / 潜在利润</div>
                <div style="font-size: 2rem; font-weight: 900; color: #1E293B; margin: 0.5rem 0;">${total_profit:,.2f}</div>
                <div style="color: #10B981; font-size: 0.875rem; font-weight: 600;">+{gain_per_share:.3f} per share</div>
            </div>
        """, unsafe_allow_value=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="color: #EF4444; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">Potential Loss / 潜在亏损</div>
                <div style="font-size: 2rem; font-weight: 900; color: #1E293B; margin: 0.5rem 0;">${total_loss:,.2f}</div>
                <div style="color: #EF4444; font-size: 0.875rem; font-weight: 600;">-{loss_per_share:.3f} per share</div>
            </div>
        """, unsafe_allow_value=True)

    # Footer Info
    if raw_f <= 0:
        st.warning("⚠️ **Negative Edge:** The math suggests skipping this trade. / 数学优势为负，建议放弃交易。")
    else:
        st.info(f"""
        **Pro Tip:** While the Kelly Criterion suggests **{adjusted_f*100:.2f}%**, most professional portfolio managers cap single trades at 10-20% to manage volatility.
        
        **专业提示：** 虽然凯利公式建议投入 **{adjusted_f*100:.2f}%**，但大多数专业基金经理会将单笔交易限制在 10-20% 以控制波动。
        """)
