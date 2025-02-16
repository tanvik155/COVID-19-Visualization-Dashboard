import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ Streamlit UI ------------------ #
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

st.title("🦠 COVID-19 Global Dashboard")
st.write("Real-time COVID-19 statistics and visualizations.")

# ------------------ Fetch COVID-19 Data ------------------ #
@st.cache_data
def get_covid_data():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Failed to fetch data. Please try again later.")
        return None

data = get_covid_data()

# ------------------ Sidebar for Country Selection ------------------ #
st.sidebar.title("🌍 Select Country")
countries = ["Global"] + sorted(data["country"].unique().tolist())
selected_country = st.sidebar.selectbox("Choose a country:", countries)

# ------------------ Display COVID-19 Statistics ------------------ #
if selected_country == "Global":
    url_global = "https://disease.sh/v3/covid-19/all"
    global_data = requests.get(url_global).json()

    st.markdown("### 🌎 Global COVID-19 Statistics")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("🦠 Total Cases", f"{global_data['cases']:,}")
    col2.metric("☠️ Total Deaths", f"{global_data['deaths']:,}")
    col3.metric("✅ Total Recovered", f"{global_data['recovered']:,}")
    
else:
    country_data = data[data["country"] == selected_country].iloc[0]

    st.markdown(f"### {country_data['country']} COVID-19 Statistics")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("🦠 Total Cases", f"{country_data['cases']:,}")
    col2.metric("☠️ Total Deaths", f"{country_data['deaths']:,}")
    col3.metric("✅ Total Recovered", f"{country_data['recovered']:,}")

# ------------------ Data Visualization ------------------ #
st.markdown("## 📊 COVID-19 Data Visualization")

# 🔹 Bar Chart: Cases, Deaths, Recoveries
fig1 = px.bar(data, x="country", y=["cases", "deaths", "recovered"], title="COVID-19 Cases by Country",
              labels={"value": "Count", "variable": "Category"}, barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# 🔹 Pie Chart: Cases Distribution
st.markdown("### 🏥 COVID-19 Cases Distribution")
fig2 = px.pie(values=[global_data["cases"], global_data["deaths"], global_data["recovered"]],
              names=["Cases", "Deaths", "Recovered"],
              title="Global COVID-19 Cases Distribution",
              color_discrete_sequence=["blue", "red", "green"])
st.plotly_chart(fig2, use_container_width=True)

# 🔹 Top 10 Most Affected Countries
top_10 = data.nlargest(10, "cases")[["country", "cases", "deaths", "recovered"]]

fig3, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y=top_10["country"], x=top_10["cases"], palette="Blues_r", ax=ax)
ax.set_title("Top 10 Most Affected Countries")
st.pyplot(fig3)

st.sidebar.info("📢 Data Source: [Disease.sh API](https://disease.sh)")

st.success("✅ Dashboard Updated! Choose a different country from the sidebar.")
