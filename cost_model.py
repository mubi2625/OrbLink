import numpy as np
import pandas as pd
from typing import Dict, Tuple

# Cost assumptions (in USD)
COST_PER_GROUND_STATION = 5_000_000  # $5M per ground station (construction, equipment, operations)
COST_PER_ISL_HARDWARE = 500_000      # $500K per satellite for ISL hardware
COST_PER_SATELLITE_BASE = 2_000_000  # $2M base cost per satellite

def calculate_ground_station_only_cost(num_ground_stations: int, 
                                      num_satellites: int) -> Dict[str, float]:
    """
    Calculate total CapEx for ground-station-only architecture.
    
    Args:
        num_ground_stations: Number of ground stations required
        num_satellites: Number of satellites in constellation
        
    Returns:
        Dictionary with cost breakdown
    """
    gs_cost = num_ground_stations * COST_PER_GROUND_STATION
    satellite_cost = num_satellites * COST_PER_SATELLITE_BASE
    total_cost = gs_cost + satellite_cost
    
    return {
        'ground_station_cost': gs_cost,
        'satellite_cost': satellite_cost,
        'isl_hardware_cost': 0,
        'total_capex': total_cost,
        'num_ground_stations': num_ground_stations,
        'num_satellites': num_satellites
    }

def calculate_crosslinked_cost(num_ground_stations_minimal: int,
                              num_satellites: int,
                              num_isl_per_satellite: int = 4) -> Dict[str, float]:
    """
    Calculate total CapEx for crosslinked architecture.
    
    Args:
        num_ground_stations_minimal: Minimal number of ground stations needed
        num_satellites: Number of satellites in constellation
        num_isl_per_satellite: Number of ISL transceivers per satellite
        
    Returns:
        Dictionary with cost breakdown
    """
    gs_cost = num_ground_stations_minimal * COST_PER_GROUND_STATION
    satellite_cost = num_satellites * COST_PER_SATELLITE_BASE
    isl_hardware_cost = num_satellites * COST_PER_ISL_HARDWARE
    total_cost = gs_cost + satellite_cost + isl_hardware_cost
    
    return {
        'ground_station_cost': gs_cost,
        'satellite_cost': satellite_cost,
        'isl_hardware_cost': isl_hardware_cost,
        'total_capex': total_cost,
        'num_ground_stations': num_ground_stations_minimal,
        'num_satellites': num_satellites
    }

def calculate_cost_comparison(num_satellites: int,
                             num_gs_ground_only: int = 5,
                             num_gs_crosslinked: int = 2) -> Dict[str, any]:
    """
    Compare costs between ground-station-only and crosslinked architectures.
    
    Args:
        num_satellites: Number of satellites in constellation
        num_gs_ground_only: Number of ground stations for ground-only architecture
        num_gs_crosslinked: Minimal ground stations for crosslinked architecture
        
    Returns:
        Dictionary with comparison metrics
    """
    # Calculate costs for both architectures
    gs_only_costs = calculate_ground_station_only_cost(num_gs_ground_only, num_satellites)
    crosslinked_costs = calculate_crosslinked_cost(num_gs_crosslinked, num_satellites)
    
    # Calculate savings
    cost_difference = gs_only_costs['total_capex'] - crosslinked_costs['total_capex']
    savings_percentage = (cost_difference / gs_only_costs['total_capex']) * 100
    
    # Ground station reduction
    gs_reduction = num_gs_ground_only - num_gs_crosslinked
    gs_reduction_percentage = (gs_reduction / num_gs_ground_only) * 100
    
    return {
        'ground_station_only': gs_only_costs,
        'crosslinked': crosslinked_costs,
        'cost_savings_usd': cost_difference,
        'savings_percentage': savings_percentage,
        'ground_station_reduction': gs_reduction,
        'gs_reduction_percentage': gs_reduction_percentage,
        'recommendation': 'Crosslinked' if cost_difference > 0 else 'Ground Station Only'
    }

def calculate_operational_costs(num_ground_stations: int,
                               years: int = 5,
                               annual_gs_opex: float = 500_000) -> float:
    """
    Calculate operational costs over mission lifetime.
    
    Args:
        num_ground_stations: Number of ground stations
        years: Mission lifetime in years
        annual_gs_opex: Annual operational cost per ground station
        
    Returns:
        Total operational cost
    """
    return num_ground_stations * annual_gs_opex * years

def generate_cost_summary(comparison: Dict[str, any]) -> Dict[str, any]:
    """
    Generate a summary of cost analysis for dashboard display.
    
    Args:
        comparison: Output from calculate_cost_comparison
        
    Returns:
        Summary dictionary for display
    """
    gs_only = comparison['ground_station_only']
    crosslinked = comparison['crosslinked']
    
    summary = {
        'total_savings_usd': comparison['cost_savings_usd'],
        'savings_percentage': comparison['savings_percentage'],
        'gs_only_capex': gs_only['total_capex'],
        'crosslinked_capex': crosslinked['total_capex'],
        'gs_reduction_count': comparison['ground_station_reduction'],
        'gs_reduction_percentage': comparison['gs_reduction_percentage'],
        'isl_hardware_cost': crosslinked['isl_hardware_cost'],
        'recommendation': comparison['recommendation'],
        'gs_only_breakdown': {
            'Ground Stations': gs_only['ground_station_cost'],
            'Satellites': gs_only['satellite_cost']
        },
        'crosslinked_breakdown': {
            'Ground Stations': crosslinked['ground_station_cost'],
            'Satellites': crosslinked['satellite_cost'],
            'ISL Hardware': crosslinked['isl_hardware_cost']
        }
    }
    
    return summary

def calculate_roi_metrics(cost_comparison: Dict[str, any],
                         latency_improvement_ms: float,
                         coverage_improvement_pct: float) -> Dict[str, float]:
    """
    Calculate Return on Investment metrics.
    
    Args:
        cost_comparison: Output from calculate_cost_comparison
        latency_improvement_ms: Latency reduction in milliseconds
        coverage_improvement_pct: Coverage improvement percentage
        
    Returns:
        ROI metrics dictionary
    """
    savings = cost_comparison['cost_savings_usd']
    
    # Simple ROI calculation
    # Assume latency improvement generates revenue (simplified model)
    latency_value = latency_improvement_ms * 100_000  # $100K per ms improvement
    coverage_value = coverage_improvement_pct * 50_000  # $50K per % improvement
    
    total_value = savings + latency_value + coverage_value
    
    crosslinked_investment = cost_comparison['crosslinked']['total_capex']
    roi_percentage = (total_value / crosslinked_investment) * 100
    
    return {
        'cost_savings_value': savings,
        'latency_improvement_value': latency_value,
        'coverage_improvement_value': coverage_value,
        'total_value': total_value,
        'roi_percentage': roi_percentage
    }

