# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("final_dataset.csv")

st.title("SDG Analysis: Urbanization vs Air Pollution (PM2.5)")
st.markdown("""
This dashboard explores the relationship between **urban population** and **air pollution (PM2.5)** across countries.
Filters are placed near their respective charts for better interaction.
""")

# -----------------------------
# 2. Map — PM2.5 by Country
# -----------------------------
st.subheader("Global PM2.5 Map")
st.markdown("""
**Filter Description:** Select a year to filter the map.  

**Chart Description:**  
This choropleth map shows the **average PM2.5 levels by country** for the selected year.  
- **Red** indicates higher air pollution.  
- **Green** indicates lower pollution.  
Useful for identifying **geographical hotspots of air pollution** worldwide.
""")

selected_year_map = st.slider(
    "Select Year for Map",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=int(df['Year'].min())
)

map_df = df[df['Year'] == selected_year_map]

fig_map = px.choropleth(
    map_df,
    locations="Country Name",
    locationmode="country names",
    color="PM25",
    hover_name="Country Name",
    hover_data={"Urban_Population": True, "PM25": True, "Country Name": False},
    color_continuous_scale=px.colors.diverging.RdYlGn[::-1]
)
fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# Dynamic insight for map
highest_country = map_df.loc[map_df['PM25'].idxmax()]["Country Name"]
highest_value = map_df['PM25'].max()
lowest_country = map_df.loc[map_df['PM25'].idxmin()]["Country Name"]
lowest_value = map_df['PM25'].min()

st.markdown(f"""
**Insight:**  
- Country with highest PM2.5 in {selected_year_map}: **{highest_country} ({highest_value:.2f})**  
- Country with lowest PM2.5: **{lowest_country} ({lowest_value:.2f})**  
- Map shows **global disparities** in air quality.
""")

# -----------------------------
# 3. Scatter Plot — Urban Pop vs PM2.5
# -----------------------------
st.subheader("Urban Population vs PM2.5")
st.markdown("""
**Filter Description:** Select countries to include in this scatter plot.  

**Chart Description:**  
This scatter plot shows the relationship between **urban population** (X-axis, log scale) and **PM2.5 levels** (Y-axis) for the selected countries.  
- Each point represents a country.  
- A **trend line** highlights the overall correlation.  
Useful for identifying whether higher urbanization is associated with higher air pollution.
""")

scatter_countries = st.multiselect(
    "Select Countries for Scatter Plot",
    options=df['Country Name'].unique(),
    default=list(df['Country Name'].unique()[:15])
)

scatter_df = df[(df['Year'] == selected_year_map) & (df['Country Name'].isin(scatter_countries))]

scatter_fig = px.scatter(
    scatter_df,
    x="Urban_Population",
    y="PM25",
    hover_name="Country Name",
    size="PM25",
    color="PM25",
    color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
    log_x=True
)

# Add trend line
if len(scatter_df) > 1:
    x = np.log(scatter_df["Urban_Population"])
    y = scatter_df["PM25"]
    coeffs = np.polyfit(x, y, 1)
    trend_y = coeffs[0]*x + coeffs[1]
    scatter_fig.add_traces(go.Scatter(
        x=scatter_df["Urban_Population"],
        y=trend_y,
        mode="lines",
        name="Trend Line",
        line=dict(color="black", dash="dash")
    ))

st.plotly_chart(scatter_fig, use_container_width=True)

# Dynamic insight for scatter
if len(scatter_df) > 1:
    correlation = scatter_df["Urban_Population"].corr(scatter_df["PM25"])
    max_polluted = scatter_df.loc[scatter_df['PM25'].idxmax()]["Country Name"]
    max_value = scatter_df['PM25'].max()
    st.markdown(f"""
**Insight:**  
- Correlation between urban population and PM2.5: **{correlation:.2f}**  
- Highest PM2.5 among selected countries: **{max_polluted} ({max_value:.2f})**  
- Trend line shows overall relationship; some countries deviate due to **effective pollution control**.
""")

# -----------------------------
# 4. Top N Most Polluted Countries — Bar Chart
# -----------------------------
st.subheader("Top N Most Polluted Countries")
st.markdown("""
**Filter Description:** Adjust Top N to see the most polluted countries.  

**Chart Description:**  
This bar chart shows the **Top N countries with the highest PM2.5 levels** for the selected year.  
- **Color gradient** (Red → Green) highlights pollution intensity.  
- Bars allow **quick comparison between countries**.
""")

top_n = st.slider(
    "Top N Polluted Countries",
    min_value=5,
    max_value=20,
    value=10
)

bar_df = df[df['Year'] == selected_year_map]
top_countries = bar_df.groupby("Country Name")["PM25"].mean().sort_values(ascending=False).head(top_n).reset_index()

bar_fig = px.bar(
    top_countries,
    x="Country Name",
    y="PM25",
    color="PM25",
    color_continuous_scale=px.colors.diverging.RdYlGn[::-1]
)
bar_fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(bar_fig, use_container_width=True)

# Dynamic insight for bar chart
top_country_name = top_countries.iloc[0]["Country Name"]
top_pm25 = top_countries.iloc[0]["PM25"]
st.markdown(f"""
**Insight:**  
- Most polluted country: **{top_country_name} ({top_pm25:.2f})**  
- Bars and colors highlight the **priority countries for air quality interventions**.
""")

# -----------------------------
# 5. Line Chart — PM2.5 Trends Over Time
# -----------------------------
st.subheader("PM2.5 Trends Over Time (Top Countries)")
st.markdown("""
**Filter Description:** Select countries to include in this line chart.  

**Chart Description:**  
This line chart shows the **PM2.5 trend over time** for the selected countries.  
- Helps monitor whether pollution is **increasing or decreasing** over the years.  
- Useful for assessing the **impact of policies or urbanization trends**.
""")

line_countries = st.multiselect(
    "Select Countries for Line Chart",
    options=df['Country Name'].unique(),
    default=list(top_countries["Country Name"])
)

line_df = df[df["Country Name"].isin(line_countries)]
line_fig = px.line(
    line_df,
    x="Year",
    y="PM25",
    color="Country Name",
    markers=True
)
st.plotly_chart(line_fig, use_container_width=True)

# Dynamic insight for line chart
trends = []
for country in line_countries:
    country_df = line_df[line_df["Country Name"] == country]
    if len(country_df) > 1:
        trend = country_df["PM25"].iloc[-1] - country_df["PM25"].iloc[0]
        trends.append((country, trend))

trends_sorted = sorted(trends, key=lambda x: x[1], reverse=True)
if trends_sorted:
    rising_country, rising_value = trends_sorted[0]
    falling_country, falling_value = trends_sorted[-1]
    st.markdown(f"""
**Insight:**  
- Country with **largest increase** in PM2.5: **{rising_country} ({rising_value:.2f})**  
- Country with **largest decrease** in PM2.5: **{falling_country} ({falling_value:.2f})**  
- Line chart highlights **trends over time** for the selected countries.
""")