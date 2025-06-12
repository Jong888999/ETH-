import streamlit as st

st.set_page_config(page_title="ETH 套利回本计算器", layout="centered")

st.title("ETH 套利回本价格计算器")
st.markdown("""
本工具用于计算在 aivora 和 bitunix 双平台套利时，综合手续费返还和体验金后，ETH 的回本价格。
""")

# 默认参数
defaults = {
    'eth_price': 3500.0,
    'position': 1.0,
    'leverage': 10,
    'margin': 350.0,
    'fee_rate': 0.0005,
    'aivora_fee_rebate': 0.85,
    'bitunix_fee_rebate': 0.80,
    'aivora_loss_rebate': 0.3,
    'direction': 'long',
}

with st.form("input_form"):
    eth_price = st.number_input("ETH 开仓价 (USD)", value=defaults['eth_price'], min_value=0.0, step=0.01)
    position = st.number_input("仓位 (ETH 数量)", value=defaults['position'], min_value=0.01, step=0.01)
    leverage = st.number_input("杠杆倍数", value=defaults['leverage'], min_value=1, step=1)
    margin = st.number_input("保证金 (USD)", value=defaults['margin'], min_value=0.0, step=0.01)
    direction = st.selectbox("aivora 方向", ["long", "short"], index=0, format_func=lambda x: "做多" if x=="long" else "做空")
    submitted = st.form_submit_button("计算回本价格")

if submitted:
    fee_rate = defaults['fee_rate']
    aivora_fee_rebate = defaults['aivora_fee_rebate']
    bitunix_fee_rebate = defaults['bitunix_fee_rebate']
    aivora_loss_rebate = defaults['aivora_loss_rebate']

    # 1. 手续费
    aivora_fee = position * eth_price * fee_rate
    bitunix_fee = position * eth_price * fee_rate
    total_fee = aivora_fee + bitunix_fee

    # 2. 返佣
    aivora_rebate = aivora_fee * aivora_fee_rebate
    bitunix_rebate = bitunix_fee * bitunix_fee_rebate
    total_rebate = aivora_rebate + bitunix_rebate

    # 3. 回本亏损
    X = (total_fee - total_rebate) / aivora_loss_rebate
    delta_p = X / position

    if direction == 'long':
        break_even_price = eth_price - delta_p
        move = "下跌"
    else:
        break_even_price = eth_price + delta_p
        move = "上涨"

    st.success(f"回本价格：${break_even_price:,.2f}")
    st.markdown(f"**ETH 需要{move} {abs(delta_p):.2f} 美元（{(abs(delta_p)/eth_price)*100:.2f}%）才能回本**")

    with st.expander("费用明细"):
        st.write(f"aivora 手续费: ${aivora_fee:,.2f}")
        st.write(f"bitunix 手续费: ${bitunix_fee:,.2f}")
        st.write(f"手续费总计: ${total_fee:,.2f}")
        st.write(f"aivora 返佣: ${aivora_rebate:,.2f}")
        st.write(f"bitunix 返佣: ${bitunix_rebate:,.2f}")
        st.write(f"返佣总计: ${total_rebate:,.2f}")
        st.write(f"aivora 亏损返体验金比例: {aivora_loss_rebate*100:.1f}%")
        st.write(f"回本时 aivora 亏损: ${X:,.2f}") 