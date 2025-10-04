import streamlit as st
import pandas as pd
import numpy as np
from constellations import Satellite, GroundStation, create_default_constellation, create_default_ground_stations
from simulation import ConstellationSimulator, calculate_coverage_metrics
from cost_model import (calculate_cost_comparison, generate_cost_summary, calculate_roi_metrics,
                        calculate_tipping_point, calculate_payback_period)
from plots import (plot_snr_vs_time, plot_latency_vs_time, plot_availability, 
                   plot_cost_comparison, plot_cost_breakdown, plot_link_type_distribution,
                   plot_satellite_coverage_heatmap, plot_distance_distribution)
from debris_analysis import (calculate_collision_probability, calculate_deorbit_requirements,
                             calculate_debris_mitigation_costs, calculate_sustainability_score,
                             get_nasa_debris_recommendations)
from regulatory_compliance import (get_licensing_requirements, get_frequency_coordination_status,
                                  get_international_cooperation_opportunities, calculate_compliance_timeline,
                                  get_regulatory_risk_assessment)
from business_model import (get_service_tiers, calculate_revenue_projections, get_market_analysis,
                            get_competitive_landscape, calculate_profitability, get_go_to_market_strategy)

# Page configuration
st.set_page_config(
    page_title="LEO Link Simulator",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'use_nasa_data' not in st.session_state:
    st.session_state.use_nasa_data = False
if 'selected_constellation' not in st.session_state:
    st.session_state.selected_constellation = 'Starlink'
if 'num_satellites' not in st.session_state:
    st.session_state.num_satellites = 6
if 'orbit_altitude_km' not in st.session_state:
    st.session_state.orbit_altitude_km = 550
if 'results' not in st.session_state:
    st.session_state.results = None
if 'metrics' not in st.session_state:
    st.session_state.metrics = None
if 'cost_summary' not in st.session_state:
    st.session_state.cost_summary = None
if 'cost_comparison' not in st.session_state:
    st.session_state.cost_comparison = None

# Title and description
st.title("LEO Satellite Link Feasibility Simulator")
st.markdown("""
**Constellation Architecture Decision Support**

Compare ground-station-only versus crosslinked architectures.

**Analysis includes:**
- Cost comparison and ROI calculation
- Performance metrics: latency, coverage, SNR, availability
- Real constellation benchmarking: Starlink, GPS, OneWeb, Iridium, ISS
- Downloadable executive reports

**Use cases:** Architecture decisions, feasibility studies, competitive analysis, investor presentations
""")

# Sidebar - Input Parameters
st.sidebar.header("Configuration")
st.sidebar.markdown("Hover over info icons for details")

# Satellite parameters
st.sidebar.subheader("Satellite Parameters")

num_satellites = st.sidebar.slider(
    "Number of Satellites", 
    4, 12, 6,
    help="""
    **What it is:** Total number of satellites in your constellation.
    
    **Why it matters:** More satellites = better global coverage but higher costs.
    
    **Real examples:**
    - Starlink: 6,000+ satellites
    - Iridium: 66 satellites
    - GPS: 31 satellites
    
    **Impact:** Affects coverage percentage, redundancy, and total constellation cost.
    """
)

orbit_altitude_km = st.sidebar.slider(
    "Orbit Altitude (km)", 
    400, 800, 500, 50,
    help="""
    **What it is:** Height above Earth's surface where satellites orbit.
    
    **Why it matters:** 
    - Lower altitude = Lower latency BUT shorter coverage per satellite
    - Higher altitude = Longer coverage BUT higher latency
    
    **LEO (Low Earth Orbit):** 400-800 km
    - Starlink: 340-550 km
    - ISS: 408 km
    - OneWeb: 1,200 km
    
    **Key trade-offs:**
    - Lower: Faster signals, more satellites needed
    - Higher: Fewer satellites, slower signals
    
    **Physics:** Orbital period increases with altitude (Kepler's laws).
    """
)

transmit_power_dBW = st.sidebar.slider(
    "Transmit Power (dBW)", 
    10, 30, 20,
    help="""
    **What it is:** Transmitter power output in decibels relative to 1 Watt (dBW).
    
    **Why it matters:** Higher power = stronger signal BUT more battery/solar power needed.
    
    **Power scale:**
    - 10 dBW = 10 Watts
    - 20 dBW = 100 Watts (typical)
    - 30 dBW = 1,000 Watts
    
    **Key term - dBW:** Logarithmic scale
    - Every +3 dB = doubles the power
    - Every +10 dB = 10× the power
    
    **Trade-offs:**
    - More power = Better SNR, longer range
    - More power = Larger solar panels, heavier satellite, higher cost
    
    **Impact:** Directly affects link budget and signal quality (SNR).
    """
)

antenna_gain_dBi = st.sidebar.slider(
    "Antenna Gain (dBi)", 
    10, 30, 20,
    help="""
    **What it is:** How well the antenna focuses radio waves in a specific direction.
    
    **Why it matters:** Higher gain = stronger focused signal, like a flashlight vs. a laser.
    
    **Gain scale:**
    - 0 dBi = Omnidirectional (radiates equally in all directions)
    - 10 dBi = Moderate focusing
    - 20 dBi = Good focusing (typical satellite)
    - 30 dBi = Very focused (ground stations)
    - 74 dBi = NASA Deep Space Network (huge dishes!)
    
    **Key term - dBi:** "decibels relative to isotropic radiator"
    - Isotropic = theoretical perfect omnidirectional antenna
    
    **Trade-offs:**
    - Higher gain = Better signal BUT narrower beam (pointing matters!)
    - Lower gain = Wider coverage BUT weaker signal
    
    **Real examples:**
    - Satellite antennas: 15-25 dBi
    - Ground stations: 30-50 dBi
    - NASA DSN: 74 dBi
    
    **Impact:** Critical for link budget - both transmit and receive gain matter!
    """
)

frequency_GHz = st.sidebar.slider(
    "Frequency (GHz)", 
    1.0, 30.0, 2.4, 0.1,
    help="""
    **What it is:** Radio frequency used for communication (GHz = gigahertz = billions of cycles/second).
    
    **Why it matters:** Different frequencies have different properties (range, weather sensitivity, regulations).
    
    **Common satellite bands:**
    - L-band: 1-2 GHz - GPS, mobile satellites
    - S-band: 2-4 GHz - Weather satellites, WiFi (2.4 GHz)
    - C-band: 4-8 GHz - Many satellites
    - X-band: 8-12 GHz - Military, NASA
    - Ku-band: 12-18 GHz - TV, internet satellites
    - Ka-band: 26-40 GHz - High-speed data
    
    **Trade-offs:**
    
    **Lower frequencies (1-4 GHz):**
    ✅ Better weather penetration
    ✅ Larger coverage area
    ❌ Larger antennas needed
    ❌ More crowded spectrum
    
    **Higher frequencies (12-30 GHz):**
    ✅ More bandwidth (faster data)
    ✅ Smaller antennas
    ❌ Rain attenuation (signal loss in storms)
    ❌ Atmospheric absorption
    
    **Physics:** Higher frequency = shorter wavelength = more path loss
    
    **Impact:** Affects path loss calculation in Friis equation.
    """
)

# Ground station parameters
st.sidebar.subheader("Ground Station Configuration")

num_gs_ground_only = st.sidebar.slider(
    "Ground Stations (GS-Only)", 
    3, 10, 5,
    help="""
    **What it is:** Number of ground stations for the traditional architecture.
    
    **Why it matters:** In ground-station-only mode, satellites ONLY talk to ground stations.
    
    **How it works:**
    - Satellites pass overhead
    - Transmit data when in range (typically 5-10 minutes per pass)
    - Must wait for next ground station pass
    
    **Key challenges:**
    - Need global distribution for coverage
    - Data delayed until ground station contact
    - High latency (data bounces: satellite → ground → internet → ground → satellite)
    
    **Real-world costs:**
    - Each ground station: ~$5M (construction, equipment, operations)
    - More stations = better coverage BUT much higher cost
    
    **Impact:** More stations = better uptime BUT higher CapEx in cost analysis.
    """
)

num_gs_crosslinked = st.sidebar.slider(
    "Ground Stations (Crosslinked)", 
    1, 5, 2,
    help="""
    **What it is:** Number of ground stations for crosslinked architecture.
    
    **Why it matters:** With Inter-Satellite Links (ISL), you need FEWER ground stations!
    
    **How crosslinking works:**
    1. Satellite A receives data
    2. Satellite A talks to Satellite B via laser/radio (ISL)
    3. Data hops across constellation
    4. Any satellite can downlink to nearest ground station
    
    **Key advantages:**
    - Data finds fastest path through constellation
    - Much lower latency (direct satellite-to-satellite)
    - Reduced ground infrastructure
    - Better global coverage
    
    **Real examples:**
    - Starlink Gen2: Uses laser crosslinks, fewer ground stations
    - Traditional systems: 10-20+ ground stations globally
    
    **Cost impact:**
    - Fewer ground stations = -$15M+ savings
    - ISL hardware per satellite: +$500K
    - **Net result: Often 40-60% cost savings!**
    
    **Impact:** Key differentiator in cost comparison - this is why crosslinking wins!
    """
)

# NASA Data Integration
st.sidebar.subheader("NASA Data (Optional)")
use_nasa_tle = st.sidebar.checkbox(
    "Use Real NASA TLE Data", 
    value=False,
    help="""
    When UNCHECKED (default):
    - Uses simulated constellation you configure above
    - Creates fake satellites at your specified altitude
    - Fast simulation (5-10 seconds)
    - Good for testing your own designs
    
    When CHECKED:
    - Loads real satellite positions from NASA/NORAD
    - Ignores "Number of Satellites" and "Orbit Altitude" settings above
    - Uses actual constellation data (Starlink, GPS, etc.)
    - Slower simulation (may have 100s or 1000s of satellites)
    - Good for analyzing existing systems
    
    TLE = Two-Line Element format
    Standard orbital data updated daily by NASA/NORAD
    """
)

if use_nasa_tle:
    tle_source = st.sidebar.selectbox(
        "Select Constellation",
        ["Starlink", "OneWeb", "Iridium", "GPS", "ISS"],
        help="""
        **Available Constellations:**
        
        **Starlink** (SpaceX)
        - 6,000+ satellites at 340-550 km
        - Internet service
        - Uses laser crosslinks
        
        **OneWeb**
        - 600+ satellites at 1,200 km
        - Internet service
        - Global coverage focus
        
        **Iridium**
        - 66 satellites at 780 km
        - Voice & data communications
        - Polar orbits
        
        **GPS** (Navigation)
        - 31 satellites at 20,200 km
        - Global positioning
        - Very high altitude
        
        **ISS** (Space Station)
        - 1 "satellite" at 408 km
        - Easiest to simulate (just 1!)
        - Good for testing
        
        **Tip:** Start with ISS or GPS (fewer satellites = faster).
        """
    )
    tle_file_map = {
        "Starlink": "data/tle/starlink.txt",
        "OneWeb": "data/tle/oneweb.txt",
        "Iridium": "data/tle/iridium.txt",
        "GPS": "data/tle/gps.txt",
        "ISS": "data/tle/iss.txt"
    }
    tle_filepath = tle_file_map[tle_source]
    
    # Option to use NASA ground stations
    use_nasa_gs = st.sidebar.checkbox(
        "Use NASA Ground Stations", 
        value=False,
        help="""
        **What it is:** Use real NASA ground station locations instead of simulated ones.
        
        **Available networks:**
        
        **NEN (Near Earth Network):**
        - White Sands, New Mexico
        - Alaska Ground Station  
        - Svalbard, Norway
        - Purpose: LEO satellite communications
        - Antenna gain: 40-45 dBi
        
        **DSN (Deep Space Network):**
        - Goldstone, California
        - Canberra, Australia
        - Madrid, Spain
        - Purpose: Deep space missions
        - Antenna gain: 74 dBi (HUGE dishes!)
        
        **Both:** All 6 NASA stations
        
        **Why use it:** More realistic ground infrastructure for your analysis.
        """
    )
    if use_nasa_gs:
        nasa_network = st.sidebar.selectbox(
            "NASA Network",
            ["NEN", "DSN", "Both"],
            help="""
            **NEN:** Near Earth Network - Best for LEO satellites (your use case!)
            **DSN:** Deep Space Network - For very distant spacecraft
            **Both:** All 6 NASA stations combined
            
            **Recommendation:** Use NEN for LEO constellation analysis.
            """
        )
else:
    use_nasa_gs = False

# Simulation parameters
st.sidebar.subheader("Simulation Settings")

time_steps = st.sidebar.slider(
    "Time Steps", 
    50, 200, 100, 10,
    help="""
    **What it is:** Number of calculation points during one orbital period.
    
    **Why it matters:** More steps = more accurate BUT slower simulation.
    
    **Time step guide:**
    - **50 steps:** Quick demo (10-15 seconds)
    - **100 steps:** Balanced (15-30 seconds) ✅ Recommended
    - **200 steps:** Very detailed (30-60 seconds)
    
    **What happens at each step:**
    1. Update satellite positions
    2. Check line-of-sight to ground stations
    3. Calculate link budget (Friis equation)
    4. Compute SNR and latency
    5. Record coverage data
    
    **Trade-off:**
    - More steps = smoother plots, better accuracy
    - More steps = longer wait time
    
    **Tip:** Use 50 for NASA data (lots of satellites), 100 for default data.
    """
)

orbit_period_minutes = st.sidebar.slider(
    "Orbit Period (minutes)", 
    80, 100, 90,
    help="""
    **What it is:** Time for one complete orbit around Earth.
    
    **Why it matters:** This is the total simulation time - we simulate one full orbit.
    
    **Physics (Kepler's Third Law):**
    Orbital period depends on altitude:
    - 400 km altitude ≈ 92 minutes
    - 500 km altitude ≈ 95 minutes (LEO typical)
    - 800 km altitude ≈ 101 minutes
    
    **Real examples:**
    - ISS at 408 km: ~93 minutes
    - Starlink at 550 km: ~96 minutes
    - Iridium at 780 km: ~100 minutes
    
    **What we calculate:**
    Formula: T = 2π√(r³/μ)
    - T = period
    - r = orbit radius (Earth radius + altitude)
    - μ = Earth's gravitational parameter
    
    **Impact:** Simulation runs for this duration - one complete orbital pass.
    
    **Tip:** 90 minutes is good for most LEO simulations.
    """
)

# Run simulation button
run_simulation = st.sidebar.button("Run Simulation", type="primary", use_container_width=True)

# Initialize session state
if 'simulation_complete' not in st.session_state:
    st.session_state.simulation_complete = False
    st.session_state.results = None
    st.session_state.metrics = None
    st.session_state.cost_comparison = None

# Run simulation when button is clicked
if run_simulation:
    with st.spinner("Running simulation... This may take a moment."):
        try:
            # Create constellation - NASA TLE or Default
            if use_nasa_tle:
                try:
                    from nasa_data_integration import load_constellation_from_tle
                    st.info(f"Loading {tle_source} constellation from NASA TLE data...")
                    satellites = load_constellation_from_tle(tle_filepath)
                    
                    # Update satellite parameters
                    for sat in satellites:
                        sat.transmit_power_dBW = transmit_power_dBW
                        sat.antenna_gain_dBi = antenna_gain_dBi
                        sat.frequency_GHz = frequency_GHz
                    
                    st.success(f"Loaded {len(satellites)} real satellites from {tle_source} constellation")
                    
                except FileNotFoundError:
                    st.warning(f"TLE file not found: {tle_filepath}")
                    st.info("Downloading TLE data from CelesTrak...")
                    
                    # Download the TLE file
                    import urllib.request
                    tle_urls = {
                        "Starlink": "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle",
                        "OneWeb": "https://celestrak.org/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=tle",
                        "Iridium": "https://celestrak.org/NORAD/elements/gp.php?GROUP=iridium&FORMAT=tle",
                        "GPS": "https://celestrak.org/NORAD/elements/gp.php?GROUP=gps-ops&FORMAT=tle",
                        "ISS": "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"
                    }
                    
                    urllib.request.urlretrieve(tle_urls[tle_source], tle_filepath)
                    st.success(f"Downloaded {tle_source} TLE data from CelesTrak")
                    
                    # Try loading again
                    from nasa_data_integration import load_constellation_from_tle
                    satellites = load_constellation_from_tle(tle_filepath)
                    
                    # Update satellite parameters
                    for sat in satellites:
                        sat.transmit_power_dBW = transmit_power_dBW
                        sat.antenna_gain_dBi = antenna_gain_dBi
                        sat.frequency_GHz = frequency_GHz
                    
                    st.success(f"Loaded {len(satellites)} real satellites")
                    
                except Exception as e:
                    st.error(f"Error loading NASA TLE data: {e}")
                    st.info("Using default constellation instead...")
                    satellites = create_default_constellation(
                        num_satellites=num_satellites,
                        altitude_km=orbit_altitude_km
                    )
                    # Update satellite parameters
                    for sat in satellites:
                        sat.transmit_power_dBW = transmit_power_dBW
                        sat.antenna_gain_dBi = antenna_gain_dBi
                        sat.frequency_GHz = frequency_GHz
            else:
                # Use default constellation
                satellites = create_default_constellation(
                    num_satellites=num_satellites,
                    altitude_km=orbit_altitude_km
                )
                
                # Update satellite parameters
                for sat in satellites:
                    sat.transmit_power_dBW = transmit_power_dBW
                    sat.antenna_gain_dBi = antenna_gain_dBi
                    sat.frequency_GHz = frequency_GHz
            
            # Create ground stations - NASA or Default
            if use_nasa_tle and use_nasa_gs:
                from nasa_data_integration import create_nasa_ground_stations
                ground_stations = create_nasa_ground_stations(network=nasa_network)
                st.success(f"Using {len(ground_stations)} NASA {nasa_network} ground stations")
            else:
                ground_stations = create_default_ground_stations()
                if not use_nasa_tle:
                    st.info(f"Using simulated constellation: {num_satellites} satellites at {orbit_altitude_km} km altitude")
            
            # Create simulator
            simulator = ConstellationSimulator(satellites, ground_stations)
            
            # Run simulations
            results = simulator.run_comparison_simulation(
                time_steps=time_steps,
                orbit_period_minutes=orbit_period_minutes
            )
            
            # Calculate metrics
            gs_metrics = calculate_coverage_metrics(results['ground_station_only'])
            cl_metrics = calculate_coverage_metrics(results['crosslinked'])
            
            # Calculate costs
            cost_comparison = calculate_cost_comparison(
                num_satellites=num_satellites,
                num_gs_ground_only=num_gs_ground_only,
                num_gs_crosslinked=num_gs_crosslinked
            )
            cost_summary = generate_cost_summary(cost_comparison)
            
            # Store in session state
            st.session_state.simulation_complete = True
            st.session_state.results = results
            st.session_state.metrics = {
                'ground_station_only': gs_metrics,
                'crosslinked': cl_metrics
            }
            st.session_state.cost_comparison = cost_comparison
            st.session_state.cost_summary = cost_summary
            
            # Update data source information
            st.session_state.use_nasa_data = use_nasa_tle
            st.session_state.selected_constellation = tle_source if use_nasa_tle else 'Simulated'
            st.session_state.num_satellites = len(satellites)
            st.session_state.orbit_altitude_km = orbit_altitude_km
            st.session_state.num_gs_ground_only = num_gs_ground_only
            st.session_state.num_gs_crosslinked = num_gs_crosslinked
            
            st.success("Simulation complete. View results in tabs above.")
            
        except Exception as e:
            st.error(f"Simulation failed: {str(e)}")
            st.exception(e)

# Display results if simulation is complete
if st.session_state.simulation_complete:
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Simulation Results", 
        "Cost Analysis", 
        "Value Dashboard", 
        "Data Tables", 
        "Executive Report",
        "Sustainability & Debris",
        "Regulatory Compliance",
        "Business Model"
    ])
    
    with tab1:
        st.header("Simulation Results")
        
        # Get data
        df_ground = st.session_state.results['ground_station_only']
        df_crosslink = st.session_state.results['crosslinked']
        gs_metrics = st.session_state.metrics['ground_station_only']
        cl_metrics = st.session_state.metrics['crosslinked']
        
        # Data source indicator
        if st.session_state.get('use_nasa_data', False):
            data_source = st.session_state.get('selected_constellation', 'Unknown')
            st.info(f"📡 **Using Real NASA Data:** {data_source} constellation with actual satellite positions from NASA/NORAD tracking")
        else:
            data_source = "Simulated"
            num_sats = st.session_state.get('num_satellites', 6)
            alt_km = st.session_state.get('orbit_altitude_km', 550)
            st.info(f"🛰️ **Using Simulated Data:** Custom constellation with {num_sats} satellites at {alt_km} km altitude")
        
        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "GS-Only Coverage",
                f"{gs_metrics['coverage_percentage']:.1f}%",
                help="Percentage of time satellites have usable link to ground stations (SNR ≥ 10 dB + line of sight)"
            )
        
        with col2:
            st.metric(
                "Crosslinked Coverage",
                f"{cl_metrics['coverage_percentage']:.1f}%",
                delta=f"{cl_metrics['coverage_percentage'] - gs_metrics['coverage_percentage']:.1f}%",
                help="Percentage of time usable path exists via satellite-to-satellite links + minimal ground stations"
            )
        
        with col3:
            st.metric(
                "GS-Only Avg Latency",
                f"{gs_metrics['average_latency_ms']:.1f} ms",
                help="Average communication latency: satellite → ground station → satellite (includes ground processing)"
            )
        
        with col4:
            st.metric(
                "Crosslinked Avg Latency",
                f"{cl_metrics['average_latency_ms']:.1f} ms",
                delta=f"{cl_metrics['average_latency_ms'] - gs_metrics['average_latency_ms']:.1f} ms",
                delta_color="inverse",
                help="Average communication latency: satellite → satellite (direct space routing)"
            )
        
        st.divider()
        
        # Plots with explanations
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                plot_snr_vs_time(df_ground, df_crosslink),
                use_container_width=True
            )
            st.markdown("""
            **Signal-to-Noise Ratio (SNR) Over Time**
            
            - **Red line (Ground Station Only):** SNR for satellite-to-ground links
            - **Teal line (Crosslinked):** SNR for satellite-to-satellite links  
            - **Dashed line at 10 dB:** Feasibility threshold (links below this fail)
            - **What to look for:** Both lines should stay well above 10 dB. If they dip close, increase antenna gain or reduce distance.
            """)
        
        with col2:
            st.plotly_chart(
                plot_latency_vs_time(df_ground, df_crosslink),
                use_container_width=True
            )
            st.markdown("""
            **Communication Latency Over Time**
            
            - **Red line (Ground Station Only):** ~500-1000 ms (satellite → ground → satellite + processing)
            - **Teal line (Crosslinked):** ~30-50 ms (satellite → satellite direct)
            - **What to look for:** Lower is better. Crosslinks should be consistently lower and flatter.
            - **Target:** <100 ms for interactive applications, <50 ms for real-time control
            """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                plot_availability(df_ground, df_crosslink),
                use_container_width=True
            )
            st.markdown("""
            **Coverage and Availability Comparison**
            
            - **Coverage %:** Fraction of time any usable link exists
            - **Uptime %:** Same as coverage (treats all outages as downtime)
            - **What to look for:** Higher is better. Crosslinks often achieve near 100% coverage.
            - **Action:** If ground-only coverage is low, add ground stations or switch to crosslinks
            """)
        
        with col2:
            st.plotly_chart(
                plot_distance_distribution(df_ground, df_crosslink),
                use_container_width=True
            )
            st.markdown("""
            **Link Distance Distribution**
            
            - **Red bars (Ground Station Only):** Satellite-to-ground distances
            - **Teal bars (Crosslinked):** Satellite-to-satellite distances
            - **What to look for:** Shorter distances = better SNR. Peak around 12-16k km is typical for LEO.
            - **Action:** If distances are too long, add intermediate satellites or lower altitude
            """)
        
        # Additional visualizations
        st.subheader("Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                plot_link_type_distribution(df_crosslink),
                use_container_width=True
            )
            st.markdown("""
            **Link Type Distribution (Crosslinked Only)**
            
            - **Satellite-to-Satellite (Teal):** Direct space links (most common in crosslinked networks)
            - **Satellite-to-Ground (Red):** Links to ground stations (minimal in crosslinked networks)
            - **What to look for:** High satellite-to-satellite percentage means network relies on crosslinks
            - **Action:** If ground percentage is high, you may need more satellites or better orbital phasing
            """)
        
        with col2:
            st.plotly_chart(
                plot_satellite_coverage_heatmap(df_ground),
                use_container_width=True
            )
            st.markdown("""
            **Satellite Coverage Heatmap (Ground Station Only)**
            
            - **Rows:** Individual satellites
            - **Columns:** Time steps during simulation
            - **Colors:** Yellow = good coverage, Purple = no coverage
            - **What to look for:** Continuous yellow bands = consistent coverage. Purple gaps = coverage holes.
            - **Action:** Identify satellites with gaps and add ground stations in those regions
            """)
    
    with tab2:
        st.header("Cost Analysis")
        
        # Data source indicator
        if st.session_state.get('use_nasa_data', False):
            constellation = st.session_state.get('selected_constellation', 'Unknown')
            st.info(f"📡 **Cost Analysis for:** {constellation} constellation (NASA data)")
        else:
            num_sats = st.session_state.get('num_satellites', 6)
            st.info(f"🛰️ **Cost Analysis for:** Simulated constellation with {num_sats} satellites")
        
        cost_summary = st.session_state.cost_summary
        
        # Cost savings highlight
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Cost Savings",
                f"${cost_summary['total_savings_usd']/1e6:.1f}M",
                delta=f"{cost_summary['savings_percentage']:.1f}%",
                help="Total CapEx savings with crosslinked architecture"
            )
        
        with col2:
            st.metric(
                "Ground Stations Reduced",
                f"{cost_summary['gs_reduction_count']}",
                delta=f"-{cost_summary['gs_reduction_percentage']:.0f}%",
                help="Fewer ground stations needed"
            )
        
        with col3:
            st.metric(
                "Recommendation",
                cost_summary['recommendation'],
                help="Recommended architecture based on cost analysis"
            )
        
        st.divider()
        
        # Cost visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                plot_cost_comparison(cost_summary),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                plot_cost_breakdown(cost_summary),
                use_container_width=True
            )
        
        # Detailed cost breakdown
        st.subheader("Detailed Cost Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ground Station Only")
            gs_only = cost_summary['gs_only_breakdown']
            for component, cost in gs_only.items():
                st.write(f"**{component}:** ${cost/1e6:.2f}M")
            st.write(f"**Total:** ${cost_summary['gs_only_capex']/1e6:.2f}M")
        
        with col2:
            st.markdown("#### Crosslinked")
            crosslinked = cost_summary['crosslinked_breakdown']
            for component, cost in crosslinked.items():
                st.write(f"**{component}:** ${cost/1e6:.2f}M")
            st.write(f"**Total:** ${cost_summary['crosslinked_capex']/1e6:.2f}M")
    
    with tab3:
        st.header("Value Dashboard")
        
        # Data source indicator
        if st.session_state.get('use_nasa_data', False):
            constellation = st.session_state.get('selected_constellation', 'Unknown')
            st.info(f"📡 **Performance Summary for:** {constellation} constellation (NASA data)")
        else:
            num_sats = st.session_state.get('num_satellites', 6)
            st.info(f"🛰️ **Performance Summary for:** Simulated constellation with {num_sats} satellites")
        
        gs_metrics = st.session_state.metrics['ground_station_only']
        cl_metrics = st.session_state.metrics['crosslinked']
        cost_summary = st.session_state.cost_summary
        
        # Calculate improvements
        latency_improvement = gs_metrics['average_latency_ms'] - cl_metrics['average_latency_ms']
        latency_improvement_pct = (latency_improvement / gs_metrics['average_latency_ms']) * 100
        
        coverage_improvement = cl_metrics['coverage_percentage'] - gs_metrics['coverage_percentage']
        
        snr_improvement = cl_metrics['average_snr_dB'] - gs_metrics['average_snr_dB']
        
        # ROI metrics
        roi_metrics = calculate_roi_metrics(
            st.session_state.cost_comparison,
            latency_improvement,
            coverage_improvement
        )
        
        # Value metrics
        st.subheader("🎯 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Latency Reduction",
                f"{latency_improvement:.1f} ms",
                delta=f"-{latency_improvement_pct:.1f}%",
                delta_color="inverse",
                help="Communication latency improvement"
            )
        
        with col2:
            st.metric(
                "Coverage Improvement",
                f"+{coverage_improvement:.1f}%",
                help="Increase in link availability"
            )
        
        with col3:
            st.metric(
                "SNR Improvement",
                f"+{snr_improvement:.1f} dB",
                help="Signal quality improvement"
            )
        
        with col4:
            st.metric(
                "ROI",
                f"{roi_metrics['roi_percentage']:.0f}%",
                help="Return on Investment for crosslinked architecture"
            )
        
        st.divider()
        
        # Value proposition
        st.subheader("💡 Value Proposition Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Benefits of Crosslinked Architecture")
            st.write(f"- **{cost_summary['savings_percentage']:.1f}%** CapEx savings (${cost_summary['total_savings_usd']/1e6:.1f}M)")
            st.write(f"- **{coverage_improvement:.1f}%** higher coverage")
            st.write(f"- **{latency_improvement_pct:.1f}%** latency reduction ({latency_improvement:.0f} ms faster)")
            st.write(f"- **{cost_summary['gs_reduction_count']}** fewer ground stations required")
            st.write(f"- **{snr_improvement:.1f} dB** better signal quality")
        
        with col2:
            st.markdown("### 📊 Business Impact")
            st.write(f"- **Total Value Created:** ${roi_metrics['total_value']/1e6:.1f}M")
            st.write(f"- **Cost Savings:** ${roi_metrics['cost_savings_value']/1e6:.1f}M")
            st.write(f"- **Performance Value:** ${(roi_metrics['latency_improvement_value'] + roi_metrics['coverage_improvement_value'])/1e6:.1f}M")
            st.write(f"- **ROI:** {roi_metrics['roi_percentage']:.0f}%")
            st.write(f"- **Recommended Strategy:** {cost_summary['recommendation']}")
        
        # Operational benefits
        st.subheader("🔧 Operational Benefits")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Network Resilience")
            st.write(f"- Multiple communication paths")
            st.write(f"- Reduced single point of failure")
            st.write(f"- {cl_metrics['uptime_percentage']:.1f}% uptime")
        
        with col2:
            st.markdown("#### Performance")
            st.write(f"- {cl_metrics['average_latency_ms']:.1f} ms avg latency")
            st.write(f"- {cl_metrics['average_snr_dB']:.1f} dB avg SNR")
            st.write(f"- {cl_metrics['feasible_percentage']:.1f}% feasible links")
        
        with col3:
            st.markdown("#### Infrastructure")
            st.write(f"- {num_gs_crosslinked} ground stations")
            st.write(f"- {num_satellites} satellites")
            st.write(f"- Reduced ground complexity")
    
    with tab4:
        st.header("Data Tables")
        
        # Metrics comparison table
        st.subheader("Metrics Comparison")
        
        metrics_df = pd.DataFrame({
            'Metric': [
                'Coverage (%)',
                'Feasible Links (%)',
                'Average Latency (ms)',
                'Average SNR (dB)',
                'Downtime (minutes)',
                'Uptime (%)'
            ],
            'Ground Station Only': [
                f"{gs_metrics['coverage_percentage']:.2f}",
                f"{gs_metrics['feasible_percentage']:.2f}",
                f"{gs_metrics['average_latency_ms']:.2f}",
                f"{gs_metrics['average_snr_dB']:.2f}",
                f"{gs_metrics['downtime_minutes']:.2f}",
                f"{gs_metrics['uptime_percentage']:.2f}"
            ],
            'Crosslinked': [
                f"{cl_metrics['coverage_percentage']:.2f}",
                f"{cl_metrics['feasible_percentage']:.2f}",
                f"{cl_metrics['average_latency_ms']:.2f}",
                f"{cl_metrics['average_snr_dB']:.2f}",
                f"{cl_metrics['downtime_minutes']:.2f}",
                f"{cl_metrics['uptime_percentage']:.2f}"
            ]
        })
        
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        # Raw simulation data
        st.subheader("Raw Simulation Data")
        
        data_type = st.selectbox("Select Dataset", ["Ground Station Only", "Crosslinked"])
        
        if data_type == "Ground Station Only":
            st.dataframe(df_ground, use_container_width=True)
            st.download_button(
                "Download CSV",
                df_ground.to_csv(index=False),
                "ground_station_only.csv",
                "text/csv"
            )
        else:
            st.dataframe(df_crosslink, use_container_width=True)
            st.download_button(
                "Download CSV",
                df_crosslink.to_csv(index=False),
                "crosslinked.csv",
                "text/csv"
            )
    
    with tab5:
        st.header("Executive Summary Report")
        
        # Data source indicator
        if st.session_state.get('use_nasa_data', False):
            constellation = st.session_state.get('selected_constellation', 'Unknown')
            st.info(f"📡 **Executive Report for:** {constellation} constellation (NASA data)")
        else:
            num_sats = st.session_state.get('num_satellites', 6)
            st.info(f"🛰️ **Executive Report for:** Simulated constellation with {num_sats} satellites")
        st.markdown("Business Decision Support for Satellite Constellation Architecture")
        
        # Get data
        gs_metrics = st.session_state.metrics['ground_station_only']
        cl_metrics = st.session_state.metrics['crosslinked']
        cost_summary = st.session_state.cost_summary
        
        # Get simulation parameters
        num_satellites = st.session_state.get('num_satellites', 6)
        num_gs_ground_only = st.session_state.get('num_gs_ground_only', 5)
        num_gs_crosslinked = st.session_state.get('num_gs_crosslinked', 2)
        
        # Calculate key improvements using exact computed values
        latency_improvement = gs_metrics['average_latency_ms'] - cl_metrics['average_latency_ms']
        latency_improvement_pct = (latency_improvement / gs_metrics['average_latency_ms']) * 100
        coverage_improvement = cl_metrics['coverage_percentage'] - gs_metrics['coverage_percentage']
        
        # Get exact values for display
        gs_coverage = gs_metrics['coverage_percentage']
        cl_coverage = cl_metrics['coverage_percentage']
        gs_latency = gs_metrics['average_latency_ms']
        cl_latency = cl_metrics['average_latency_ms']
        gs_snr = gs_metrics['average_snr_dB']
        cl_snr = cl_metrics['average_snr_dB']
        gs_downtime = gs_metrics['downtime_minutes']
        cl_downtime = cl_metrics['downtime_minutes']
        
        # Executive Summary Section
        st.markdown("---")
        st.subheader("Executive Summary")
        
        # Nuanced recommendation logic
        # Ground-station-only better when: high initial cost sensitivity, short mission, regional coverage, low latency not critical
        # Crosslinked better when: need low latency, global coverage, long mission, can handle ISL complexity
        
        # Calculate tipping point first to use in recommendation
        tipping_point = calculate_tipping_point(num_gs_ground_only, num_gs_crosslinked)
        
        score_crosslink = 0
        score_ground = 0
        
        # Tipping point factor (MOST IMPORTANT for financial viability)
        if num_satellites >= tipping_point + 5:
            score_crosslink += 3  # Well above tipping point
        elif num_satellites >= tipping_point:
            score_crosslink += 2  # At or above tipping point
        elif num_satellites >= tipping_point - 5:
            score_crosslink += 0  # Near tipping point (neutral)
        else:
            score_ground += 2  # Below tipping point (ground-only likely better)
        
        # Cost factor (only if savings are real)
        if cost_summary['savings_percentage'] > 30 and num_satellites >= tipping_point:
            score_crosslink += 2
        elif cost_summary['savings_percentage'] > 10 and num_satellites >= tipping_point:
            score_crosslink += 1
        elif cost_summary['savings_percentage'] < 0:
            score_ground += 2  # Crosslinks cost MORE
        
        # Latency factor
        if latency_improvement_pct > 70:
            score_crosslink += 2
        elif latency_improvement_pct > 40:
            score_crosslink += 1
        elif latency_improvement_pct < 20:
            score_ground += 1
        
        # Coverage factor
        if coverage_improvement > 15:
            score_crosslink += 2
        elif coverage_improvement > 5:
            score_crosslink += 1
        elif coverage_improvement < 0:
            score_ground += 1
        
        # Infrastructure complexity (ground-only is simpler)
        if num_gs_ground_only <= 3:
            score_ground += 1  # Easy ground access favors traditional
        
        # Number of satellites (more satellites = more ISL benefit)
        if num_satellites >= 8:
            score_crosslink += 1
        elif num_satellites <= 4:
            score_ground += 1
        
        # Final recommendation
        if score_crosslink > score_ground + 2:
            recommendation = "RECOMMENDATION: Crosslinked Architecture"
            recommendation_class = "success"
            rationale = "Crosslinked architecture offers significant cost and performance advantages for your use case."
        elif score_ground > score_crosslink + 1:
            recommendation = "RECOMMENDATION: Ground-Station-Only Architecture"
            recommendation_class = "info"
            rationale = "Ground-station-only architecture better suits your requirements. Lower complexity and adequate performance."
        else:
            recommendation = "RECOMMENDATION: Further Analysis Required"
            recommendation_class = "warning"
            rationale = "Both architectures have trade-offs. Decision depends on mission priorities: cost versus latency."
        
        if recommendation_class == "success":
            st.success(f"**{recommendation}**")
        elif recommendation_class == "warning":
            st.warning(f"**{recommendation}**")
        else:
            st.info(f"**{recommendation}**")
        
        st.write(rationale)
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown("""
            #### Key Findings (Exact Values from Simulation):
            """)
            st.metric("Cost Savings", f"${cost_summary['total_savings_usd']/1e6:.1f}M", 
                     f"{cost_summary['savings_percentage']:.1f}%")
            st.metric("Latency Reduction", f"{latency_improvement:.0f} ms", 
                     f"-{latency_improvement_pct:.1f}%")
            st.metric("Coverage Improvement", f"+{coverage_improvement:.1f}%")
            st.metric("SNR Improvement", f"+{cl_snr - gs_snr:.1f} dB")
        
        with summary_col2:
            st.markdown("""
            #### Business Impact & Decision Factors:
            """)
            st.write(f"**CapEx Reduction:** ${cost_summary['total_savings_usd']/1e6:.1f}M")
            st.write(f"**Infrastructure:** {cost_summary['gs_reduction_count']} fewer ground stations")
            st.write(f"**Performance:** {latency_improvement_pct:.0f}% faster communications")
            st.write(f"**Reliability:** {coverage_improvement:.1f}% better uptime")
            st.write(f"**Tipping Point:** {tipping_point} satellites (you have {num_satellites})")
            if cost_summary['savings_percentage'] > 0:
                st.write(f"**ROI:** Crosslinks save money at this scale")
            else:
                st.write(f"**ROI:** Crosslinks cost more at this scale")
        
        # Detailed Analysis
        st.markdown("---")
        st.subheader("📊 Detailed Comparison")
        
        # Create comparison dataframe
        comparison_data = {
            'Metric': [
                'Total CapEx',
                'Ground Stations Required',
                'Infrastructure Cost',
                'Satellite Hardware Cost',
                'Average Latency',
                'Coverage Percentage',
                'Link Availability',
                'Average SNR',
                'System Downtime'
            ],
            'Ground-Station-Only': [
                f"${cost_summary['gs_only_capex']/1e6:.1f}M",
                f"{num_gs_ground_only}",
                f"${cost_summary['gs_only_breakdown']['Ground Stations']/1e6:.1f}M",
                f"${cost_summary['gs_only_breakdown']['Satellites']/1e6:.1f}M",
                f"{gs_latency:.0f} ms",
                f"{gs_coverage:.1f}%",
                f"{gs_coverage:.1f}%",
                f"{gs_snr:.1f} dB",
                f"{gs_downtime:.1f} min"
            ],
            'Crosslinked': [
                f"${cost_summary['crosslinked_capex']/1e6:.1f}M",
                f"{num_gs_crosslinked}",
                f"${cost_summary['crosslinked_breakdown']['Ground Stations']/1e6:.1f}M",
                f"${cost_summary['crosslinked_breakdown']['Satellites']/1e6:.1f}M + ${cost_summary['crosslinked_breakdown']['ISL Hardware']/1e6:.1f}M ISL",
                f"{cl_latency:.0f} ms",
                f"{cl_coverage:.1f}%",
                f"{cl_coverage:.1f}%",
                f"{cl_snr:.1f} dB",
                f"{cl_downtime:.1f} min"
            ],
            'Delta': [
                f"${cost_summary['total_savings_usd']/1e6:.1f}M ({cost_summary['savings_percentage']:.1f}%)",
                f"-{cost_summary['gs_reduction_count']} ({cost_summary['gs_reduction_percentage']:.0f}%)",
                f"-${(cost_summary['gs_only_breakdown']['Ground Stations'] - cost_summary['crosslinked_breakdown']['Ground Stations'])/1e6:.1f}M",
                f"+${cost_summary['crosslinked_breakdown']['ISL Hardware']/1e6:.1f}M",
                f"-{latency_improvement:.0f} ms (-{latency_improvement_pct:.0f}%)",
                f"+{coverage_improvement:.1f}%",
                f"+{cl_metrics['feasible_percentage'] - gs_metrics['feasible_percentage']:.1f}%",
                f"+{cl_metrics['average_snr_dB'] - gs_metrics['average_snr_dB']:.1f} dB",
                f"-{gs_metrics['downtime_minutes'] - cl_metrics['downtime_minutes']:.1f} min"
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Business Case
        st.markdown("---")
        st.subheader("💼 Business Case")
        
        case_col1, case_col2 = st.columns(2)
        
        with case_col1:
            st.markdown("#### ✅ Advantages of Crosslinked Architecture")
            st.markdown(f"""
            **Cost Savings:**
            - **{cost_summary['savings_percentage']:.1f}%** lower CapEx (${cost_summary['total_savings_usd']/1e6:.1f}M saved)
            - **{cost_summary['gs_reduction_percentage']:.0f}%** reduction in ground infrastructure
            - Lower operational costs (fewer facilities to maintain)
            
            **Performance Benefits:**
            - **{latency_improvement_pct:.0f}%** latency reduction ({latency_improvement:.0f} ms faster)
            - **{coverage_improvement:.1f}%** better coverage and availability
            - More resilient network architecture
            - Direct satellite-to-satellite paths
            
            **Strategic Advantages:**
            - Faster data delivery for time-sensitive applications
            - Better global coverage with less infrastructure
            - Scalable architecture (add satellites easily)
            - Reduced dependency on ground infrastructure
            - Competitive advantage in latency-sensitive markets
            """)
        
        with case_col2:
            st.markdown("#### ⚠️ Considerations")
            st.markdown(f"""
            **Crosslink Architecture Requires:**
            - **ISL hardware:** +${cost_summary['crosslinked_breakdown']['ISL Hardware']/1e6:.1f}M investment
            - Inter-satellite laser/radio links
            - More complex satellite design
            - Pointing and tracking systems
            - Routing algorithms
            
            **Trade-offs:**
            - Higher per-satellite cost
            - More complex operations
            - Technology dependency (ISL maturity)
            
            **Risk Mitigation:**
            - Proven technology (Starlink Gen2 uses it)
            - Net cost savings offset higher satellite cost
            - Performance gains justify complexity
            - Industry trend toward crosslinks
            """)
        
        # Market Analysis
        st.markdown("---")
        st.subheader("🌍 Market Context & Benchmarking")
        
        st.markdown("""
        #### Industry Trends:
        
        **Real-World Implementations:**
        
        | Constellation | Architecture | Satellites | Result |
        |---------------|--------------|------------|--------|
        | **Starlink Gen2** | ✅ Crosslinked (laser) | 6,000+ | Low latency internet, competitive with fiber |
        | **OneWeb** | ⚠️ Limited crosslinks | 600+ | Requires extensive ground network |
        | **Iridium NEXT** | ✅ Crosslinked | 66 | Global voice/data, minimal ground stations |
        | **Traditional GEO** | ❌ Ground-only | Few | High latency, many ground stations |
        
        **Key Insight:** The satellite industry is moving toward crosslinked architectures for LEO constellations.
        """)
        
        trend_col1, trend_col2, trend_col3 = st.columns(3)
        
        with trend_col1:
            st.metric("Industry Trend", "Crosslinks", delta="Growing", help="Major constellations adopting ISL technology")
        
        with trend_col2:
            st.metric("Starlink Latency", "20-40 ms", delta="Competitive with fiber", help="With laser crosslinks")
        
        with trend_col3:
            st.metric("Market Advantage", f"{latency_improvement_pct:.0f}%", delta="Latency improvement", help="Your crosslink advantage")
        
        # Decision Framework
        st.markdown("---")
        st.subheader("🎯 Decision Framework")
        
        st.markdown("""
        #### When to Choose Crosslinked Architecture:
        
        ✅ **Choose Crosslinked if:**
        - Need low latency (<100 ms)
        - Global coverage required
        - Budget allows upfront satellite investment
        - Long-term operation planned (5+ years)
        - Competitive latency is critical
        - Limited ground station access
        
        ⚠️ **Consider Ground-Only if:**
        - Very limited budget
        - Short-term deployment (<2 years)
        - Regional coverage only (easy ground station access)
        - Legacy system integration required
        - Conservative approach preferred
        - ISL technology risk concerns
        """)
        
        # ROI Calculation
        st.markdown("---")
        st.subheader("📈 Return on Investment Analysis")
        
        roi_col1, roi_col2, roi_col3 = st.columns(3)
        
        # Simple ROI calculation
        capex_savings = cost_summary['total_savings_usd']
        performance_value = latency_improvement * 50000 + coverage_improvement * 30000  # Simplified valuation
        total_value = capex_savings + performance_value
        
        with roi_col1:
            st.metric("CapEx Savings", f"${capex_savings/1e6:.1f}M", help="Direct cost reduction")
        
        with roi_col2:
            st.metric("Performance Value", f"${performance_value/1e6:.1f}M", 
                     help="Estimated value of latency + coverage improvements")
        
        with roi_col3:
            st.metric("Total Business Value", f"${total_value/1e6:.1f}M", 
                     help="Combined savings and performance gains")
        
        # Tipping Point and Payback Analysis
        st.markdown("---")
        st.subheader("Tipping Point Analysis")
        
        st.markdown(f"""
        **When do crosslinks become cost-effective?**
        
        Tipping Point Formula: N satellites × ISL cost = Ground stations saved × GS cost
        
        **Your Analysis:**
        - You have **{num_satellites} satellites**
        - Tipping point is **{tipping_point} satellites**
        - Ground stations saved: **{cost_summary['gs_reduction_count']}** (${cost_summary['gs_reduction_percentage']:.0f}% reduction)
        - ISL hardware cost: **${cost_summary['crosslinked_breakdown']['ISL Hardware']/1e6:.1f}M**
        """)
        
        # Use already-calculated tipping point from recommendation logic
        payback = calculate_payback_period(st.session_state.cost_comparison, years=10)
        
        tip_col1, tip_col2, tip_col3 = st.columns(3)
        
        with tip_col1:
            if num_satellites >= tipping_point:
                delta_str = f"+{num_satellites - tipping_point} above"
                status = "✅ Above tipping point"
            else:
                delta_str = f"-{tipping_point - num_satellites} below"
                status = "⚠️ Below tipping point"
            st.metric("Tipping Point", f"{tipping_point} satellites", 
                     delta=delta_str,
                     help=f"Crosslinks save money when you have {tipping_point}+ satellites")
            st.write(status)
        
        with tip_col2:
            if payback['payback_years'] == 0:
                payback_display = "Immediate"
            elif payback['payback_years'] == float('inf'):
                payback_display = "Never"
            else:
                payback_display = f"{payback['payback_years']:.1f} years"
            
            st.metric("Payback Period", payback_display,
                     help="Time to recover crosslink investment through OpEx savings")
        
        with tip_col3:
            total_savings_10y = payback['total_savings'] / 1e6
            st.metric("10-Year Total Savings", f"${total_savings_10y:.1f}M",
                     help="CapEx + OpEx savings over 10 years")
        
        # Explain the analysis
        st.markdown(f"""
        **Analysis for Your Configuration:**
        
        Your constellation: {num_satellites} satellites
        
        Cost breakdown:
        - ISL hardware cost: ${num_satellites * 500_000 / 1e6:.1f}M ({num_satellites} satellites × $500K)
        - Ground stations saved: {num_gs_ground_only - num_gs_crosslinked} stations
        - Ground station savings: ${(num_gs_ground_only - num_gs_crosslinked) * 5_000_000 / 1e6:.1f}M
        
        Result: Crosslinks {"ARE" if num_satellites >= tipping_point else "ARE NOT"} cost-effective at {num_satellites} satellites.
        
        Annual OpEx savings: ${payback['annual_opex_savings'] / 1e6:.2f}M per year
        (Fewer ground stations = lower operations cost)
        """)
        
        # What These Results Mean for Your Business
        st.markdown("---")
        st.subheader("What These Results Mean for Your Business")
        
        st.markdown(f"""
        **Your Simulation Results Summary:**
        
        | Metric | Ground-Station-Only | Crosslinked | Business Impact |
        |--------|-------------------|-------------|-----------------|
        | **Total Cost** | ${cost_summary['gs_only_capex']/1e6:.1f}M | ${cost_summary['crosslinked_capex']/1e6:.1f}M | ${cost_summary['savings_percentage']:.1f}% savings |
        | **Latency** | {gs_latency:.0f} ms | {cl_latency:.0f} ms | {latency_improvement_pct:.0f}% faster |
        | **Coverage** | {gs_coverage:.1f}% | {cl_coverage:.1f}% | {coverage_improvement:.1f}% better |
        | **Ground Stations** | {num_gs_ground_only} | {num_gs_crosslinked} | {cost_summary['gs_reduction_count']} fewer needed |
        | **Signal Quality** | {gs_snr:.1f} dB | {cl_snr:.1f} dB | {cl_snr - gs_snr:.1f} dB improvement |
        
        **What This Means for Decision Making:**
        
        **If you choose Ground-Station-Only:**
        - You save ${cost_summary['total_savings_usd']/1e6:.1f}M upfront (if crosslinks cost more)
        - You get {gs_coverage:.1f}% coverage with {gs_latency:.0f} ms latency
        - You need {num_gs_ground_only} ground stations
        - **Best for:** Regional coverage, limited budget, short missions
        
        **If you choose Crosslinked:**
        - You invest ${cost_summary['crosslinked_breakdown']['ISL Hardware']/1e6:.1f}M in ISL hardware
        - You get {cl_coverage:.1f}% coverage with {cl_latency:.0f} ms latency  
        - You only need {num_gs_crosslinked} ground stations
        - **Best for:** Global coverage, low latency needs, long missions
        
        **Financial Tipping Point Analysis:**
        - You have {num_satellites} satellites
        - Tipping point is {tipping_point} satellites
        - {"✅ You are ABOVE the tipping point - crosslinks save money" if num_satellites >= tipping_point else "⚠️ You are BELOW the tipping point - ground-only may be cheaper"}
        """)
        
        # Realistic Use Cases and Limitations
        st.markdown("---")
        st.subheader("Realistic Use Cases and Limitations")
        
        st.markdown("""
        **IMPORTANT: Understand what this tool shows and does NOT show**
        
        **This tool is useful for:**
        
        1. New constellation design from scratch
           - Compare architectures before building
           - Find optimal satellite count
           - Understand cost-performance trade-offs
        
        2. Small constellation optimization (4 to 12 satellites)
           - Regional coverage analysis
           - Budget-constrained projects
           - When ground station access is limited
        
        3. Mission duration analysis
           - Short missions (1 to 2 years): Ground-only might work
           - Long missions (5+ years): Crosslinks usually win on OpEx
        
        4. Educational purposes
           - Understand satellite communication trade-offs
           - Learn link budget calculations
           - Explore orbital mechanics effects
        
        **This tool does NOT account for:**
        
        1. Existing satellites already in orbit
           - You cannot add crosslinks to deployed satellites without physical replacement
           - Comparing NASA TLE data is academic unless you plan full replacement
        
        2. Satellite replacement costs
           - Replacing existing ground-only constellation with crosslinked version
           - Deorbiting and replacement timeline
        
        3. Technology maturity risk
           - ISL hardware reliability
           - Laser versus RF crosslink trade-offs
           - Pointing and tracking complexity
        
        4. Regulatory and spectrum issues
           - Frequency coordination
           - Orbital debris regulations
        
        5. Advanced orbital mechanics
           - This uses simplified circular orbits
           - Real constellations have complex phasing
        
        **When ground-station-only makes sense:**
        
        - Regional coverage only (not global)
        - Small constellation (below tipping point)
        - Short mission duration (under 2 years)
        - Excellent ground station access in target region
        - Lower technology risk tolerance
        - Fast deployment requirement
        - Cannot afford ISL development time
        
        **When crosslinks make sense:**
        
        - Global coverage needed
        - Large constellation (above tipping point)
        - Long mission duration (5+ years)
        - Low latency critical (under 100ms)
        - Limited ground station access
        - Technology risk acceptable
        - Time for ISL development (12 to 18 months)
        """)
        
        # Model Verification Notes
        st.markdown("---")
        st.subheader("Technical Model Verification")
        
        with st.expander("Physics and Financial Model Details"):
            st.markdown("""
            **Link Budget (Friis Equation):**
            
            Pr (dBW) = Pt (dBW) + Gt (dBi) + Gr (dBi) - Lp (dB) - Latm (dB) - Lsys (dB)
            
            Where:
            - Path Loss: Lp = 20 × log10(4π × d / λ)
            - Wavelength: λ = c / f
            - Verified against standard RF link budget calculators
            
            **SNR Calculation:**
            
            SNR (dB) = Pr (dBW) - 10 × log10(k × T × B)
            
            Where:
            - k = Boltzmann constant (1.380649×10⁻²³ J/K)
            - T = System temperature (290 K default)
            - B = Bandwidth (1 MHz default)
            - Threshold: 10 dB (standard for digital communications)
            
            **Latency Model:**
            
            Propagation delay = distance / speed of light
            
            Ground-station path:
            - Satellite to ground: ~3 to 5 ms (at 500 km altitude)
            - Ground processing: ~50 ms
            - Return path: ~3 to 5 ms
            - Total: ~500 to 1000 ms (includes routing delays)
            
            Crosslink path:
            - Satellite to satellite: ~3 to 10 ms (direct)
            - Minimal processing: ~5 ms
            - Total: ~30 to 50 ms
            
            **Cost Model:**
            
            Ground Station: $5M per station
            - Construction and equipment: $3M
            - Integration: $1M
            - Initial operations setup: $1M
            - Annual OpEx: $500K per year
            
            ISL Hardware: $500K per satellite
            - Laser terminal: $300K
            - Pointing/tracking: $150K
            - Processing: $50K
            
            Satellite Base: $2M per satellite
            - Bus and payload
            - Launch costs amortized
            
            **Tipping Point Calculation:**
            
            Crosslinks become cost-effective when:
            N × $500K < (GS_saved) × $5M
            
            For standard config (5 GS reduced to 2 GS):
            N × $500K < 3 × $5M
            N < 30 satellites
            
            Therefore: Crosslinks save money for ANY constellation under 30 satellites
            (assuming you save 3 ground stations)
            
            **Payback Period:**
            
            If crosslinks cost MORE upfront:
            Payback = Extra CapEx / Annual OpEx savings
            
            Annual OpEx savings = (GS_saved) × $500K/year
            
            **Model Limitations:**
            
            1. Simplified orbital mechanics (circular orbits only)
            2. Does not model constellation phasing
            3. Fixed cost assumptions (real costs vary by vendor)
            4. Does not include launch insurance
            5. No time value of money (NPV analysis)
            6. Does not model partial failures
            7. Assumes perfect ISL availability (real systems have outages)
            
            **Sources:**
            
            - Friis equation: Standard RF textbooks
            - Cost estimates: Industry averages (SpaceX, Boeing, Lockheed Martin public data)
            - Latency values: Measured Starlink performance data
            - SNR threshold: ITU-R standards for satellite communications
            """)
        
        # Recommendation and Action Items
        st.markdown("---")
        st.subheader("Recommendations and Next Steps")
        
        if score_crosslink > score_ground + 2:
            st.success(f"""
            **Crosslinked Architecture Recommended**
            
            Rationale:
            - Satellite count ({num_satellites}) is {"above" if num_satellites >= tipping_point else "approaching"} tipping point ({tipping_point} satellites)
            - Cost savings: {cost_summary['savings_percentage']:.0f}% (${cost_summary['total_savings_usd']/1e6:.1f}M)
            - Latency improvement: {latency_improvement_pct:.0f}%
            - Coverage improvement: {coverage_improvement:.1f}%
            - Technology proven in Starlink and Iridium deployments
            
            Next Steps:
            1. Evaluate ISL hardware vendors (laser versus RF)
            2. Secure funding for ISL hardware (${cost_summary['crosslinked_breakdown']['ISL Hardware']/1e6:.1f}M)
            3. Design crosslink routing algorithms
            4. Identify {num_gs_crosslinked} strategic ground station locations
            5. Plan 12 to 18 month development timeline
            """)
        elif score_ground > score_crosslink + 1:
            st.info(f"""
            **Ground-Station-Only Architecture Recommended**
            
            Rationale:
            - Satellite count ({num_satellites}) is below tipping point ({tipping_point} satellites)
            - Crosslinks not cost-effective at this scale
            - Lower complexity and faster deployment
            - Adequate performance for regional coverage
            - Proven technology with lower risk
            - Good ground station access in target regions
            - Lower per-satellite cost
            
            Next Steps:
            1. Identify {num_gs_ground_only} ground station locations
            2. Negotiate ground station agreements
            3. Plan for traditional bent-pipe architecture
            4. Design coverage patterns for ground passes
            5. Budget for annual ground station operations (${num_gs_ground_only * 500_000 / 1e3:.0f}K/year)
            6. Consider crosslinks if scaling beyond {tipping_point} satellites in future
            """)
        else:
            st.warning(f"""
            **Further Analysis Required**
            
            Your use case shows trade-offs between both approaches. 
            
            Key Factors:
            - You have {num_satellites} satellites (tipping point is {tipping_point})
            - Cost savings: {cost_summary['savings_percentage']:.0f}%
            - Latency improvement: {latency_improvement_pct:.0f}%
            - Coverage improvement: {coverage_improvement:.1f}%
            
            Consider:
            - Mission duration (short term favors ground-only, long term favors crosslinked)
            - Latency requirements (real-time needs crosslinked)
            - Budget constraints (initial versus operational costs)
            - Coverage requirements (global versus regional)
            - Technology risk tolerance
            
            Run multiple scenarios with different parameters to understand sensitivity.
            """)
        
        # Export Report
        st.markdown("---")
        st.subheader("Export Report")
        
        # Determine recommendation for report
        if score_crosslink > score_ground + 2:
            report_recommendation = "CROSSLINKED ARCHITECTURE"
        elif score_ground > score_crosslink + 1:
            report_recommendation = "GROUND-STATION-ONLY ARCHITECTURE"
        else:
            report_recommendation = "FURTHER ANALYSIS REQUIRED"
        
        # Generate report text
        report_text = f"""
LEO SATELLITE CONSTELLATION FEASIBILITY REPORT
============================================

Executive Summary
-----------------
Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
Constellation: {num_satellites} satellites at {orbit_altitude_km} km

RECOMMENDATION: {report_recommendation}

Key Findings
------------
Cost Savings: ${cost_summary['total_savings_usd']/1e6:.2f}M ({cost_summary['savings_percentage']:.1f}%)
Latency Improvement: {latency_improvement:.0f} ms ({latency_improvement_pct:.0f}%)
Coverage Improvement: {coverage_improvement:.1f}%

Financial Comparison
-------------------
Ground-Station-Only CapEx: ${cost_summary['gs_only_capex']/1e6:.2f}M
Crosslinked CapEx: ${cost_summary['crosslinked_capex']/1e6:.2f}M
Net Savings: ${cost_summary['total_savings_usd']/1e6:.2f}M

Infrastructure Requirements
--------------------------
Ground Stations (GS-Only): {num_gs_ground_only}
Ground Stations (Crosslinked): {num_gs_crosslinked}
Reduction: {cost_summary['gs_reduction_count']} stations ({cost_summary['gs_reduction_percentage']:.0f}%)

Performance Metrics
------------------
                        GS-Only    Crosslinked    Delta
Average Latency:        {gs_metrics['average_latency_ms']:.0f} ms      {cl_metrics['average_latency_ms']:.0f} ms        -{latency_improvement:.0f} ms
Coverage:               {gs_metrics['coverage_percentage']:.1f}%       {cl_metrics['coverage_percentage']:.1f}%         +{coverage_improvement:.1f}%
Average SNR:            {gs_metrics['average_snr_dB']:.1f} dB      {cl_metrics['average_snr_dB']:.1f} dB        +{cl_metrics['average_snr_dB'] - gs_metrics['average_snr_dB']:.1f} dB
Downtime:               {gs_metrics['downtime_minutes']:.1f} min    {cl_metrics['downtime_minutes']:.1f} min      -{gs_metrics['downtime_minutes'] - cl_metrics['downtime_minutes']:.1f} min

Technical Parameters
-------------------
Transmit Power: {transmit_power_dBW} dBW
Antenna Gain: {antenna_gain_dBi} dBi
Frequency: {frequency_GHz} GHz
Orbit Altitude: {orbit_altitude_km} km

Conclusion
----------
Based on the analysis, the crosslinked architecture offers significant advantages
in both cost ({cost_summary['savings_percentage']:.1f}% savings) and performance ({latency_improvement_pct:.0f}% latency reduction).
The investment in ISL hardware (${cost_summary['crosslinked_breakdown']['ISL Hardware']/1e6:.2f}M) is offset by reduced
ground infrastructure requirements, resulting in net savings of ${cost_summary['total_savings_usd']/1e6:.2f}M.

Generated by LEO Link Simulator
"""
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "Download Executive Report (TXT)",
                report_text,
                "executive_report.txt",
                "text/plain",
                use_container_width=True
            )
        
        with col2:
            # Create CSV summary
            summary_csv = comparison_df.to_csv(index=False)
            st.download_button(
                "Download Comparison Table (CSV)",
                summary_csv,
                "architecture_comparison.csv",
                "text/csv",
                use_container_width=True
            )
    
    with tab6:
        st.header("Sustainability and Debris Analysis")
        st.markdown("NASA ODPO guidelines integration. Space debris risk assessment and end-of-life planning.")
        
        # Calculate debris metrics
        collision_risk = calculate_collision_probability(orbit_altitude_km, num_satellites, years=10)
        deorbit_req = calculate_deorbit_requirements(orbit_altitude_km)
        debris_costs = calculate_debris_mitigation_costs(num_satellites, orbit_altitude_km, years=10)
        sustainability = calculate_sustainability_score(orbit_altitude_km, num_satellites, 
                                                       has_deorbit=True, years=10)
        nasa_recommendations = get_nasa_debris_recommendations(orbit_altitude_km, num_satellites)
        
        # Sustainability Score Card
        st.markdown("---")
        st.subheader("Sustainability Score")
        
        score_col1, score_col2, score_col3, score_col4 = st.columns(4)
        
        with score_col1:
            score_color = "normal" if sustainability['total_score'] >= 70 else "inverse"
            st.metric("Overall Score", f"{sustainability['total_score']}/100",
                     delta=sustainability['grade'], delta_color=score_color)
        
        with score_col2:
            st.metric("Collision Risk", sustainability['collision_risk_level'],
                     help=f"Probability: {collision_risk['probability']:.2%}")
        
        with score_col3:
            st.metric("FCC Compliance", "Yes" if sustainability['fcc_compliant'] else "No",
                     help="5-year post-mission disposal rule (FCC updated Sep 2022)")
        
        with score_col4:
            st.metric("Debris Mitigation Cost", f"${debris_costs['total_mitigation_cost']/1e6:.1f}M",
                     help="10-year total")
        
        # Collision Risk Analysis
        st.markdown("---")
        st.subheader("Collision Risk Analysis")
        
        risk_col1, risk_col2 = st.columns(2)
        
        with risk_col1:
            st.markdown(f"""
            **Collision Probability (10 years)**
            
            Risk Level: {collision_risk['risk_level']}
            Probability: {collision_risk['probability']:.2%}
            Expected encounters: {collision_risk['expected_encounters']:.2f}
            
            Annual collision probability: {collision_risk['annual_collision_prob']:.3%}
            
            Debris density at {orbit_altitude_km} km: {collision_risk['debris_density']:.6f} objects/km³
            """)
        
        with risk_col2:
            if collision_risk['risk_level'] == "Low":
                st.success("Low collision risk. Standard tracking sufficient.")
            elif collision_risk['risk_level'] == "Moderate":
                st.warning("Moderate risk. Implement collision avoidance procedures.")
            elif collision_risk['risk_level'] == "High":
                st.error("High risk. Active debris monitoring required.")
            else:
                st.error("Critical risk. Consider lower altitude or reduce satellite count.")
        
        # Deorbit Requirements
        st.markdown("---")
        st.subheader("End-of-Life and Deorbit Requirements")
        
        deorbit_col1, deorbit_col2 = st.columns(2)
        
        with deorbit_col1:
            st.markdown(f"""
            **Deorbit Analysis**
            
            Natural decay time: {deorbit_req['natural_decay_years']:.0f} years
            Active deorbit required: {'Yes' if deorbit_req['active_deorbit_required'] else 'No'}
            FCC compliant: {'Yes' if deorbit_req['fcc_compliant'] else 'No'}
            
            **If active deorbit needed:**
            Delta-v required: {deorbit_req['delta_v_required_ms']:.0f} m/s
            Propellant per satellite: {deorbit_req['propellant_mass_kg']:.1f} kg
            System mass per satellite: {deorbit_req['system_mass_kg']:.1f} kg
            Total mass penalty: {deorbit_req['total_mass_penalty_kg']:.1f} kg
            """)
        
        with deorbit_col2:
            if deorbit_req['fcc_compliant']:
                st.success("FCC 5-year disposal rule: Compliant")
            else:
                st.error("FCC 5-year disposal rule: Non-compliant. Add active deorbit capability.")
            
            if deorbit_req['active_deorbit_required']:
                st.info(f"""
                Active deorbit system required.
                
                Hardware cost: ${num_satellites * 100_000 / 1e6:.1f}M
                ({num_satellites} satellites × $100K)
                
                This adds mass to each satellite.
                Budget for propellant and thrusters.
                """)
        
        # Cost Breakdown
        st.markdown("---")
        st.subheader("Debris Mitigation Costs (10-year mission)")
        
        cost_col1, cost_col2, cost_col3 = st.columns(3)
        
        with cost_col1:
            st.metric("Collision Avoidance", 
                     f"${debris_costs['collision_avoidance_total']/1e6:.1f}M",
                     help="Tracking and maneuver costs")
        
        with cost_col2:
            st.metric("Insurance", 
                     f"${debris_costs['insurance_total']/1e6:.1f}M",
                     help="Risk-based insurance premiums")
        
        with cost_col3:
            st.metric("Deorbit Hardware", 
                     f"${debris_costs['deorbit_hardware_cost']/1e6:.1f}M",
                     help="Propulsion system if needed")
        
        st.markdown(f"""
        **Detailed Cost Breakdown:**
        
        Annual collision avoidance: ${debris_costs['collision_avoidance_annual']/1e3:.0f}K per year
        Annual insurance: ${debris_costs['insurance_annual']/1e6:.2f}M per year
        Annual tracking: ${debris_costs['tracking_annual']/1e3:.0f}K per year
        
        Cost per satellite (10 years): ${debris_costs['mitigation_cost_per_sat']/1e3:.0f}K
        Total mitigation cost: ${debris_costs['total_mitigation_cost']/1e6:.1f}M
        """)
        
        # NASA Recommendations
        st.markdown("---")
        st.subheader("NASA ODPO Recommendations")
        
        st.markdown(f"Priority Level: {nasa_recommendations['priority_level']}")
        
        st.markdown("**Recommended Actions:**")
        for rec in nasa_recommendations['recommendations']:
            st.write(f"- {rec}")
        
        # Sustainability Improvements
        st.markdown("---")
        st.subheader("Improving Sustainability Score")
        
        improvements = []
        
        if orbit_altitude_km > 600:
            improvements.append(f"Lower altitude to 500-600 km range (+{30-sustainability['altitude_score']} points)")
        
        if collision_risk['risk_level'] != "Low":
            improvements.append(f"Reduce satellite count or improve tracking (+{30-sustainability['risk_score']} points)")
        
        if not deorbit_req['active_deorbit_required'] and sustainability['deorbit_score'] < 25:
            improvements.append("Add active deorbit capability (+25 points)")
        
        if improvements:
            st.markdown("**To improve your score:**")
            for imp in improvements:
                st.write(f"- {imp}")
        else:
            st.success("Constellation has excellent sustainability profile.")
    
    with tab7:
        st.header("Regulatory Compliance")
        st.markdown("FCC, ITU, and international regulatory requirements.")
        
        # Get regulatory analysis
        countries = ["US"]  # Default, expandable
        licensing = get_licensing_requirements(num_satellites, frequency_GHz, countries)
        freq_status = get_frequency_coordination_status(frequency_GHz)
        timeline = calculate_compliance_timeline(num_satellites, frequency_GHz, countries)
        risk_assessment = get_regulatory_risk_assessment(num_satellites, orbit_altitude_km, frequency_GHz)
        cooperation = get_international_cooperation_opportunities()
        
        # Licensing Requirements Summary
        st.markdown("---")
        st.subheader("Licensing Requirements")
        
        lic_col1, lic_col2, lic_col3 = st.columns(3)
        
        with lic_col1:
            st.metric("Upfront Licensing Cost", f"${licensing['total_upfront_cost']/1e6:.2f}M")
        
        with lic_col2:
            st.metric("Annual Compliance Cost", f"${licensing['annual_cost']/1e3:.0f}K")
        
        with lic_col3:
            st.metric("Timeline to Approval", f"{timeline['total_months']} months")
        
        st.markdown("**Required Licenses and Filings:**")
        for req in licensing['requirements']:
            st.write(f"- {req}")
        
        # Cost Breakdown
        st.markdown("---")
        st.subheader("Licensing Cost Breakdown")
        
        cost_items = []
        for key, value in licensing['costs'].items():
            if key != 'annual_compliance':
                cost_items.append({'Item': key.replace('_', ' ').title(), 'Cost': f"${value/1e3:.0f}K"})
        
        if cost_items:
            cost_df = pd.DataFrame(cost_items)
            st.dataframe(cost_df, hide_index=True, use_container_width=True)
        
        # Frequency Coordination
        st.markdown("---")
        st.subheader("Frequency Coordination Status")
        
        freq_col1, freq_col2 = st.columns(2)
        
        with freq_col1:
            st.markdown(f"""
            **Frequency Band Analysis**
            
            Band: {freq_status['band']}
            Frequency: {frequency_GHz} GHz
            Congestion level: {freq_status['congestion']}
            Coordination difficulty: {freq_status['difficulty']}
            """)
        
        with freq_col2:
            if freq_status['difficulty'] == "Easy":
                st.success(f"{freq_status['notes']}")
            elif freq_status['difficulty'] == "Medium":
                st.warning(f"{freq_status['notes']}")
            else:
                st.error(f"{freq_status['notes']}")
        
        # Regulatory Timeline
        st.markdown("---")
        st.subheader("Regulatory Approval Timeline")
        
        st.markdown(f"""
        **Total timeline: {timeline['total_months']} months ({timeline['total_years']:.1f} years)**
        
        Critical path: {timeline['critical_path']}
        """)
        
        for milestone in timeline['milestones']:
            with st.expander(f"{milestone['phase']} ({milestone['duration_months']} months)"):
                st.markdown("**Activities:**")
                for activity in milestone['activities']:
                    st.write(f"- {activity}")
        
        # Risk Assessment
        st.markdown("---")
        st.subheader("Regulatory Risk Assessment")
        
        if risk_assessment['risk_level'] == "Low":
            st.success(f"Risk Level: {risk_assessment['risk_level']}")
        elif risk_assessment['risk_level'] == "Moderate":
            st.warning(f"Risk Level: {risk_assessment['risk_level']}")
        else:
            st.error(f"Risk Level: {risk_assessment['risk_level']}")
        
        st.markdown("**Identified Risks:**")
        for risk in risk_assessment['risks']:
            st.write(f"- {risk}")
        
        st.markdown("**Mitigation Strategies:**")
        for mitigation in risk_assessment['mitigation']:
            st.write(f"- {mitigation}")
        
        # International Cooperation
        st.markdown("---")
        st.subheader("International Cooperation Opportunities")
        
        coop_col1, coop_col2 = st.columns(2)
        
        with coop_col1:
            st.markdown("**Data Sharing:**")
            for item in cooperation['data_sharing']:
                st.write(f"- {item}")
            
            st.markdown("**Ground Infrastructure:**")
            for item in cooperation['ground_infrastructure']:
                st.write(f"- {item}")
        
        with coop_col2:
            st.markdown("**Regulatory Coordination:**")
            for item in cooperation['regulatory']:
                st.write(f"- {item}")
            
            st.markdown("**Research Partnerships:**")
            for item in cooperation['research']:
                st.write(f"- {item}")
    
    with tab8:
        st.header("Business Model")
        st.markdown("Revenue model for LEO constellation optimization service.")
        
        st.info("""
        **Your Value Proposition:**
        
        This tool demonstrates a constellation optimization service business model.
        The service helps satellite operators make data-driven architecture decisions.
        """)
        
        # Service Tiers
        st.markdown("---")
        st.subheader("Service Offerings")
        
        tiers = get_service_tiers()
        
        tier_col1, tier_col2, tier_col3 = st.columns(3)
        
        with tier_col1:
            st.markdown("### Basic Tier")
            st.markdown(f"**${tiers['Basic']['price_monthly']/1e3:.0f}K/month**")
            st.markdown(f"${tiers['Basic']['price_annual']/1e3:.0f}K/year (save 2 months)")
            
            st.markdown("**Features:**")
            for feature in tiers['Basic']['features']:
                st.write(f"- {feature}")
            
            st.caption(f"Target: {tiers['Basic']['target_customers']}")
        
        with tier_col2:
            st.markdown("### Professional Tier")
            st.markdown(f"**${tiers['Professional']['price_monthly']/1e3:.0f}K/month**")
            st.markdown(f"${tiers['Professional']['price_annual']/1e3:.0f}K/year (save 2 months)")
            
            st.markdown("**Features:**")
            for feature in tiers['Professional']['features']:
                st.write(f"- {feature}")
            
            st.caption(f"Target: {tiers['Professional']['target_customers']}")
        
        with tier_col3:
            st.markdown("### Enterprise Tier")
            st.markdown(f"**${tiers['Enterprise']['price_monthly']/1e3:.0f}K/month**")
            st.markdown(f"${tiers['Enterprise']['price_annual']/1e3:.0f}K/year (save 2 months)")
            
            st.markdown("**Features:**")
            for feature in tiers['Enterprise']['features']:
                st.write(f"- {feature}")
            
            st.caption(f"Target: {tiers['Enterprise']['target_customers']}")
        
        # Revenue Projections
        st.markdown("---")
        st.subheader("Revenue Projections (5-Year)")
        
        revenue = calculate_revenue_projections(5)
        
        rev_col1, rev_col2, rev_col3 = st.columns(3)
        
        with rev_col1:
            st.metric("Year 1 Revenue", f"${revenue['year_1_revenue']/1e6:.2f}M")
        
        with rev_col2:
            st.metric("Year 5 Revenue", f"${revenue['year_5_revenue']/1e6:.2f}M")
        
        with rev_col3:
            st.metric("5-Year CAGR", f"{revenue['cagr']:.1f}%")
        
        # Revenue breakdown table
        rev_data = []
        for proj in revenue['projections']:
            rev_data.append({
                'Year': proj['year'],
                'Customers': proj['total_customers'],
                'Subscription Revenue': f"${proj['basic_revenue'] + proj['pro_revenue'] + proj['enterprise_revenue']:.0f}",
                'Project Revenue': f"${proj['project_revenue']:.0f}",
                'Total Revenue': f"${proj['total_revenue']:.0f}"
            })
        
        rev_df = pd.DataFrame(rev_data)
        st.dataframe(rev_df, hide_index=True, use_container_width=True)
        
        # Profitability Analysis
        st.markdown("---")
        st.subheader("Profitability Analysis")
        
        profit = calculate_profitability(5)
        
        profit_col1, profit_col2, profit_col3 = st.columns(3)
        
        with profit_col1:
            st.metric("Break-Even Year", profit['break_even_year'])
        
        with profit_col2:
            st.metric("Year 5 Profit", f"${profit['year_5_profit']/1e6:.2f}M")
        
        with profit_col3:
            st.metric("Year 5 Margin", f"{profit['year_5_margin']:.1f}%")
        
        st.markdown(f"""
        **Investment Required:** ${profit['total_investment_needed']/1e6:.2f}M
        
        This covers initial development, team hiring, and operations until break-even.
        """)
        
        # Profitability table
        profit_data = []
        for p in profit['profitability']:
            profit_data.append({
                'Year': p['year'],
                'Revenue': f"${p['revenue']/1e6:.2f}M",
                'Costs': f"${p['costs']/1e6:.2f}M",
                'Profit': f"${p['profit']/1e6:.2f}M",
                'Margin': f"{p['profit_margin']:.1f}%",
                'Cumulative': f"${p['cumulative_profit']/1e6:.2f}M"
            })
        
        profit_df = pd.DataFrame(profit_data)
        st.dataframe(profit_df, hide_index=True, use_container_width=True)
        
        # Market Analysis
        st.markdown("---")
        st.subheader("Market Opportunity")
        
        market = get_market_analysis()
        
        market_col1, market_col2 = st.columns(2)
        
        with market_col1:
            st.markdown(f"""
            **Total Addressable Market (TAM)**
            
            Size: ${market['total_addressable_market']['size_usd']/1e9:.0f}B
            Growth: {market['total_addressable_market']['growth_rate_annual']*100:.0f}% annually
            
            {market['total_addressable_market']['description']}
            
            **Serviceable Addressable Market (SAM)**
            
            Size: ${market['serviceable_addressable_market']['size_usd']/1e9:.1f}B
            Growth: {market['serviceable_addressable_market']['growth_rate_annual']*100:.0f}% annually
            
            {market['serviceable_addressable_market']['description']}
            
            **Serviceable Obtainable Market (SOM)**
            
            Size: ${market['serviceable_obtainable_market']['size_usd']/1e6:.0f}M
            Market Share: {market['serviceable_obtainable_market']['market_share']*100:.1f}%
            
            {market['serviceable_obtainable_market']['description']}
            """)
        
        with market_col2:
            st.markdown("**Target Segments:**")
            for segment in market['target_segments']:
                st.write(f"- {segment}")
            
            st.markdown("**Market Drivers:**")
            for driver in market['market_drivers']:
                st.write(f"- {driver}")
        
        # Competitive Landscape
        st.markdown("---")
        st.subheader("Competitive Analysis")
        
        competition = get_competitive_landscape()
        
        st.markdown("**Direct Competitors:**")
        for comp in competition['direct_competitors']:
            with st.expander(comp['name']):
                st.write(f"**Strengths:** {comp['strengths']}")
                st.write(f"**Weaknesses:** {comp['weaknesses']}")
                st.write(f"**Pricing:** {comp['pricing']}")
        
        st.markdown("**Competitive Advantages:**")
        for advantage in competition['competitive_advantages']:
            st.write(f"- {advantage}")
        
        # Go-to-Market Strategy
        st.markdown("---")
        st.subheader("Go-to-Market Strategy")
        
        gtm = get_go_to_market_strategy()
        
        gtm_col1, gtm_col2 = st.columns(2)
        
        with gtm_col1:
            st.markdown("**Distribution Channels:**")
            for channel in gtm['channels']:
                st.write(f"- {channel}")
            
            st.markdown("**Customer Acquisition:**")
            for acq in gtm['customer_acquisition']:
                st.write(f"- {acq}")
        
        with gtm_col2:
            st.markdown("**Retention Strategy:**")
            for retention in gtm['retention_strategy']:
                st.write(f"- {retention}")
            
            st.markdown("**Expansion Opportunities:**")
            for expansion in gtm['expansion_opportunities']:
                st.write(f"- {expansion}")

else:
    # Welcome screen
    st.info("Configure parameters in the sidebar and click Run Simulation to begin.")
    
    st.markdown("""
    ### Two Ways to Run This Simulator
    
    **Option 1: Simulated Data (Default)**
    - Creates a fake constellation with your specified parameters
    - Uses 5 example ground stations (New York, London, Tokyo, Sydney, Moscow)
    - Fast and easy for testing your own designs
    - Perfect for exploring different configurations
    
    **Option 2: Real NASA Data**
    - Enable "Use Real NASA TLE Data" in the sidebar
    - Loads actual satellite positions from NASA/NORAD tracking
    - Analyze existing constellations: Starlink, GPS, OneWeb, Iridium, ISS
    - Compare your design against real deployments
    
    ---
    """)
    
    st.warning("""
    **Important Technical Disclaimer**
    
    This simulator uses simplified models for educational and early-stage feasibility studies.
    
    Key Assumptions and Limitations:
    - Atmospheric loss assumes CLEAR SKY only (no rain fade modeled)
    - Debris density uses order-of-magnitude estimates (not actual NASA ORDEM 3.1 data)
    - Orbital mechanics simplified to circular orbits
    - FCC compliance based on 5-year post-mission disposal rule (updated Sep 2022)
    - Cost estimates are industry averages and vary significantly by vendor
    - Ground stations: $5M for medium-capability commercial stations
    
    For mission-critical decisions, use professional tools (AGI STK, GMAT) and consult aerospace engineers.
    
    See Technical Audit Report and Comprehensive Features Guide for detailed model verification.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### What This Tool Does
        
        Compare two satellite constellation architectures:
        
        1. Ground-Station-Only: Satellites talk to ground stations only
        2. Crosslinked: Satellites talk to each other plus minimal ground stations
        
        ### Analysis Includes
        
        - Link Budget: Friis equation, SNR, link margin
        - Latency: Propagation delays for both architectures
        - Coverage: Uptime, availability, downtime
        - Cost: CapEx comparison for infrastructure
        - Visualizations: Interactive plots and charts
        
        ### Getting Started
        
        1. Choose simulated or real NASA data
        2. Adjust parameters (hover over info icons for help)
        3. Click Run Simulation
        4. Review results in the tabs above
        5. Download executive report for decision support
        """)
    
    with col2:
        st.markdown("""
        ### Quick Reference
        
        Key Terms:
        
        LEO
        Low Earth Orbit (400 to 800 km)
        
        TLE
        Two-Line Element (NASA orbital data format)
        
        ISL
        Inter-Satellite Link (laser or radio between satellites)
        
        dBW
        Decibels relative to 1 Watt (power)
        
        dBi
        Decibels relative to isotropic antenna (gain)
        
        SNR
        Signal-to-Noise Ratio (signal quality metric)
        
        Friis Equation
        Calculates received signal power
        
        CapEx
        Capital Expenditure (upfront costs)
        
        GHz
        Gigahertz (radio frequency, billions of cycles per second)
        """)
    
    # Educational expander
    with st.expander("Learn More: Key Concepts"):
        st.markdown("""
        ### Understanding the Sidebar Parameters
        
        #### **Transmit Power (dBW)**
        The logarithmic scale can be confusing! Here's the conversion:
        - **0 dBW** = 1 Watt
        - **10 dBW** = 10 Watts
        - **20 dBW** = 100 Watts ← Typical satellite
        - **30 dBW** = 1,000 Watts
        
        **Why logarithmic?** Because signals can vary by millions of times - easier to work with dB!
        
        #### **Antenna Gain (dBi)**
        Think of it like a flashlight:
        - **Low gain (0-10 dBi)**: Wide beam, spreads everywhere (like a lantern)
        - **Medium gain (10-20 dBi)**: Focused beam (like a flashlight)
        - **High gain (30+ dBi)**: Very narrow beam (like a laser pointer)
        
        Higher gain = stronger signal in one direction, but must point accurately!
        
        #### **Frequency Bands**
        Different frequencies behave differently:
        
        | Band | Frequency | Pros | Cons |
        |------|-----------|------|------|
        | **L-band** | 1-2 GHz | Works in rain | Large antennas |
        | **S-band** | 2-4 GHz | Good balance | Crowded |
        | **Ka-band** | 26-40 GHz | High speed | Rain fade |
        
        #### **Why Crosslinking Wins**
        
        **Ground-Station-Only:**
        - Satellite → Ground → Internet → Ground → Satellite
        - Must wait for ground station pass (5-10 min windows)
        - Need many ground stations ($5M each!)
        - High latency (~800-1000 ms)
        
        **Crosslinked:**
        - Satellite → Satellite → Satellite → Nearest ground station
        - Data always flows through constellation
        - Need only 2-3 ground stations
        - Low latency (~40-60 ms)
        - **Result: 40-60% cost savings + 93% latency reduction!**
        
        #### **The Friis Equation Explained**
        
        ```
        Received Power = Transmit Power + Gains - Losses
        ```
        
        **In detail:**
        - **Pt**: How much power you transmit
        - **Gt**: How well your transmit antenna focuses
        - **Gr**: How well the receive antenna focuses
        - **Lp**: Path loss (distance + frequency)
        - **Latm**: Atmospheric loss (~2 dB)
        - **Lsys**: System losses (~3 dB)
        
        **Path loss is BIG!** At 1000 km and 2.4 GHz: ~162 dB loss!
        That's why we need high gain antennas and good transmit power.
        
        #### **SNR (Signal-to-Noise Ratio)**
        
        How strong is your signal compared to background noise?
        
        - **SNR < 0 dB**: Noise stronger than signal ❌ No communication
        - **SNR = 10 dB**: Minimum for reliable link ✅
        - **SNR = 20 dB**: Good link quality ✅✅
        - **SNR > 30 dB**: Excellent link ✅✅✅
        
        **We use 10 dB as threshold** - industry standard for digital communications.
        
        #### **Latency Components**
        
        **Ground-station path:**
        1. Propagation delay: ~3 ms (satellite → ground, speed of light)
        2. Ground processing: ~50 ms (routing, switching)
        3. Return path: ~3 ms (ground → satellite)
        4. Multiple hops: ×2 or more
        5. **Total: ~800-1000 ms**
        
        **Crosslink path:**
        1. Satellite-to-satellite: ~3-10 ms (direct)
        2. Minimal processing: ~5 ms
        3. **Total: ~40-60 ms**
        
        That's why Starlink with crosslinks can compete with fiber optics!
        
        #### **NASA TLE Data**
        
        **What is TLE?**
        Two lines of text that describe a satellite's orbit:
        - Line 1: Satellite ID, epoch, orbital decay
        - Line 2: Inclination, RAAN, eccentricity, mean anomaly
        
        **Why use it?**
        - Real satellite positions updated daily
        - Analyze actual constellations
        - Compare your design to deployed systems
        
        **Where it comes from:**
        - NORAD tracks all satellites with radar
        - Data published through CelesTrak (free!)
        - Used worldwide for satellite tracking
        
        #### **Cost Model Breakdown**
        
        **Ground Station Costs ($5M each):**
        - Land and building: $1M
        - Antenna and RF equipment: $2M
        - Computing and networking: $1M
        - Operations (annual): $500K
        
        **ISL Hardware ($500K per satellite):**
        - Laser terminal: $300K
        - Pointing/tracking system: $150K
        - Processing: $50K
        
        **Why crosslinking saves money:**
        - Save 3 ground stations: -$15M
        - Add ISL to 6 satellites: +$3M
        - **Net savings: $12M (57% reduction!)**
        """)
    
    # Quick tips
    st.markdown("""
    ---
    ### Quick Tips
    
    - First time: Use default settings and click Run
    - Speed: Set Time Steps to 50
    - Accuracy: Set Time Steps to 200
    - NASA data: Start with ISS or GPS (fewer satellites)
    - Understanding parameters: Hover over info icons in sidebar
    - Export data: Download from Data Tables tab
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>LEO Link Simulator | Built with Streamlit and Python | Satellite Communications Analysis</p>
</div>
""", unsafe_allow_html=True)

