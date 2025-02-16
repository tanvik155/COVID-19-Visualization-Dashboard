import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 🔹 Streamlit App Config
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide"
)

# 🔹 Function to Fetch Data
@st.cache_data
def fetch_data(url):
    """Fetch JSON data from API and handle errors."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# 🔹 Load Data
GLOBAL_API = "https://disease.sh/v3/covid-19/all"
COUNTRIES_API = "https://disease.sh/v3/covid-19/countries"

global_data = fetch_data(GLOBAL_API)
country_data = fetch_data(COUNTRIES_API)

# 🔹 Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["🌍 Global Overview", "📌 Country-wise Data", "📊 Data Table"])

# 🔹 Page: Global Overview
if page == "🌍 Global Overview":
    st.title("🌍 COVID-19 Global Overview")
    
    if global_data:
        col1, col2, col3 = st.columns(3)

        col1.metric("🦠 Total Cases", f"{global_data['cases']:,}")
        col2.metric("☠️ Total Deaths", f"{global_data['deaths']:,}")
        col3.metric("💪 Total Recovered", f"{global_data['recovered']:,}")

        # Pie Chart for Global Cases Distribution
        fig1 = px.pie(
            values=[global_data["cases"], global_data["deaths"], global_data["recovered"]],
            names=["Cases", "Deaths", "Recovered"],
            title="Global COVID-19 Cases Distribution",
            color_discrete_sequence=["blue", "red", "green"]
        )
        st.plotly_chart(fig1, use_container_width=True)

    else:
        st.warning("⚠️ Global COVID-19 data is unavailable.")

# 🔹 Page: Country-wise Data
elif page == "📌 Country-wise Data":
    st.title("📌 COVID-19 Country-wise Statistics")

    if country_data:
        df = pd.DataFrame(country_data)[["country", "cases", "deaths", "recovered"]]
        df = df.sort_values(by="cases", ascending=False)

        # Dropdown to Select Country
        country_list = df["country"].tolist()
        selected_country = st.sidebar.selectbox("Select a country", country_list)

        # Filter Selected Country Data
        country_stats = df[df["country"] == selected_country].iloc[0]

        # Display Selected Country Data
        st.subheader(f"📍 {selected_country}")
        st.metric("🦠 Cases", f"{country_stats['cases']:,}")
        st.metric("☠️ Deaths", f"{country_stats['deaths']:,}")
        st.metric("💪 Recovered", f"{country_stats['recovered']:,}")

        # Bar Chart of Top 10 Most Affected Countries
        st.subheader("🌎 Top 10 Most Affected Countries")
        top10 = df.head(10)
        fig2 = px.bar(
            top10, x="country", y="cases",
            title="Top 10 Countries by COVID-19 Cases",
            color="cases",
            labels={"cases": "Total Cases", "country": "Country"},
            color_continuous_scale="reds"
        )
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("⚠️ Country-wise COVID-19 data is unavailable.")

# 🔹 Page: Data Table
elif page == "📊 Data Table":
    st.title("📊 COVID-19 Data Table")

    if country_data:
        df = pd.DataFrame(country_data)[["country", "cases", "deaths", "recovered"]]
        df = df.sort_values(by="cases", ascending=False)

        # Display Data Table
        st.dataframe(df, height=600)

    else:
        st.warning("⚠️ Data is not available.")

# 🔹 Footer
st.sidebar.markdown("---")
st.sidebar.info("Developed by Tanvi Kakade | Data Source: disease.sh API")
