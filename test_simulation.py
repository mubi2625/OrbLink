"""
Quick test script to verify the simulation works correctly.
Run this before launching the Streamlit app to ensure everything is functioning.
"""

import numpy as np
from constellations import create_default_constellation, create_default_ground_stations
from simulation import ConstellationSimulator, calculate_coverage_metrics
from cost_model import calculate_cost_comparison, generate_cost_summary
from link_budget import friis_received_power, calculate_snr, is_link_feasible

def test_basic_functionality():
    """Test basic functionality of all modules."""
    
    print("🧪 Testing LEO Link Simulator...")
    print("-" * 50)
    
    # Test 1: Create constellation
    print("\n✅ Test 1: Creating satellite constellation...")
    satellites = create_default_constellation(num_satellites=6, altitude_km=500)
    assert len(satellites) == 6, "Failed to create 6 satellites"
    print(f"   Created {len(satellites)} satellites at 500 km altitude")
    
    # Test 2: Create ground stations
    print("\n✅ Test 2: Creating ground stations...")
    ground_stations = create_default_ground_stations()
    assert len(ground_stations) == 5, "Failed to create 5 ground stations"
    print(f"   Created {len(ground_stations)} ground stations")
    
    # Test 3: Link budget calculations
    print("\n✅ Test 3: Testing link budget calculations...")
    test_distance = 1000000  # 1000 km
    received_power = friis_received_power(
        transmit_power_dBW=20.0,
        transmit_gain_dBi=20.0,
        receive_gain_dBi=30.0,
        distance_m=test_distance,
        frequency_Hz=2.4e9
    )
    snr_dB, _ = calculate_snr(received_power, 1e6, 290.0)
    feasible = is_link_feasible(snr_dB)
    print(f"   Distance: {test_distance/1000:.0f} km")
    print(f"   Received Power: {received_power:.2f} dBW")
    print(f"   SNR: {snr_dB:.2f} dB")
    print(f"   Link Feasible: {feasible}")
    
    # Test 4: Run mini simulation
    print("\n✅ Test 4: Running mini simulation...")
    simulator = ConstellationSimulator(satellites, ground_stations)
    results = simulator.run_comparison_simulation(time_steps=10, orbit_period_minutes=90)
    
    assert 'ground_station_only' in results, "Missing ground station only results"
    assert 'crosslinked' in results, "Missing crosslinked results"
    
    gs_df = results['ground_station_only']
    cl_df = results['crosslinked']
    
    print(f"   Ground Station Only: {len(gs_df)} records")
    print(f"   Crosslinked: {len(cl_df)} records")
    
    # Test 5: Calculate metrics
    print("\n✅ Test 5: Calculating coverage metrics...")
    gs_metrics = calculate_coverage_metrics(gs_df)
    cl_metrics = calculate_coverage_metrics(cl_df)
    
    print(f"   GS-Only Coverage: {gs_metrics['coverage_percentage']:.1f}%")
    print(f"   Crosslinked Coverage: {cl_metrics['coverage_percentage']:.1f}%")
    print(f"   GS-Only Avg Latency: {gs_metrics['average_latency_ms']:.1f} ms")
    print(f"   Crosslinked Avg Latency: {cl_metrics['average_latency_ms']:.1f} ms")
    
    # Test 6: Cost analysis
    print("\n✅ Test 6: Testing cost model...")
    cost_comparison = calculate_cost_comparison(
        num_satellites=6,
        num_gs_ground_only=5,
        num_gs_crosslinked=2
    )
    cost_summary = generate_cost_summary(cost_comparison)
    
    print(f"   GS-Only CapEx: ${cost_summary['gs_only_capex']/1e6:.1f}M")
    print(f"   Crosslinked CapEx: ${cost_summary['crosslinked_capex']/1e6:.1f}M")
    print(f"   Savings: ${cost_summary['total_savings_usd']/1e6:.1f}M ({cost_summary['savings_percentage']:.1f}%)")
    print(f"   Recommendation: {cost_summary['recommendation']}")
    
    # Summary
    print("\n" + "=" * 50)
    print("✨ All tests passed! System is ready to run.")
    print("=" * 50)
    print("\n🚀 Launch the app with: streamlit run main.py")
    print()

if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        print("\n⚠️  Please check the error above before running the Streamlit app.")

