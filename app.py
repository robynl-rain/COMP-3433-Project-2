# Robyn Edwards
# COMP 3433 - Project 2
# 08/20/2025

from dash import Dash, dcc, html, Input, Output
import numpy as np
import pandas as pd
import plotly.express as px

# read in data from csv file
nchs_data = pd.read_csv(r"https://raw.githubusercontent.com/robynl-rain/COMP-3433-Project-2/refs/heads/main/data/NCHS_-_Leading_Causes_of_Death__United_States.csv")

# split data into sets for the states and the whole country
state_data = nchs_data[nchs_data["State"] != "United States"]
national_data = nchs_data[nchs_data["State"] == "United States"]

# create lists for values for states, causes, and years
states = sorted(state_data["State"].unique())
causes = sorted(nchs_data["Cause Name"].unique())
years = np.sort(nchs_data["Year"].unique())


# initialize dash application
app = Dash(__name__, suppress_callback_exceptions=True)

# create title for dash application
app.title = "Leading Causes of Death - United States"

# configure application layout
app.layout = html.Div(
    className="app-container",
    children=[
        # make header for page
        html.H1("Leading Causes of Death in the U.S.", style={"marginBottom": 0}),

        html.Hr(),
        
        # create different tabs for different displays of data
        dcc.Tabs(id="tabs", value="tab-overview", 
            children=[
                dcc.Tab(label="Overview", value="tab-overview"),
                dcc.Tab(label="National Data Overview", value="tab-national"),
                dcc.Tab(label="State Data", value="tab-state"),
                dcc.Tab(label="Compare States", value="tab-comparison"),
            ],
        ),

        # create container for the tabs
        html.Div(id="tab-content", style={"marginTop": 16}),
    ],
)


# callback for tabs and their respective content
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
)
def render_content(tab):
    # case for the tab displaying the app overview
    if tab == "tab-overview":
        return html.Div([
            # print a brief overview of the data itself
            html.H2("Overview of Dataset and Application"),
            html.P(
                "This is an interactive dashboard displaying data for the top 10 leading causes of death in the United States from 1999-2017"
                "The dataset used for all the representations shown in this dashboard was published by the Centers for Disease Control and Prevention (CDC) / "
                "National Center for Health Statistics (NCHS), based on collected data from the National Vital Statistics System (NVSS)"
            ),
            html.P(
                "Visualizations of this data are provided for both the state and national level."
                "Choose from the different tabs to view historical trends at the national level, view data trends by state, and compare data for specific states directly"
            ),

            # provide brief instruction on using the dashboard
            html.H3("How to Use This Dashboard"),
            html.Ul([
                html.Li("Use the tabs at the top to switch between statelevel, national, and comparison views."),
                html.Li("Dropdown menus and controls allow you to filter by state, cause of death, year, and metric."),
                html.Li("Hover over charts to see exact values and trends."),
            ]),
            
            # provide citations for the data used 
            html.H3("Citation"),
            html.P(
                "National Center for Health Statistics (NCHS). "
                "NCHS Leading Causes of Death, United States. "
                "Centers for Disease Control and Prevention, U.S. Department of Health and Human Services."
            ),
            html.P([
                "Data accessed via Data.gov: ",
                html.A("https://catalog.data.gov/dataset/nchs-leading-causes-of-death-united-states", href="https://catalog.data.gov/dataset/nchs-leading-causes-of-death-united-states", target="_blank")
            ], style={"maxWidth": "800px", "margin": "auto"}),
        ])
    
    # case for the tab displaying national data
    if tab == "tab-national":
        return html.Div([
            # create a dropdown menu for the user to select a cause of death to filter by
            html.Div([
                html.Label("Select Cause of Death:"),
                dcc.Dropdown(causes, value=causes[0], id="ntl-cause-dropdown"),
            ]),
            # include a line plot and bar plot for the national level data
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
                children=[
                    dcc.Graph(id="ntl-line-plot"),
                    dcc.Graph(id="ntl-bar-plot"),
                ],
            ),
        ])
    
    # case for the tab displaying state information
    elif tab == "tab-state":
        return html.Div([
            # controls for user interaction
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "12px", "marginTop": 12},
                children=[
                    # create a dropdown menu for the user to select a state
                    html.Div([
                        html.Label("Select State:"),
                        dcc.Dropdown(states, value=states[0], id="state-dropdown"),
                    ]),
                    # create a dropdown menu for the user to select a cause of death to filter by
                    html.Div([
                        html.Label("Select Cause of Death:"),
                        dcc.Dropdown(causes, value=causes[0], id="cause-dropdown"),
                    ]),
                    # create a dropdown menu for the user to select a year
                    html.Div([
                        html.Label("Select Year:"),
                        dcc.Dropdown(years, value=years[0], id="year-dropdown"),
                    ]),
                    # create a radio for the user to select the metric of data to view
                    html.Div([
                        html.Label("Choose Metric:"),
                        dcc.RadioItems(["Deaths", "Age-adjusted Death Rate"], value="Deaths", id="metric-radio")
                    ]),
                ],
            ),
            # include line plot, bar plot, and a map for the individual states data
            html.Div([
                dcc.Graph(id="state-line-plot"),
                dcc.Graph(id="state-bar-plot"),
                dcc.Graph(id="state-map-plot"),
            ], style={"width": "68%", "display": "inline-block", "paddingLeft": "2%"}),
        ])
    
    # case for the tab showing comparison of data between states
    elif tab == "tab-comparison":
        return html.Div([
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "12px"},
                children=[
                    # create a dropdown menu for the user to select the first state for comparison
                    html.Div([
                        html.Label("Select First State:"),
                        dcc.Dropdown(states, value=states[0], id="comp-state1-dropdown"),
                    ]),
                    # create a dropdown menu for the user to select the second state for comparison
                    html.Div([
                        html.Label("Select Second State:"),
                        dcc.Dropdown(states, value=states[1], id="comp-state2-dropdown"),
                    ]),
                    # create a dropdown menu for the user to select a cause of death to filter by
                    html.Div([
                        html.Label("Select Cause of Death:"),
                        dcc.Dropdown(causes, value=causes[0], id="comp-cause-dropdown"),
                    ]),
                ],
            ),
            # use a line plot to compare the historical trends of the selected states
            dcc.Graph(id="compare-line"),
        ])


# callback for the tab of national data and its associated figures/plots
@app.callback(
    Output("ntl-line-plot", "figure"),
    Output("ntl-bar-plot", "figure"),
    Input("ntl-cause-dropdown", "value"),
)
def update_national_tab(selected_cause):
    # line plot to chart trends in deaths from the selected cause over time

    # define data frame to filter data with the selected cause
    line_df = national_data[national_data["Cause Name"] == selected_cause]
    # create figure for the data
    line_fig = px.line(line_df, x="Year", y="Age-adjusted Death Rate", title=f"Rate of Death from {selected_cause} in the United States from 1999-2017")
    line_fig.update_layout(yaxis_title="Age-Adjusted Death Rate (per 100,000 people)")
    
    #bar chart to display the top causes of death for the selected year

    # create dataframe to filter out top causes in the most recent year
    bar_df = national_data[(national_data["Year"] == national_data["Year"].max()) & (national_data["Cause Name"] != "All causes")]
    bar_df = bar_df.sort_values(by="Deaths", ascending=False).head(10)
    # create figure for the data
    bar_fig = px.bar(bar_df, x="Cause Name", y="Deaths", title=f"Top Causes of Death in the United States during {bar_df['Year'].max()}")
    bar_fig.update_layout(yaxis_title="Total Number of Deaths")
    bar_fig.update_layout(yaxis_title="Cause of Death")

    # return the final figures
    return line_fig, bar_fig


# callback for the tab of state data and its associated figures/plots
@app.callback(
    Output("state-line-plot", "figure"),
    Output("state-bar-plot", "figure"),
    Output("state-map-plot", "figure"),
    Input("state-dropdown", "value"),
    Input("cause-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("metric-radio", "value"),
)
def update_state_tab(selected_state, selected_cause, selected_year, selected_metric):
    # line plot of historical trends for the selected state and cause
   
    # define data frame to include the selected cause, year, state, and metric
    line_df = state_data[(state_data["State"] == selected_state) & (state_data["Cause Name"] == selected_cause)]
    # create figure to show a line plot of the cause of death over time
    line_fig = px.line(line_df, x="Year", y=selected_metric, )
    if selected_metric=="Deaths":
        line_fig.update_layout(yaxis_title="Total Number of Deaths",
        title=f"Total Deaths from {selected_cause} in {selected_state} from 1999-2017")
    if selected_metric=="Age-adjusted Death Rate":
        line_fig.update_layout(yaxis_title="Age-Adjusted Death Rate (per 100,000 people)",
        title=f"Rate of Death from {selected_cause} in {selected_state} from 1999-2017")
    # bar graph of the leading causes of death for the selected state and year

    # define data frame to include the selected state and year
    bar_df = state_data[(state_data["State"] == selected_state) & (state_data["Year"] == selected_year) & (state_data["Cause Name"] != "All causes")]
    bar_df = bar_df.sort_values(by=selected_metric, ascending=False).head(10)
    # create figure to display bar graph
    bar_fig = px.bar(bar_df, x="Cause Name", y=selected_metric, title=f"Top Causes of Death in {selected_state}, {selected_year}")
    if selected_metric=="Deaths":
        bar_fig.update_layout(yaxis_title="Total Number of Deaths")
    if selected_metric=="Age-adjusted Death Rate":
        bar_fig.update_layout(yaxis_title="Age-Adjusted Death Rate (per 100,000 people)")


    # state abbreviations
    state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
    }

    # map showing differences between states for a selected year and cause

    # define data frame to include data with the selected cause and year
    map_df = state_data[(state_data["Cause Name"] == selected_cause) & (state_data["Year"] == selected_year)]
    map_df["State_abbrev"] = map_df["State"].map(state_abbrev)
    # create figure to display map 
    map_fig = px.choropleth(map_df, locations="State_abbrev", locationmode="USA-states", color=selected_metric, scope="usa", color_continuous_scale='Viridis')
    if selected_metric=="Deaths":
        map_fig.update_layout(yaxis_title="Total Number of Deaths",
        title=f"Total Deaths from {selected_cause} across the U.S. in {selected_year}")
    if selected_metric=="Age-adjusted Death Rate":
        map_fig.update_layout(yaxis_title="Age-Adjusted Death Rate (per 100,000 people)",
        title=f"Rate of Death from {selected_cause} across the U.S. in {selected_year}")
    # return the figures produced
    return line_fig, bar_fig, map_fig


# callback for the tab of state comparison data and its associated figures/plots
@app.callback(
    Output("compare-line", "figure"),
    Input("comp-state1-dropdown", "value"),
    Input("comp-state2-dropdown", "value"),
    Input("comp-cause-dropdown", "value"),
)
def update_comparison_tab(state1, state2, selected_cause):
    # line plot to show comparison of historical trends between two selected states

    # define data frame to filter data to the selected states and cause
    df = state_data[(state_data["State"].isin([state1, state2])) & (state_data["Cause Name"] == selected_cause)]
    # create figure to display data
    fig = px.line(df, x="Year", y="Age-adjusted Death Rate", color="State", title=f"Rate of Death from {selected_cause} in {state1} and {state2} from 1999-2017")
    fig.update_layout(yaxis_title="Age-Adjusted Death Rate (per 100,000 people)")
    return fig

# run the app
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)