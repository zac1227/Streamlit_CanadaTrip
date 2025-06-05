import streamlit as st
import requests

st.set_page_config(page_title="出國前行李整理", layout="wide")

api_key = st.secrets["weatherapi"]["api_key"]

cities = ["Vancouver", "Victoria", "Tofino", "Whistler", "Kamloops", "Banff", "Lake Louise", "Jasper", "Kelowna"]

st.title("🇨🇦 出國前行李整理與城鎮的氣象預測")

# === 行李 Check List ===
with st.expander("🧳 點開查看行李 Check List"):
    clothes = ["厚外套", "長袖衣物", "短袖衣物", "防水鞋", "毛帽", "手套"]
    electronics = ["手機", "充電器", "行動電源", "耳機", "插座", "電熱壺"]
    documents = ["護照", "機票", "保險文件", "加拿大 ETA", "住宿確認單","國際駕照"]
    others = ["防曬乳","保養品", "墨鏡", "水壺", "背包", "雨傘"]
    medicine = ["胃藥","止痛藥","感冒藥"]
    st.subheader("👕 衣物")
    for item in clothes:
        st.checkbox(item)

    st.subheader("📸 電子用品")
    for item in electronics:
        st.checkbox(item)

    st.subheader("📄 證件與文件")
    for item in documents:
        st.checkbox(item)
    st.subheader("🌟 常備藥物")
    for item in medicine:
        st.checkbox(item)
    st.subheader("🌟 其他")
    for item in others:
        st.checkbox(item)
    
# === 天氣總表 ===
st.header("🌤 各城市未來 3 天平均 + 穿搭提醒")

for city in cities:
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3&aqi=no&alerts=no"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast_days = data["forecast"]["forecastday"]

        max_temps = [day["day"]["maxtemp_c"] for day in forecast_days]
        min_temps = [day["day"]["mintemp_c"] for day in forecast_days]
        daily_diffs = [day["day"]["maxtemp_c"] - day["day"]["mintemp_c"] for day in forecast_days]

        avg_max = round(sum(max_temps) / len(max_temps), 1)
        avg_min = round(sum(min_temps) / len(min_temps), 1)
        avg_diff = round(sum(daily_diffs) / len(daily_diffs), 1)

        st.subheader(f"📍 {city}")
        st.write(f"☀ 平均白天最高：{avg_max}°C")
        st.write(f"❄ 平均夜晚最低：{avg_min}°C")
        st.write(f"🌡 平均早晚溫差：{avg_diff}°C")

        # 穿搭提醒分色
        shown = False
        if avg_max >= 25:
            st.error("🔥 白天偏熱，請準備防曬、透氣衣物。")
            shown = True
        if avg_diff >= 10:
            st.warning("🌡 早晚溫差大，需多層次穿搭。")
            shown = True
        if avg_min <= 10:
            st.info("❄ 晚上偏冷，請攜帶厚外套、保暖裝備。")
            shown = True
        if not shown:
            st.success("✅ 氣溫穩定，標準旅行裝備即可。")
    else:
        st.error(f"⚠ 無法取得 {city} 的天氣資料")
