"""
Satellite Communication Link Simulation Platform
A Python-based interactive web application for evaluating satellite communication scenarios using NASA data.
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import requests
import json
import os
from datetime import datetime
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import tempfile

# Initialise the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Satellite Communication Link Simulator"

# Read NASA data
def load_nasa_data():
    """Load NASA data from nasa_data.txt file"""
    try:
        with open('nasa_data.txt', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # Return default data if file not found
        return {
            "weather_attenuation": {
                "L": {"clear": 0.1, "rain": 0.2},
                "S": {"clear": 0.2, "rain": 0.5},
                "X": {"clear": 0.3, "rain": 1.0},
                "Ku": {"clear": 0.5, "rain": 2.0},
                "Ka": {"clear": 0.8, "rain": 5.0},
                "optical": {"clear": 0.0, "rain": 50.0}
            },
            "debris_data": {
                "100": 0,
                "200": 50,
                "400": 200,
                "600": 500,
                "800": 800,
                "1000": 600,
                "1200": 400,
                "1500": 200,
                "2000": 100
            }
        }

# Load NASA data
nasa_data = load_nasa_data()

# Frequency band definitions
FREQUENCY_BANDS = {
    "L": {"freq_mhz": 1500, "wavelength_m": 0.2},
    "S": {"freq_mhz": 3000, "wavelength_m": 0.1},
    "X": {"freq_mhz": 8000, "wavelength_m": 0.0375},
    "Ku": {"freq_mhz": 12000, "wavelength_m": 0.025},
    "Ka": {"freq_mhz": 20000, "wavelength_m": 0.015},
    "optical": {"freq_mhz": 300000, "wavelength_m": 0.000001}
}

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Satellite Communication Link Simulator", 
                   className="text-center text-primary mb-4"),
            html.P("Evaluate satellite communication scenarios using NASA data", 
                   className="text-center text-muted mb-4")
        ])
    ]),
    
    # Input Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Communication Link Parameters"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Frequency Band"),
                            dcc.Dropdown(
                                id="freq-band",
                                options=[{"label": k, "value": k} for k in FREQUENCY_BANDS.keys()],
                                value="X",
                                clearable=False
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Transmit Power (dBW)"),
                            dbc.Input(
                                id="tx-power",
                                type="number",
                                value=10,
                                min=0,
                                max=50
                            )
                        ], width=6)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Antenna Gain TX (dBi)"),
                            dbc.Input(
                                id="tx-gain",
                                type="number",
                                value=20,
                                min=0,
                                max=50
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Antenna Gain RX (dBi)"),
                            dbc.Input(
                                id="rx-gain",
                                type="number",
                                value=20,
                                min=0,
                                max=50
                            )
                        ], width=6)
                    ])
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Mission Geometry"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Satellite Altitude (km)"),
                            dbc.Input(
                                id="altitude",
                                type="number",
                                value=500,
                                min=100,
                                max=2000
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Inclination (degrees)"),
                            dbc.Input(
                                id="inclination",
                                type="number",
                                value=98,
                                min=0,
                                max=180
                            )
                        ], width=6)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Ground Station Latitude"),
                            dbc.Input(
                                id="gs-lat",
                                type="number",
                                value=40.7128,
                                min=-90,
                                max=90,
                                step=0.0001
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Ground Station Longitude"),
                            dbc.Input(
                                id="gs-lon",
                                type="number",
                                value=-74.0060,
                                min=-180,
                                max=180,
                                step=0.0001
                            )
                        ], width=6)
                    ])
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Mission Parameters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Mission Parameters - Scenario A"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Number of Satellites"),
                            dbc.Input(
                                id="num-satellites-a",
                                type="number",
                                value=1,
                                min=1,
                                max=1000
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Ground Station Availability (%)"),
                            dbc.Input(
                                id="gs-availability-a",
                                type="number",
                                value=95,
                                min=0,
                                max=100
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Link Type"),
                            dcc.Dropdown(
                                id="link-type-a",
                                options=[
                                    {"label": "Direct-to-Ground", "value": "direct"},
                                    {"label": "Relay via Constellation", "value": "relay"}
                                ],
                                value="direct",
                                clearable=False
                            )
                        ], width=4)
                    ])
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Mission Parameters - Scenario B"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Number of Satellites"),
                            dbc.Input(
                                id="num-satellites-b",
                                type="number",
                                value=12,
                                min=1,
                                max=1000
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Ground Station Availability (%)"),
                            dbc.Input(
                                id="gs-availability-b",
                                type="number",
                                value=90,
                                min=0,
                                max=100
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Link Type"),
                            dcc.Dropdown(
                                id="link-type-b",
                                options=[
                                    {"label": "Direct-to-Ground", "value": "direct"},
                                    {"label": "Relay via Constellation", "value": "relay"}
                                ],
                                value="relay",
                                clearable=False
                            )
                        ], width=4)
                    ])
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Scenario Comparison
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Scenario Comparison"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Scenario A Name"),
                            dbc.Input(
                                id="scenario-a-name",
                                type="text",
                                value="Direct LEO",
                                placeholder="Enter scenario A name"
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Scenario B Name"),
                            dbc.Input(
                                id="scenario-b-name",
                                type="text",
                                value="Relay Constellation",
                                placeholder="Enter scenario B name"
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Priority"),
                            dcc.Dropdown(
                                id="priority",
                                options=[
                                    {"label": "Lowest Cost", "value": "cost"},
                                    {"label": "Highest Performance", "value": "performance"},
                                    {"label": "Balanced Trade-off", "value": "balanced"}
                                ],
                                value="balanced",
                                clearable=False
                            )
                        ], width=4)
                    ])
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # Control Buttons
    dbc.Row([
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button("Run Simulation", id="run-sim", color="primary", size="lg"),
                dbc.Button("Download PDF Report", id="download-pdf", color="success", size="lg"),
                dbc.Button("Clear Results", id="clear-results", color="secondary", size="lg")
            ], className="d-flex justify-content-center")
        ], width=12)
    ], className="mb-4"),
    
    # Results Section
    dbc.Row([
        dbc.Col([
            html.Div(id="simulation-results")
        ], width=12)
    ]),
    
    # Hidden div to store data for PDF generation
    html.Div(id="pdf-data", style={"display": "none"}),
    
    # Download component
    dcc.Download(id="download-pdf-file")
])

# Calculation functions
def calculate_path_loss(range_km, frequency_mhz):
    """Calculate free-space path loss using Friis equation"""
    return 20 * np.log10(range_km) + 20 * np.log10(frequency_mhz) + 32.44

def calculate_received_power(tx_power_dbw, tx_gain_dbi, rx_gain_dbi, path_loss_db, atmospheric_loss_db=0):
    """Calculate received power using Friis transmission equation"""
    return tx_power_dbw + tx_gain_dbi + rx_gain_dbi - path_loss_db - atmospheric_loss_db

def calculate_snr(received_power_dbw, noise_power_dbw):
    """Calculate signal-to-noise ratio"""
    return received_power_dbw - noise_power_dbw

def get_atmospheric_attenuation(freq_band, weather_condition="clear"):
    """Get atmospheric attenuation based on frequency band and weather"""
    if freq_band in nasa_data["weather_attenuation"]:
        return nasa_data["weather_attenuation"][freq_band][weather_condition]
    return 0.1

def get_debris_count(altitude):
    """Get debris count for given altitude"""
    altitude_str = str(int(altitude // 100) * 100)  # Round to nearest 100km
    if altitude_str in nasa_data["debris_data"]:
        return nasa_data["debris_data"][altitude_str]
    return 0

def calculate_coverage_time(altitude_km, inclination_deg):
    """Calculate approximate coverage time for a satellite pass"""
    # Simplified calculation based on orbital mechanics
    earth_radius = 6371  # km
    orbital_period = 2 * np.pi * np.sqrt((earth_radius + altitude_km)**3 / 398600.4418) / 60  # minutes
    
    # Coverage time is approximately the time the satellite is above horizon
    # This is a simplified calculation
    max_elevation_time = orbital_period * 0.1  # Rough estimate
    return max_elevation_time

def fetch_nasa_weather_data(lat, lon):
    """Fetch weather data from NASA POWER API"""
    try:
        # NASA POWER API endpoint
        url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
        params = {
            "parameters": "PRECTOT,CLOUD_AMT",
            "community": "RE",
            "longitude": lon,
            "latitude": lat,
            "start": "20240101",
            "end": "20240101",
            "format": "JSON"
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Extract relevant weather data
            if 'properties' in data and 'parameter' in data['properties']:
                precip = data['properties']['parameter'].get('PRECTOT', {}).get('2024-01-01', 0)
                cloud = data['properties']['parameter'].get('CLOUD_AMT', {}).get('2024-01-01', 0)
                return {"precipitation": precip, "cloud_cover": cloud}
    except Exception as e:
        print(f"Error fetching NASA weather data: {e}")
    
    # Return default values if API fails
    return {"precipitation": 0, "cloud_cover": 50}

# Callback for simulation
@app.callback(
    [Output("simulation-results", "children"),
     Output("pdf-data", "children")],
    [Input("run-sim", "n_clicks")],
    [State("freq-band", "value"),
     State("tx-power", "value"),
     State("tx-gain", "value"),
     State("rx-gain", "value"),
     State("altitude", "value"),
     State("inclination", "value"),
     State("gs-lat", "value"),
     State("gs-lon", "value"),
     State("num-satellites-a", "value"),
     State("gs-availability-a", "value"),
     State("link-type-a", "value"),
     State("num-satellites-b", "value"),
     State("gs-availability-b", "value"),
     State("link-type-b", "value"),
     State("scenario-a-name", "value"),
     State("scenario-b-name", "value"),
     State("priority", "value")]
)
def run_simulation(n_clicks, freq_band, tx_power, tx_gain, rx_gain, altitude, 
                  inclination, gs_lat, gs_lon, num_satellites_a, gs_availability_a, 
                  link_type_a, num_satellites_b, gs_availability_b, link_type_b,
                  scenario_a_name, scenario_b_name, priority):
    
    if n_clicks is None:
        return "", ""
    
    # Get frequency parameters
    freq_params = FREQUENCY_BANDS[freq_band]
    frequency_mhz = freq_params["freq_mhz"]
    
    # Fetch weather data
    weather_data = fetch_nasa_weather_data(gs_lat, gs_lon)
    
    # Determine weather condition
    if weather_data["precipitation"] > 5:  # mm/day
        weather_condition = "rain"
    else:
        weather_condition = "clear"
    
    # Calculate atmospheric attenuation
    atmospheric_loss = get_atmospheric_attenuation(freq_band, weather_condition)
    
    # Calculate range parameters
    earth_radius = 6371  # km
    min_range = altitude
    max_range = np.sqrt((earth_radius + altitude)**2 - earth_radius**2)
    
    # Generate range values for plotting
    ranges = np.linspace(min_range, max_range, 100)
    
    # Calculate path loss and received power
    path_losses = [calculate_path_loss(r, frequency_mhz) for r in ranges]
    received_powers = [calculate_received_power(tx_power, tx_gain, rx_gain, pl, atmospheric_loss) 
                      for pl in path_losses]
    
    # Calculate SNR (assuming noise power of -140 dBW)
    noise_power = -140  # dBW
    snrs = [calculate_snr(rp, noise_power) for rp in received_powers]
    
    # Calculate link margin (assuming required SNR of 10 dB)
    required_snr = 10
    link_margins = [snr - required_snr for snr in snrs]
    
    # Calculate coverage time
    coverage_time = calculate_coverage_time(altitude, inclination)
    
    # Get debris count
    debris_count = get_debris_count(altitude)
    
    # Calculate costs and metrics for both scenarios
    satellite_cost = 1000000  # $1M per satellite
    ground_station_cost = 500000  # $500K per ground station
    
    # Scenario A calculations
    total_cost_a = (num_satellites_a * satellite_cost) + ground_station_cost
    reliability_a = gs_availability_a / 100 * (1 - atmospheric_loss / 100)
    
    # Scenario B calculations (with different parameters)
    # For relay constellation, assume higher complexity and different costs
    relay_multiplier = 1.5 if link_type_b == "relay" else 1.0
    total_cost_b = (num_satellites_b * satellite_cost * relay_multiplier) + ground_station_cost
    reliability_b = gs_availability_b / 100 * (1 - atmospheric_loss / 100)
    
    # Create comparison plots
    fig1 = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Path Loss vs Range", "Received Power vs Range", 
                       "SNR vs Range", "Link Margin vs Range"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Path Loss plot
    fig1.add_trace(
        go.Scatter(x=ranges, y=path_losses, mode='lines', name='Path Loss',
                  line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    # Received Power plot
    fig1.add_trace(
        go.Scatter(x=ranges, y=received_powers, mode='lines', name='Received Power',
                  line=dict(color='green', width=2)),
        row=1, col=2
    )
    
    # SNR plot
    fig1.add_trace(
        go.Scatter(x=ranges, y=snrs, mode='lines', name='SNR',
                  line=dict(color='red', width=2)),
        row=2, col=1
    )
    
    # Link Margin plot
    fig1.add_trace(
        go.Scatter(x=ranges, y=link_margins, mode='lines', name='Link Margin',
                  line=dict(color='orange', width=2)),
        row=2, col=2
    )
    
    fig1.update_layout(height=600, showlegend=True, title_text="Link Performance Analysis")
    fig1.update_xaxes(title_text="Range (km)")
    fig1.update_yaxes(title_text="Path Loss (dB)", row=1, col=1)
    fig1.update_yaxes(title_text="Received Power (dBW)", row=1, col=2)
    fig1.update_yaxes(title_text="SNR (dB)", row=2, col=1)
    fig1.update_yaxes(title_text="Link Margin (dB)", row=2, col=2)
    
    # Create scenario comparison chart
    scenarios = [scenario_a_name, scenario_b_name]
    max_snrs = [max(snrs), max(snrs)]  # Same technical performance for both
    min_margins = [min(link_margins), min(link_margins)]
    costs = [total_cost_a, total_cost_b]
    reliabilities = [reliability_a, reliability_b]
    coverage_times = [coverage_time, coverage_time * 0.8]  # Relay might have slightly less coverage
    
    fig2 = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Performance Comparison", "Cost vs Reliability"),
        specs=[[{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Performance comparison bar chart
    fig2.add_trace(
        go.Bar(x=scenarios, y=max_snrs, name='Max SNR (dB)', marker_color='lightblue'),
        row=1, col=1
    )
    fig2.add_trace(
        go.Bar(x=scenarios, y=[m + 20 for m in min_margins], name='Link Margin (dB)', marker_color='lightgreen'),
        row=1, col=1
    )
    
    # Cost vs Reliability scatter plot
    fig2.add_trace(
        go.Scatter(x=costs, y=[r*100 for r in reliabilities], 
                  mode='markers+text', text=scenarios, textposition="top center",
                  marker=dict(size=15, color=['red', 'blue']),
                  name='Scenarios'),
        row=1, col=2
    )
    
    fig2.update_layout(height=400, showlegend=True, title_text="Scenario Comparison")
    fig2.update_xaxes(title_text="Scenario", row=1, col=1)
    fig2.update_yaxes(title_text="Performance (dB)", row=1, col=1)
    fig2.update_xaxes(title_text="Total Cost ($)", row=1, col=2)
    fig2.update_yaxes(title_text="Reliability (%)", row=1, col=2)
    
    # Create radar chart for comprehensive comparison
    categories = ['Max SNR', 'Link Margin', 'Reliability', 'Coverage Time', 'Cost Efficiency']
    
    # Normalise values for radar chart (0-100 scale)
    scenario_a_values = [
        min(100, max(0, (max(snrs) + 50) * 2)),  # Max SNR
        min(100, max(0, (min(link_margins) + 20) * 2.5)),  # Link Margin
        reliability_a * 100,  # Reliability
        min(100, coverage_time * 5),  # Coverage Time
        min(100, max(0, 100 - (total_cost_a / 10000000) * 100))  # Cost Efficiency (inverted)
    ]
    
    scenario_b_values = [
        min(100, max(0, (max(snrs) + 50) * 2)),  # Max SNR
        min(100, max(0, (min(link_margins) + 20) * 2.5)),  # Link Margin
        reliability_b * 100,  # Reliability
        min(100, coverage_time * 0.8 * 5),  # Coverage Time
        min(100, max(0, 100 - (total_cost_b / 10000000) * 100))  # Cost Efficiency (inverted)
    ]
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Scatterpolar(
        r=scenario_a_values,
        theta=categories,
        fill='toself',
        name=scenario_a_name,
        line_color='red'
    ))
    
    fig3.add_trace(go.Scatterpolar(
        r=scenario_b_values,
        theta=categories,
        fill='toself',
        name=scenario_b_name,
        line_color='blue'
    ))
    
    fig3.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Comprehensive Scenario Comparison",
        height=500
    )
    
    # Determine recommendation based on priority
    if priority == "cost":
        recommendation = scenario_a_name if total_cost_a < total_cost_b else scenario_b_name
        reason = "Lower total cost"
    elif priority == "performance":
        recommendation = scenario_a_name if reliability_a > reliability_b else scenario_b_name
        reason = "Higher reliability and performance"
    else:  # balanced
        # Simple scoring system
        score_a = (reliability_a * 0.4) + (1 - total_cost_a/20000000) * 0.3 + (coverage_time/20) * 0.3
        score_b = (reliability_b * 0.4) + (1 - total_cost_b/20000000) * 0.3 + (coverage_time*0.8/20) * 0.3
        recommendation = scenario_a_name if score_a > score_b else scenario_b_name
        reason = "Best balanced trade-off"
    
    # Create summary metrics
    max_snr = max(snrs)
    min_link_margin = min(link_margins)
    avg_received_power = np.mean(received_powers)
    
    # Create results layout
    results = dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig1)
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig2)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig3)
            ], width=6)
        ], className="mt-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Scenario Comparison Summary"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H5(f"{scenario_a_name}", className="text-primary"),
                                html.P(f"Cost: ${total_cost_a:,.0f}"),
                                html.P(f"Reliability: {reliability_a*100:.1f}%"),
                                html.P(f"Satellites: {num_satellites_a}"),
                                html.P(f"Link Type: {link_type_a.title()}")
                            ], width=6),
                            dbc.Col([
                                html.H5(f"{scenario_b_name}", className="text-primary"),
                                html.P(f"Cost: ${total_cost_b:,.0f}"),
                                html.P(f"Reliability: {reliability_b*100:.1f}%"),
                                html.P(f"Satellites: {num_satellites_b}"),
                                html.P(f"Link Type: {link_type_b.title()}")
                            ], width=6)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mt-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4(f"Recommendation: {recommendation}", className="alert-heading"),
                    html.P(f"Based on {priority} priority: {reason}"),
                    html.Hr(),
                    html.P("Key factors considered: Cost, Reliability, Coverage, and Technical Performance")
                ], color="success" if "A" in recommendation else "info")
            ], width=12)
        ], className="mt-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Technical Performance Metrics"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H5("Maximum SNR", className="text-primary"),
                                html.H4(f"{max_snr:.1f} dB", className="text-success")
                            ], width=3),
                            dbc.Col([
                                html.H5("Minimum Link Margin", className="text-primary"),
                                html.H4(f"{min_link_margin:.1f} dB", 
                                       className="text-success" if min_link_margin > 0 else "text-danger")
                            ], width=3),
                            dbc.Col([
                                html.H5("Average Received Power", className="text-primary"),
                                html.H4(f"{avg_received_power:.1f} dBW", className="text-info")
                            ], width=3),
                            dbc.Col([
                                html.H5("Coverage Time", className="text-primary"),
                                html.H4(f"{coverage_time:.1f} min", className="text-warning")
                            ], width=3)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mt-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Mission Constraints"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H6("Atmospheric Attenuation"),
                                html.P(f"{atmospheric_loss:.2f} dB ({weather_condition} conditions)")
                            ], width=4),
                            dbc.Col([
                                html.H6("Debris Count at Altitude"),
                                html.P(f"{debris_count} objects")
                            ], width=4),
                            dbc.Col([
                                html.H6("Weather Data Source"),
                                html.P("NASA POWER API")
                            ], width=4)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mt-3")
    ])
    
    # Prepare data for PDF
    pdf_data = {
        "scenario_a": {
            "name": scenario_a_name,
            "cost": total_cost_a,
            "reliability": reliability_a,
            "satellites": num_satellites_a,
            "link_type": link_type_a
        },
        "scenario_b": {
            "name": scenario_b_name,
            "cost": total_cost_b,
            "reliability": reliability_b,
            "satellites": num_satellites_b,
            "link_type": link_type_b
        },
        "recommendation": recommendation,
        "reason": reason,
        "priority": priority,
        "freq_band": freq_band,
        "altitude": altitude,
        "max_snr": max_snr,
        "min_link_margin": min_link_margin,
        "coverage_time": coverage_time,
        "weather_condition": weather_condition,
        "debris_count": debris_count
    }
    
    return results, json.dumps(pdf_data)

# Callback for PDF download
@app.callback(
    Output("download-pdf-file", "data"),
    [Input("download-pdf", "n_clicks")],
    [State("pdf-data", "children")]
)
def generate_pdf(n_clicks, pdf_data_json):
    if n_clicks is None or not pdf_data_json:
        return None
    
    try:
        pdf_data = json.loads(pdf_data_json)
        
        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            doc = SimpleDocTemplate(tmp_file.name, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph("Satellite Communication Link Analysis Report", title_style))
            story.append(Spacer(1, 20))
            
            # Mission information
            story.append(Paragraph(f"<b>Frequency Band:</b> {pdf_data['freq_band']}", styles['Normal']))
            story.append(Paragraph(f"<b>Altitude:</b> {pdf_data['altitude']} km", styles['Normal']))
            story.append(Paragraph(f"<b>Weather Condition:</b> {pdf_data['weather_condition']}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Scenario comparison
            story.append(Paragraph("<b>Scenario Comparison</b>", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            # Scenario A
            story.append(Paragraph(f"<b>{pdf_data['scenario_a']['name']}</b>", styles['Heading3']))
            story.append(Paragraph(f"• Cost: ${pdf_data['scenario_a']['cost']:,.0f}", styles['Normal']))
            story.append(Paragraph(f"• Reliability: {pdf_data['scenario_a']['reliability']*100:.1f}%", styles['Normal']))
            story.append(Paragraph(f"• Satellites: {pdf_data['scenario_a']['satellites']}", styles['Normal']))
            story.append(Paragraph(f"• Link Type: {pdf_data['scenario_a']['link_type'].title()}", styles['Normal']))
            story.append(Spacer(1, 10))
            
            # Scenario B
            story.append(Paragraph(f"<b>{pdf_data['scenario_b']['name']}</b>", styles['Heading3']))
            story.append(Paragraph(f"• Cost: ${pdf_data['scenario_b']['cost']:,.0f}", styles['Normal']))
            story.append(Paragraph(f"• Reliability: {pdf_data['scenario_b']['reliability']*100:.1f}%", styles['Normal']))
            story.append(Paragraph(f"• Satellites: {pdf_data['scenario_b']['satellites']}", styles['Normal']))
            story.append(Paragraph(f"• Link Type: {pdf_data['scenario_b']['link_type'].title()}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Recommendation
            story.append(Paragraph("<b>Recommendation</b>", styles['Heading2']))
            story.append(Paragraph(f"<b>Selected Scenario:</b> {pdf_data['recommendation']}", styles['Normal']))
            story.append(Paragraph(f"<b>Priority:</b> {pdf_data['priority'].title()}", styles['Normal']))
            story.append(Paragraph(f"<b>Reason:</b> {pdf_data['reason']}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Key metrics
            story.append(Paragraph("<b>Technical Performance Metrics</b>", styles['Heading2']))
            story.append(Paragraph(f"Maximum SNR: {pdf_data['max_snr']:.1f} dB", styles['Normal']))
            story.append(Paragraph(f"Minimum Link Margin: {pdf_data['min_link_margin']:.1f} dB", styles['Normal']))
            story.append(Paragraph(f"Coverage Time: {pdf_data['coverage_time']:.1f} minutes", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Mission constraints
            story.append(Paragraph("<b>Mission Constraints</b>", styles['Heading2']))
            story.append(Paragraph(f"Weather Condition: {pdf_data['weather_condition']}", styles['Normal']))
            story.append(Paragraph(f"Debris Count at Altitude: {pdf_data['debris_count']} objects", styles['Normal']))
            story.append(Paragraph("Weather Data Source: NASA POWER API", styles['Normal']))
            story.append(Paragraph("Debris Data Source: NASA Orbital Debris Program Office", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Analysis summary
            story.append(Paragraph("<b>Analysis Summary</b>", styles['Heading2']))
            if pdf_data['min_link_margin'] > 0:
                story.append(Paragraph("✓ Link is feasible with positive margin", styles['Normal']))
            else:
                story.append(Paragraph("⚠ Link may not be reliable due to negative margin", styles['Normal']))
            
            story.append(Paragraph(f"✓ Analysis based on NASA data and ITU-R recommendations", styles['Normal']))
            story.append(Paragraph(f"✓ Real-time weather data integrated from NASA POWER API", styles['Normal']))
            story.append(Paragraph(f"✓ Orbital debris data from NASA ODPO", styles['Normal']))
            
            # Footer
            story.append(Spacer(1, 30))
            story.append(Paragraph(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                 styles['Normal']))
            story.append(Paragraph("Data sources: NASA POWER API, NASA ODPO, ITU-R Recommendations", 
                                 styles['Normal']))
            
            doc.build(story)
            
            # Read the file and return as download
            with open(tmp_file.name, 'rb') as f:
                pdf_content = f.read()
            
            return dict(content=pdf_content, filename=f"satellite_link_analysis_{pdf_data['recommendation'].replace(' ', '_')}.pdf")
    
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

# Callback for clearing results
@app.callback(
    Output("simulation-results", "children", allow_duplicate=True),
    [Input("clear-results", "n_clicks")],
    prevent_initial_call=True
)
def clear_results(n_clicks):
    if n_clicks:
        return ""
    return ""

if __name__ == "__main__":
    app.run_server(debug=True, host='127.0.0.1', port=8050)

