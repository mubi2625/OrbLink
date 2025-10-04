import streamlit as st
import pandas as pd
import numpy as np
from constellations import Satellite, GroundStation, create_default_constellation, create_default_ground_stations
from simulation import ConstellationSimulator, calculate_coverage_metrics
from cost_model import calculate_cost_comparison, generate_cost_summary, calculate_roi_metrics
from plots import (plot_snr_vs_time, plot_latency_vs_time, plot_availability, 
                   plot_cost_comparison, plot_cost_breakdown, plot_link_type_distribution,
                   plot_satellite_coverage_heatmap, plot_distance_distribution)

# Page configuration
st.set_page_config(
    page_title="LEO Link Simulator",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🛰️ LEO Satellite Link Feasibility Simulator")
st.markdown("""
Compare **Ground-Station-Only** vs **Crosslinked** constellation architectures.
Analyze link feasibility, SNR, latency, coverage, and cost savings.
""")

# Sidebar - Input Parameters
st.sidebar.header("⚙️ Constellation Parameters")

# Satellite parameters
st.sidebar.subheader("Satellite Configuration")
num_satellites = st.sidebar.slider("Number of Satellites", 4, 12, 6)
orbit_altitude_km = st.sidebar.slider("Orbit Altitude (km)", 400, 800, 500, 50)
transmit_power_dBW = st.sidebar.slider("Transmit Power (dBW)", 10, 30, 20)
antenna_gain_dBi = st.sidebar.slider("Antenna Gain (dBi)", 10, 30, 20)
frequency_GHz = st.sidebar.slider("Frequency (GHz)", 1.0, 30.0, 2.4, 0.1)

# Ground station parameters
st.sidebar.subheader("Ground Station Configuration")
num_gs_ground_only = st.sidebar.slider("Ground Stations (GS-Only)", 3, 10, 5)
num_gs_crosslinked = st.sidebar.slider("Ground Stations (Crosslinked)", 1, 5, 2)

# Simulation parameters
st.sidebar.subheader("Simulation Settings")
time_steps = st.sidebar.slider("Time Steps", 50, 200, 100, 10)
orbit_period_minutes = st.sidebar.slider("Orbit Period (minutes)", 80, 100, 90)

# Run simulation button
run_simulation = st.sidebar.button("🚀 Run Simulation", type="primary", use_container_width=True)

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
            # Create constellation
            satellites = create_default_constellation(
                num_satellites=num_satellites,
                altitude_km=orbit_altitude_km
            )
            
            # Update satellite parameters
            for sat in satellites:
                sat.transmit_power_dBW = transmit_power_dBW
                sat.antenna_gain_dBi = antenna_gain_dBi
                sat.frequency_GHz = frequency_GHz
            
            # Create ground stations
            ground_stations = create_default_ground_stations()
            
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
            
            st.success("✅ Simulation completed successfully!")
            
        except Exception as e:
            st.error(f"❌ Simulation failed: {str(e)}")
            st.exception(e)

# Display results if simulation is complete
if st.session_state.simulation_complete:
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Simulation Results", "💰 Cost Analysis", "📈 Value Dashboard", "📋 Data Tables"])
    
    with tab1:
        st.header("Simulation Results")
        
        # Get data
        df_ground = st.session_state.results['ground_station_only']
        df_crosslink = st.session_state.results['crosslinked']
        gs_metrics = st.session_state.metrics['ground_station_only']
        cl_metrics = st.session_state.metrics['crosslinked']
        
        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "GS-Only Coverage",
                f"{gs_metrics['coverage_percentage']:.1f}%",
                help="Percentage of time with feasible link"
            )
        
        with col2:
            st.metric(
                "Crosslinked Coverage",
                f"{cl_metrics['coverage_percentage']:.1f}%",
                delta=f"{cl_metrics['coverage_percentage'] - gs_metrics['coverage_percentage']:.1f}%",
                help="Percentage of time with feasible link"
            )
        
        with col3:
            st.metric(
                "GS-Only Avg Latency",
                f"{gs_metrics['average_latency_ms']:.1f} ms",
                help="Average communication latency"
            )
        
        with col4:
            st.metric(
                "Crosslinked Avg Latency",
                f"{cl_metrics['average_latency_ms']:.1f} ms",
                delta=f"{cl_metrics['average_latency_ms'] - gs_metrics['average_latency_ms']:.1f} ms",
                delta_color="inverse",
                help="Average communication latency"
            )
        
        st.divider()
        
        # Plots
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                plot_snr_vs_time(df_ground, df_crosslink),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                plot_latency_vs_time(df_ground, df_crosslink),
                use_container_width=True
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                plot_availability(df_ground, df_crosslink),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                plot_distance_distribution(df_ground, df_crosslink),
                use_container_width=True
            )
        
        # Additional visualizations
        st.subheader("Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                plot_link_type_distribution(df_crosslink),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                plot_satellite_coverage_heatmap(df_ground),
                use_container_width=True
            )
    
    with tab2:
        st.header("Cost Analysis")
        
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
                "📥 Download CSV",
                df_ground.to_csv(index=False),
                "ground_station_only.csv",
                "text/csv"
            )
        else:
            st.dataframe(df_crosslink, use_container_width=True)
            st.download_button(
                "📥 Download CSV",
                df_crosslink.to_csv(index=False),
                "crosslinked.csv",
                "text/csv"
            )

else:
    # Welcome screen
    st.info("👈 Configure simulation parameters in the sidebar and click **Run Simulation** to begin.")
    
    st.markdown("""
    ### About This Simulator
    
    This tool simulates and compares two LEO satellite constellation architectures:
    
    1. **Ground-Station-Only**: Satellites communicate exclusively through ground stations
    2. **Crosslinked**: Satellites communicate with each other (ISL) plus minimal ground stations
    
    ### Features
    
    - **Link Budget Analysis**: Friis equation, SNR, link margin calculations
    - **Latency Modeling**: Realistic propagation delays for both architectures
    - **Coverage Metrics**: Uptime, availability, and downtime tracking
    - **Cost Comparison**: CapEx analysis for ground stations vs crosslink hardware
    - **Interactive Visualizations**: Real-time plots and dashboards
    
    ### Technical Models
    
    - **Friis Equation**: Pr = Pt + Gt + Gr - Lp - Latm - Lsys
    - **SNR Threshold**: 10 dB for feasible link
    - **Orbital Mechanics**: Circular orbit propagation at selected altitude
    - **Latency**: Ground (~500-1000ms) vs Crosslink (~30-50ms)
    
    ### Getting Started
    
    1. Adjust satellite and ground station parameters
    2. Configure simulation settings
    3. Run the simulation
    4. Explore results in the tabs above
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>LEO Link Simulator | Built with Streamlit & Python | 🛰️ Satellite Communications Analysis</p>
</div>
""", unsafe_allow_html=True)

