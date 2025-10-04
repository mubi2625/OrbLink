"""
Space Debris Risk Analysis Module

Integrates NASA ODPO guidelines and calculates collision risk,
deorbit requirements, and end-of-life costs.
"""

import numpy as np
from typing import Dict, Tuple

# NASA and international guidelines
FCC_DEORBIT_YEARS = 5  # FCC 5-year rule (updated September 2022 from 25 years)
# Simplified debris density estimates (not actual NASA ORDEM 3.1 model)
# Real debris environment is complex and altitude-specific
DEBRIS_DENSITY_LOW = 0.00001  # Objects per km³ at 400-600 km (order of magnitude estimate)
DEBRIS_DENSITY_MED = 0.0001   # Objects per km³ at 600-800 km (order of magnitude estimate)
DEBRIS_DENSITY_HIGH = 0.001   # Objects per km³ at 800-1000 km (order of magnitude estimate)

# Costs
COLLISION_AVOIDANCE_COST_PER_SAT = 50_000  # Annual per satellite
DEORBIT_PROPULSION_COST = 100_000  # Per satellite hardware
INSURANCE_BASE_RATE = 0.02  # 2% of satellite value per year

def get_debris_density(altitude_km: float) -> float:
    """
    Get debris density at given altitude.
    Based on NASA ODPO debris environment models.
    
    Args:
        altitude_km: Orbital altitude in km
        
    Returns:
        Debris objects per cubic km
    """
    if altitude_km < 600:
        return DEBRIS_DENSITY_LOW
    elif altitude_km < 800:
        return DEBRIS_DENSITY_MED
    else:
        return DEBRIS_DENSITY_HIGH

def calculate_collision_probability(altitude_km: float,
                                   num_satellites: int,
                                   years: int = 5) -> Dict[str, float]:
    """
    Calculate collision probability over mission lifetime.
    
    Simplified model based on:
    - Orbital altitude (debris density)
    - Number of satellites (cross-sectional area)
    - Mission duration
    
    Args:
        altitude_km: Orbital altitude
        num_satellites: Number of satellites in constellation
        years: Mission lifetime in years
        
    Returns:
        Dictionary with collision risk metrics
    """
    # Debris density at altitude
    debris_density = get_debris_density(altitude_km)
    
    # Satellite cross-section (assume 10 m² average)
    cross_section_m2 = 10.0
    
    # Orbital velocity at altitude (simplified circular orbit)
    earth_radius = 6371  # km
    orbit_radius = earth_radius + altitude_km
    orbital_velocity = 7.8 * np.sqrt(earth_radius / orbit_radius)  # km/s
    
    # Volume swept per satellite per year
    # Simplified: cross_section × velocity × time
    volume_per_sat_per_year = cross_section_m2 * 1e-6 * orbital_velocity * 365.25 * 24 * 3600
    
    # Total volume for constellation
    total_volume = volume_per_sat_per_year * num_satellites * years
    
    # Expected number of encounters
    expected_encounters = total_volume * debris_density
    
    # Probability of at least one collision (Poisson distribution)
    prob_collision = 1 - np.exp(-expected_encounters)
    
    # Risk level
    if prob_collision < 0.01:
        risk_level = "Low"
    elif prob_collision < 0.05:
        risk_level = "Moderate"
    elif prob_collision < 0.15:
        risk_level = "High"
    else:
        risk_level = "Critical"
    
    return {
        'probability': prob_collision,
        'expected_encounters': expected_encounters,
        'risk_level': risk_level,
        'debris_density': debris_density,
        'annual_collision_prob': 1 - np.exp(-expected_encounters/years)
    }

def calculate_deorbit_requirements(altitude_km: float,
                                  satellite_mass_kg: float = 200) -> Dict[str, float]:
    """
    Calculate deorbit delta-v and propellant requirements.
    Based on altitude and FCC 5-year post-mission disposal rule.
    
    Args:
        altitude_km: Orbital altitude
        satellite_mass_kg: Satellite mass
        
    Returns:
        Deorbit requirements
    """
    # Natural decay time (exponential with altitude)
    # FCC requires disposal within 5 years post-mission (updated Sep 2022)
    # Below 400 km: decays naturally within 5 years
    # Above 400 km: typically needs active deorbit to meet 5-year rule
    
    if altitude_km < 400:
        natural_decay_years = 1
        active_deorbit_required = False  # Decays quickly enough
    elif altitude_km < 500:
        natural_decay_years = 5
        active_deorbit_required = False  # Borderline, may decay in time
    elif altitude_km < 600:
        natural_decay_years = 15
        active_deorbit_required = True  # Too slow for 5-year rule
    else:
        natural_decay_years = 100 + (altitude_km - 600) * 5
        active_deorbit_required = True  # Definitely needs active deorbit
    
    # Delta-v required for deorbit (simplified)
    # Need to lower perigee to ~200 km for atmospheric drag
    altitude_drop = altitude_km - 200
    delta_v_ms = 50 + altitude_drop * 0.5  # m/s (simplified)
    
    # Propellant mass (Tsiolkovsky equation)
    # Isp = 220s for hydrazine thrusters
    isp = 220
    g0 = 9.81
    mass_ratio = np.exp(delta_v_ms / (isp * g0))
    propellant_mass = satellite_mass_kg * (mass_ratio - 1)
    
    # Propulsion system mass (10% of propellant)
    system_mass = propellant_mass * 0.1
    
    # Total mass penalty
    total_mass_penalty = propellant_mass + system_mass
    
    return {
        'natural_decay_years': natural_decay_years,
        'active_deorbit_required': active_deorbit_required,
        'delta_v_required_ms': delta_v_ms,
        'propellant_mass_kg': propellant_mass,
        'system_mass_kg': system_mass,
        'total_mass_penalty_kg': total_mass_penalty,
        'fcc_compliant': natural_decay_years <= FCC_DEORBIT_YEARS or active_deorbit_required
    }

def calculate_debris_mitigation_costs(num_satellites: int,
                                     altitude_km: float,
                                     satellite_value: float = 2_000_000,
                                     years: int = 5) -> Dict[str, float]:
    """
    Calculate total costs for debris mitigation and compliance.
    
    Args:
        num_satellites: Number of satellites
        altitude_km: Orbital altitude
        satellite_value: Value per satellite for insurance
        years: Mission lifetime
        
    Returns:
        Cost breakdown for debris mitigation
    """
    # Collision avoidance (tracking and maneuvers)
    collision_avoidance_annual = num_satellites * COLLISION_AVOIDANCE_COST_PER_SAT
    collision_avoidance_total = collision_avoidance_annual * years
    
    # Deorbit hardware (if required)
    deorbit_req = calculate_deorbit_requirements(altitude_km)
    if deorbit_req['active_deorbit_required']:
        deorbit_hardware_cost = num_satellites * DEORBIT_PROPULSION_COST
    else:
        deorbit_hardware_cost = 0
    
    # Insurance (based on collision risk)
    collision_risk = calculate_collision_probability(altitude_km, num_satellites, years)
    risk_multiplier = 1.0 + collision_risk['probability']
    annual_insurance = num_satellites * satellite_value * INSURANCE_BASE_RATE * risk_multiplier
    total_insurance = annual_insurance * years
    
    # Tracking and monitoring subscription
    tracking_annual = 10_000 * np.sqrt(num_satellites)  # Economies of scale
    tracking_total = tracking_annual * years
    
    # Total costs
    total_mitigation_cost = (collision_avoidance_total + 
                            deorbit_hardware_cost + 
                            total_insurance + 
                            tracking_total)
    
    return {
        'collision_avoidance_annual': collision_avoidance_annual,
        'collision_avoidance_total': collision_avoidance_total,
        'deorbit_hardware_cost': deorbit_hardware_cost,
        'insurance_annual': annual_insurance,
        'insurance_total': total_insurance,
        'tracking_annual': tracking_annual,
        'tracking_total': tracking_total,
        'total_mitigation_cost': total_mitigation_cost,
        'mitigation_cost_per_sat': total_mitigation_cost / num_satellites
    }

def calculate_sustainability_score(altitude_km: float,
                                  num_satellites: int,
                                  has_deorbit: bool,
                                  years: int = 5) -> Dict[str, any]:
    """
    Calculate overall sustainability score for constellation.
    
    Score factors:
    - Altitude (lower is better for natural decay)
    - Collision risk
    - Deorbit capability
    - FCC compliance
    
    Args:
        altitude_km: Orbital altitude
        num_satellites: Number of satellites
        has_deorbit: Whether satellites have active deorbit
        years: Mission lifetime
        
    Returns:
        Sustainability metrics and score
    """
    # Altitude score (0-30 points)
    if altitude_km < 500:
        altitude_score = 30
    elif altitude_km < 600:
        altitude_score = 25
    elif altitude_km < 700:
        altitude_score = 15
    else:
        altitude_score = 5
    
    # Collision risk score (0-30 points)
    collision_risk = calculate_collision_probability(altitude_km, num_satellites, years)
    if collision_risk['risk_level'] == "Low":
        risk_score = 30
    elif collision_risk['risk_level'] == "Moderate":
        risk_score = 20
    elif collision_risk['risk_level'] == "High":
        risk_score = 10
    else:
        risk_score = 0
    
    # Deorbit capability score (0-25 points)
    deorbit_req = calculate_deorbit_requirements(altitude_km)
    if has_deorbit or not deorbit_req['active_deorbit_required']:
        deorbit_score = 25
    else:
        deorbit_score = 0
    
    # FCC compliance score (0-15 points)
    if deorbit_req['fcc_compliant']:
        compliance_score = 15
    else:
        compliance_score = 0
    
    # Total score (0-100)
    total_score = altitude_score + risk_score + deorbit_score + compliance_score
    
    # Grade
    if total_score >= 85:
        grade = "Excellent"
    elif total_score >= 70:
        grade = "Good"
    elif total_score >= 55:
        grade = "Acceptable"
    else:
        grade = "Poor"
    
    return {
        'total_score': total_score,
        'grade': grade,
        'altitude_score': altitude_score,
        'risk_score': risk_score,
        'deorbit_score': deorbit_score,
        'compliance_score': compliance_score,
        'collision_risk_level': collision_risk['risk_level'],
        'fcc_compliant': deorbit_req['fcc_compliant']
    }

def get_nasa_debris_recommendations(altitude_km: float,
                                   num_satellites: int) -> Dict[str, str]:
    """
    Get NASA ODPO recommended practices.
    
    Args:
        altitude_km: Orbital altitude
        num_satellites: Number of satellites
        
    Returns:
        Recommendations dictionary
    """
    recommendations = []
    
    # Altitude-based recommendations
    if altitude_km > 600:
        recommendations.append("Install active deorbit propulsion (FCC 5-year disposal rule)")
        recommendations.append("Budget for end-of-life maneuvers")
    
    if altitude_km > 700:
        recommendations.append("Consider lower altitude for natural decay")
        recommendations.append("Increase debris tracking frequency")
    
    # Constellation size recommendations
    if num_satellites > 50:
        recommendations.append("Implement automated collision avoidance")
        recommendations.append("Establish dedicated operations center")
    
    if num_satellites > 100:
        recommendations.append("Coordinate with NASA and ESA debris offices")
        recommendations.append("Participate in Space Data Association")
    
    # Universal recommendations
    recommendations.append("Design for demise (break up on reentry)")
    recommendations.append("Avoid explosive passivation")
    recommendations.append("Track all objects >10cm")
    recommendations.append("Share tracking data internationally")
    
    return {
        'recommendations': recommendations,
        'priority_level': 'High' if altitude_km > 600 or num_satellites > 50 else 'Medium'
    }

