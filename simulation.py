import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from constellations import Satellite, GroundStation, create_default_constellation, create_default_ground_stations
from link_budget import friis_received_power, calculate_snr, is_link_feasible, calculate_latency

class ConstellationSimulator:
    """Simulates LEO satellite constellation communication."""
    
    def __init__(self, satellites: List[Satellite], ground_stations: List[GroundStation]):
        self.satellites = satellites
        self.ground_stations = ground_stations
        self.results = []
        
    def simulate_ground_station_only(self, 
                                   time_steps: int = 100,
                                   orbit_period_minutes: float = 90.0) -> pd.DataFrame:
        """Simulate ground-station-only constellation."""
        results = []
        dt = (orbit_period_minutes * 60) / time_steps  # Time step in seconds
        
        for step in range(time_steps):
            current_time = step * dt
            
            for i, sat in enumerate(self.satellites):
                # Update satellite position
                sat.update_position(dt)
                
                # Find best ground station link
                best_gs = None
                best_snr = -np.inf
                best_distance = np.inf
                
                for gs in self.ground_stations:
                    if gs.is_visible(sat):
                        distance = sat.compute_distance(gs)
                        
                        # Calculate link budget
                        received_power = friis_received_power(
                            sat.transmit_power_dBW,
                            sat.antenna_gain_dBi,
                            gs.antenna_gain_dBi,
                            distance,
                            sat.frequency_GHz * 1e9
                        )
                        
                        snr_dB, _ = calculate_snr(received_power, 1e6, gs.system_temperature_K)
                        
                        if snr_dB > best_snr:
                            best_snr = snr_dB
                            best_distance = distance
                            best_gs = gs
                
                # Record results
                is_feasible = is_link_feasible(best_snr) if best_gs else False
                latency = calculate_latency(best_distance, is_crosslink=False) if best_gs else np.nan
                
                results.append({
                    'time_step': step,
                    'time_minutes': current_time / 60,
                    'satellite_id': sat.satellite_id,
                    'constellation_type': 'ground_station_only',
                    'link_type': 'satellite_to_ground',
                    'ground_station_id': best_gs.station_id if best_gs else None,
                    'distance_m': best_distance if best_gs else np.nan,
                    'snr_dB': best_snr if best_gs else -np.inf,
                    'is_feasible': is_feasible,
                    'latency_ms': latency,
                    'coverage': 1.0 if is_feasible else 0.0
                })
        
        return pd.DataFrame(results)
    
    def simulate_crosslinked(self, 
                           time_steps: int = 100,
                           orbit_period_minutes: float = 90.0) -> pd.DataFrame:
        """Simulate crosslinked constellation."""
        results = []
        dt = (orbit_period_minutes * 60) / time_steps
        
        for step in range(time_steps):
            current_time = step * dt
            
            # Update all satellite positions
            for sat in self.satellites:
                sat.update_position(dt)
            
            # Check satellite-to-satellite links
            for i, sat1 in enumerate(self.satellites):
                for j, sat2 in enumerate(self.satellites[i+1:], i+1):
                    if sat1.is_visible(sat2):
                        distance = sat1.compute_distance(sat2)
                        
                        # Calculate link budget
                        received_power = friis_received_power(
                            sat1.transmit_power_dBW,
                            sat1.antenna_gain_dBi,
                            sat2.antenna_gain_dBi,
                            distance,
                            sat1.frequency_GHz * 1e9
                        )
                        
                        snr_dB, _ = calculate_snr(received_power, 1e6, 290.0)
                        is_feasible = is_link_feasible(snr_dB)
                        latency = calculate_latency(distance, is_crosslink=True)
                        
                        results.append({
                            'time_step': step,
                            'time_minutes': current_time / 60,
                            'satellite_id': sat1.satellite_id,
                            'constellation_type': 'crosslinked',
                            'link_type': 'satellite_to_satellite',
                            'ground_station_id': None,
                            'distance_m': distance,
                            'snr_dB': snr_dB,
                            'is_feasible': is_feasible,
                            'latency_ms': latency,
                            'coverage': 1.0 if is_feasible else 0.0
                        })
            
            # Check satellite-to-ground station links (minimal ground stations)
            for sat in self.satellites:
                for gs in self.ground_stations[:2]:  # Only use 2 ground stations for crosslinked
                    if gs.is_visible(sat):
                        distance = sat.compute_distance(gs)
                        
                        received_power = friis_received_power(
                            sat.transmit_power_dBW,
                            sat.antenna_gain_dBi,
                            gs.antenna_gain_dBi,
                            distance,
                            sat.frequency_GHz * 1e9
                        )
                        
                        snr_dB, _ = calculate_snr(received_power, 1e6, gs.system_temperature_K)
                        is_feasible = is_link_feasible(snr_dB)
                        latency = calculate_latency(distance, is_crosslink=False)
                        
                        results.append({
                            'time_step': step,
                            'time_minutes': current_time / 60,
                            'satellite_id': sat.satellite_id,
                            'constellation_type': 'crosslinked',
                            'link_type': 'satellite_to_ground',
                            'ground_station_id': gs.station_id,
                            'distance_m': distance,
                            'snr_dB': snr_dB,
                            'is_feasible': is_feasible,
                            'latency_ms': latency,
                            'coverage': 1.0 if is_feasible else 0.0
                        })
        
        return pd.DataFrame(results)
    
    def run_comparison_simulation(self, 
                                time_steps: int = 100,
                                orbit_period_minutes: float = 90.0) -> Dict[str, pd.DataFrame]:
        """Run both simulation types and return comparison results."""
        
        # Ground station only simulation
        gs_results = self.simulate_ground_station_only(time_steps, orbit_period_minutes)
        
        # Crosslinked simulation
        crosslink_results = self.simulate_crosslinked(time_steps, orbit_period_minutes)
        
        return {
            'ground_station_only': gs_results,
            'crosslinked': crosslink_results
        }

def calculate_coverage_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate coverage and availability metrics."""
    
    # Overall coverage percentage
    total_coverage = df['coverage'].mean() * 100
    
    # Feasible links percentage
    feasible_percentage = df['is_feasible'].mean() * 100
    
    # Average latency
    avg_latency = df['latency_ms'].mean()
    
    # Average SNR
    avg_snr = df['snr_dB'].mean()
    
    # Downtime calculation
    total_time = df['time_minutes'].max() - df['time_minutes'].min()
    downtime = total_time * (1 - df['coverage'].mean())
    
    return {
        'coverage_percentage': total_coverage,
        'feasible_percentage': feasible_percentage,
        'average_latency_ms': avg_latency,
        'average_snr_dB': avg_snr,
        'downtime_minutes': downtime,
        'uptime_percentage': 100 - (downtime / total_time * 100)
    }

def run_demo_simulation() -> Dict[str, pd.DataFrame]:
    """Run a demonstration simulation with default parameters."""
    
    # Create default constellation
    satellites = create_default_constellation(num_satellites=6, altitude_km=500)
    ground_stations = create_default_ground_stations()
    
    # Create simulator
    simulator = ConstellationSimulator(satellites, ground_stations)
    
    # Run simulation
    results = simulator.run_comparison_simulation(time_steps=50, orbit_period_minutes=90)
    
    return results
