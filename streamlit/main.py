import streamlit as st
import plotly.graph_objects as go
from datasets.cases import national_cases


st.set_page_config(page_title="Summary", layout="wide")
st.title("Coronavirus Dashboard - Italy 2020-2025")

df = national_cases()
df["date"] = df["date"].dt.date

current = st.slider(
    label="Date",
    value=df["date"].max(),
    min_value=df["date"].min(),
    max_value=df["date"].max(),
)
current_df = df.loc[df["date"] == current]
df = df.loc[df['date'] <= current]

a1, a2, a3, a4 = st.columns(4)
with a1:
    st.metric(
        "Active Cases",
        current_df['active_cases'],
        delta=(current_df['active_cases'] - current_df['active_cases_7d_ago']).item(),
        delta_description="vs 7 days prior",
        delta_color="inverse",
        chart_type="area",
        chart_data=df['active_cases'],
        format="compact",
        border=True,
    )

with a2:
    st.metric(
        "New Cases",
        current_df['new_cases'],
        delta=(current_df['new_cases'] - current_df['new_cases_7d_ago']).item(),
        delta_description="vs 7 days prior",
        delta_color="inverse",
        chart_type="area",
        chart_data=df['new_cases_7d_avg'],
        format="compact",
        border=True,
    )

with a3:
    st.metric(
        "New Deaths",
        current_df['new_deaths'],
        delta=(current_df['new_deaths'] - current_df['new_deaths_7d_ago']).item(),
        delta_description="vs 7 days prior",
        delta_color="inverse",
        chart_type="area",
        chart_data=df['new_deaths_7d_avg'],
        format="compact",
        border=True,
    )

with a4:
    st.metric(
        "New Recoveries",
        current_df['new_recovered'],
        delta=(current_df['new_recovered'] - current_df['new_recovered_7d_ago']).item(),
        delta_description="vs 7 days prior",
        delta_color="normal",
        chart_type="area",
        chart_data=df['new_recovered_7d_avg'],
        format="compact",
        border=True,
    )


def snake_case(string):
    return string.replace(" ", "_").lower()

metric = st.pills("Metric", ["Active Cases", "New Cases", "New Deaths", "New Recovered"], default="Active Cases")
st.area_chart(df, x="date", y=snake_case(metric))

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['new_cases_7d_avg'],
    name='New Cases',
    mode='lines',
    stackgroup='in',
    fillcolor='red',
    line=dict(color='red', width=0.5)
))

fig.add_trace(go.Scatter(
    x=df['date'],
    y=-df['new_deaths_7d_avg'],
    name='Deaths',
    mode='lines',
    stackgroup='out',
    fillcolor='black',
    line=dict(color='black', width=0.5)
))

fig.add_trace(go.Scatter(
    x=df['date'],
    y=-df['new_recovered_7d_avg'],
    name='Recoveries',
    mode='lines',
    stackgroup='out',
    fillcolor='green',
    line=dict(color='green', width=0.5)
))

fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['change_in_active_cases'],
    name='Active Cases',
    mode='lines',
    line=dict(color='blue', width=1)
))

fig.update_layout(
    hovermode='x unified',
    title='Stacked Areas with Sum Line',
    yaxis_title='Cases',
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.15,
        xanchor='center',
        x=0.5
    )
)

st.plotly_chart(fig, width='stretch')
