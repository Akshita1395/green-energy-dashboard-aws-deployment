import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Page Config
st.set_page_config(page_title="Green Future Analytics", page_icon="🌍", layout="wide")

# Colors (GLOBAL)

bg_color = "#1e293b"
text_color = "#e2e8f0"
grid_color = "#334155"

metric_labels = {
    "greenhouse_gas_emissions": "Greenhouse Gas Emissions",
    "renewables_share_energy": "Renewables Share of Energy"
}

model_descriptions = {
    "Linear Regression": "Fits a straight-line relationship between scaled renewable share, year, and CO₂.",
    "Ridge Regression": "A regularized linear model that reduces overfitting.",
    "Random Forest": "A tree ensemble model that captures non-linear patterns."
}


# Styling

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #0f172a, #1e293b);
}}
section[data-testid="stSidebar"] {{
    background: #020617;
}}
h1, h2, h3 {{
    color: {text_color};
}}
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_energy.csv")
    exclude = ['World','Asia','Europe','Africa','North America','South America','Oceania','European Union']
    return df[~df['country'].isin(exclude)]

df = load_data()

# Sidebar

st.sidebar.title("🔎 Controls")
st.sidebar.markdown("Filters apply to all charts, metrics, insights, predictions, and downloads.")

countries = sorted(df['country'].unique())
selected_countries = st.sidebar.multiselect("Select Country(ies)", countries, default=[countries[0]])

global_view = st.sidebar.checkbox("Global View")

if global_view:
    st.sidebar.info("Global View aggregates values across the selected year range.")
else:
    st.sidebar.info("Select one or more countries to compare their results across the dashboard.")

year_range = st.sidebar.slider("Year Range",
    int(df['year'].min()), int(df['year'].max()), (2000, 2020))

metric = st.sidebar.selectbox("Metric",
    ["greenhouse_gas_emissions", "renewables_share_energy"])
metric_title = metric_labels.get(metric, metric)

prediction_model = st.sidebar.selectbox("Prediction Model",
    ["Linear Regression", "Ridge Regression", "Random Forest"])

st.sidebar.info(model_descriptions[prediction_model])
st.sidebar.caption("Model choice affects only the prediction section and uses current filtered data.")


# Apply Filters

df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

if global_view:
    filtered_df = df.groupby('year').mean(numeric_only=True).reset_index()
    entity_label = "Global Average"
else:
    if not selected_countries:
        selected_countries = [countries[0]]
    filtered_df = df[df['country'].isin(selected_countries)].sort_values(["country", "year"])
    entity_label = ", ".join(selected_countries)

# Comparison Logic

if global_view:
    combined_df = filtered_df.copy()
    combined_df["country_label"] = entity_label
else:
    combined_df = filtered_df.copy()
    combined_df["country_label"] = combined_df["country"]

# Helper for consistent charts

def style_fig(fig):
    fig.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color),
        xaxis=dict(gridcolor=grid_color),
        yaxis=dict(gridcolor=grid_color),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

# Title

st.markdown("<h1 style='text-align:center;'>🌍 Green Future Analytics Dashboard</h1>", unsafe_allow_html=True)

st.markdown(f"""
**Filters:**  
- Mode: {'Global View' if global_view else 'Country Comparison'}  
- Countries: {entity_label}  
- Years: {year_range[0]}–{year_range[1]}  
- Metric: {metric_labels.get(metric, metric)}  
- Prediction Model: {prediction_model}
""")

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

trend_df = filtered_df.copy()
if not global_view:
    trend_df = trend_df.groupby('year').mean(numeric_only=True).reset_index()

co2_change = trend_df['greenhouse_gas_emissions'].iloc[-1] - trend_df['greenhouse_gas_emissions'].iloc[0] if len(trend_df) > 1 else 0
trend_status = "Down" if co2_change < 0 else "Up" if len(trend_df) > 1 else "N/A"
trend_delta = f"{abs(co2_change):.2f}" if len(trend_df) > 1 else ""

# KPIs

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Renewable", round(filtered_df['renewables_share_energy'].mean(),2))
c2.metric("Avg CO₂", round(filtered_df['greenhouse_gas_emissions'].mean(),2))
c3.metric("Years", f"{filtered_df['year'].min()}-{filtered_df['year'].max()}")
c4.metric("CO₂ Trend", trend_status, delta=trend_delta)

st.divider()

st.subheader("📌 Summary")

st.info(f"""
Entity: {entity_label}  
Years: {filtered_df['year'].min()} - {filtered_df['year'].max()}  
Avg CO₂: {filtered_df['greenhouse_gas_emissions'].mean():.2f}  
Avg Renewable: {filtered_df['renewables_share_energy'].mean():.2f}%
""")

# Trend

st.subheader("📊 Trend Analysis")

fig = px.line(
    combined_df,
    x='year',
    y=metric,
    color='country_label',
    template="plotly",
    title=f"{metric_title} Trend"
)
fig.update_layout(legend_title_text='Country')
st.plotly_chart(style_fig(fig), use_container_width=True)

# Scatter

st.subheader("🔗 Relationship Analysis")

scatter = px.scatter(
    combined_df,
    x="renewables_share_energy",
    y="greenhouse_gas_emissions",
    color="country_label",
    hover_data=["year"],
    template="plotly",
    title="CO₂ vs Renewable Share"
)
scatter.update_layout(legend_title_text='Country')
st.plotly_chart(style_fig(scatter), use_container_width=True)

# Energy Distribution

st.subheader("⚡ Energy Distribution")

if global_view or len(selected_countries) == 1:
    st.caption("Average share of electricity generation by source for the selected data.")
    energy_df = pd.DataFrame({
        'Source': ['Solar','Wind','Hydro'],
        'Value': [
            filtered_df['solar_electricity'].mean(),
            filtered_df['wind_electricity'].mean(),
            filtered_df['hydro_electricity'].mean()
        ]
    })
    pie = px.pie(energy_df, names='Source', values='Value', template="plotly")
    st.plotly_chart(style_fig(pie), use_container_width=True)
else:
    st.caption("Average electricity generation by source for each selected country.")
    country_energy = filtered_df.groupby('country')[['solar_electricity','wind_electricity','hydro_electricity']].mean().reset_index()
    energy_melt = country_energy.melt(id_vars='country', value_vars=['solar_electricity','wind_electricity','hydro_electricity'],
                                      var_name='Source', value_name='Value')
    bar_energy = px.bar(energy_melt, x='country', y='Value', color='Source', barmode='group', template="plotly")
    st.plotly_chart(style_fig(bar_energy), use_container_width=True)

# Top Emitters

st.subheader("🌍 Top Emitters")

top_emitters = df.groupby("country")["greenhouse_gas_emissions"].mean().sort_values(ascending=False).head(10)
bar = px.bar(x=top_emitters.values, y=top_emitters.index, orientation='h', template="plotly")
st.plotly_chart(style_fig(bar), use_container_width=True)

# Top Renewable

st.subheader("🌱 Top Renewable Countries")

top_renew = df.groupby("country")["renewables_share_energy"].mean().sort_values(ascending=False).head(10)
renew = px.bar(x=top_renew.values, y=top_renew.index, orientation='h', template="plotly")
st.plotly_chart(style_fig(renew), use_container_width=True)


# Histogram

st.subheader("📊 Emissions Distribution")

hist = px.histogram(filtered_df, x="greenhouse_gas_emissions", template="plotly")
st.plotly_chart(style_fig(hist), use_container_width=True)


# Box Plot

st.subheader("📦 Emissions Spread")

box = px.box(filtered_df, y="greenhouse_gas_emissions", template="plotly")
st.plotly_chart(style_fig(box), use_container_width=True)

# Heatmap

st.subheader("🔥 Correlation Heatmap")

corr = filtered_df[['greenhouse_gas_emissions','renewables_share_energy',
                    'solar_electricity','wind_electricity','hydro_electricity']].corr()

heat = px.imshow(corr, text_auto=True, template="plotly")
st.plotly_chart(style_fig(heat), use_container_width=True)


# Growth
st.subheader("📈 Growth Rate")

growth_df = filtered_df.copy()
if global_view:
    growth_df['growth'] = growth_df['greenhouse_gas_emissions'].pct_change() * 100
else:
    growth_df['growth'] = growth_df.groupby('country')['greenhouse_gas_emissions'].pct_change() * 100

growth_df = growth_df.dropna(subset=['growth'])
if growth_df.empty:
    st.warning("Not enough data to calculate growth for the selected filters.")
else:
    growth = px.line(growth_df, x='year', y='growth', color='country' if not global_view else None,
                     template="plotly", title="Year-over-Year CO₂ Growth")
    st.plotly_chart(style_fig(growth), use_container_width=True)

# Prediction

st.subheader("🔮 Prediction")

ml_df = filtered_df[['renewables_share_energy','year','greenhouse_gas_emissions']].dropna()

if len(ml_df) > 5:
    features = ml_df[['renewables_share_energy','year']]
    target = ml_df['greenhouse_gas_emissions']

    if prediction_model == "Linear Regression":
        model = Pipeline([('scaler', StandardScaler()), ('reg', LinearRegression())])
    elif prediction_model == "Ridge Regression":
        model = Pipeline([('scaler', StandardScaler()), ('reg', Ridge(alpha=1.0))])
    else:
        model = Pipeline([('scaler', StandardScaler()), ('reg', RandomForestRegressor(n_estimators=100, random_state=42))])

    model.fit(features, target)

    score = model.score(features, target)

    renew = st.slider("Renewable %", 0.0, 100.0, float(ml_df.iloc[-1]['renewables_share_energy']))
    year = st.number_input("Year", 2000, 2050, int(ml_df.iloc[-1]['year']))

    input_df = pd.DataFrame(
        [[renew, year]], columns=['renewables_share_energy', 'year']
    )
    pred = model.predict(input_df)[0]
    st.write(f"Training data points: {len(ml_df)} | Model R² score: {score:.2f}")
    st.success(f"Predicted CO₂: {pred:.2f}")
else:
    st.warning("Not enough data to generate a prediction. Try a wider year range or another country selection.")


# Insights

st.subheader("🧠 Insights")

if filtered_df["renewables_share_energy"].mean()>30:
    st.success("High renewable adoption")
else:
    st.warning("Low renewable adoption")

if trend_df["greenhouse_gas_emissions"].iloc[-1] > trend_df["greenhouse_gas_emissions"].iloc[0]:
    st.error("Emissions increasing")
else:
    st.success("Emissions decreasing")

st.divider()
st.subheader("✅ Conclusion")
conclusions = []
if filtered_df["renewables_share_energy"].mean() > 30:
    conclusions.append("Renewables are a strong part of the selected dataset.")
else:
    conclusions.append("Renewable adoption remains modest and could improve.")
if trend_status == "Down":
    conclusions.append("CO₂ emissions are trending downward in the selected period.")
elif trend_status == "Up":
    conclusions.append("CO₂ emissions are trending upward in the selected period.")
else:
    conclusions.append("Not enough trend data is available for a clear CO₂ direction.")
st.info(" ".join(conclusions))


# Data Access Section
st.divider()
st.subheader("📄 Data Access")

st.write("View and download the processed dataset used in this dashboard.")

# Toggle to show data
show_data = st.checkbox("Show Data")

if show_data:
    st.dataframe(filtered_df, use_container_width=True)

# Download button
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name=f"{'_'.join(selected_countries)}_data.csv" if not global_view else "global_data.csv",
    mime='text/csv'
)