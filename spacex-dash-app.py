"""
SpaceX Launch Records Dashboard
================================

Interactive Plotly Dash dashboard for the IBM Data Science Professional
Certificate, Applied Data Science Capstone (SpaceX Falcon 9 landing prediction).

Features
--------
- Launch-site dropdown ("All Sites" or one site).
- Pie chart: share of successful launches per site (All Sites),
  or success vs. failure counts for the selected site.
- Payload range slider.
- Scatter plot: payload mass vs. launch outcome, coloured by booster version.

Run
---
    pip install pandas dash plotly
    python spacex-dash-app.py

Then open http://127.0.0.1:8050 in a browser.

The script reads `spacex_launch_dash.csv` from the same folder. If the file is
missing, it downloads it from the IBM Skills Network course storage.
"""

import os

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
DATA_FILE = "spacex_launch_dash.csv"
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)

if os.path.exists(DATA_FILE):
    spacex_df = pd.read_csv(DATA_FILE)
else:
    spacex_df = pd.read_csv(DATA_URL)

# Readable outcome labels for the charts (the 'class' column is 1 = landed, 0 = failed)
spacex_df["Outcome"] = spacex_df["class"].map({1: "Success", 0: "Failure"})

min_payload = spacex_df["Payload Mass (kg)"].min()
max_payload = spacex_df["Payload Mass (kg)"].max()

# Dropdown options built from the data, so they always match the 'Launch Site' column
site_options = [{"label": "All Sites", "value": "ALL"}] + [
    {"label": site, "value": site} for site in sorted(spacex_df["Launch Site"].unique())
]

OUTCOME_COLORS = {"Success": "#2F6FB0", "Failure": "#E8662B"}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
app = Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1200px", "margin": "0 auto", "padding": "20px"},
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 40},
        ),

        # TASK 1: launch-site dropdown (default: all sites)
        dcc.Dropdown(
            id="site-dropdown",
            options=site_options,
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),

        # TASK 2: success pie chart
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),

        # TASK 3: payload range slider
        html.P("Payload range (kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={i: str(i) for i in range(0, 10001, 2500)},
            value=[min_payload, max_payload],
        ),

        # TASK 4: payload vs. outcome scatter plot
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ],
)

# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    """All sites: each site's share of successful launches.
    One site: success vs. failure counts at that site."""
    if entered_site == "ALL":
        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Successful Launches by Site",
        )
    else:
        site_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        counts = site_df["Outcome"].value_counts().reset_index()
        counts.columns = ["Outcome", "count"]
        fig = px.pie(
            counts,
            values="count",
            names="Outcome",
            color="Outcome",
            color_discrete_map=OUTCOME_COLORS,
            title=f"Success vs. Failed Launches for site {entered_site}",
        )
    return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_scatter_chart(entered_site, payload_range):
    """Payload mass vs. landing outcome within the selected payload range,
    coloured by booster version category."""
    low, high = payload_range
    in_range = spacex_df["Payload Mass (kg)"].between(low, high)
    filtered_df = spacex_df[in_range]

    if entered_site == "ALL":
        title = "Correlation between Payload and Success for all Sites"
    else:
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        title = f"Correlation between Payload and Success for site {entered_site}"

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=["Launch Site", "Outcome"],
        title=title,
    )
    fig.update_yaxes(tickvals=[0, 1], ticktext=["Failure (0)", "Success (1)"])
    return fig


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=False)
