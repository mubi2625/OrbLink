"""
Regulatory Compliance and Licensing Module

Covers FCC, ITU, national space agencies, and international frameworks.
"""

from typing import Dict, List

# Licensing costs (USD)
FCC_LICENSE_COST = 500_000  # US launch and operation license
ITU_COORDINATION_COST = 200_000  # Frequency coordination
NATIONAL_LICENSE_COST = 300_000  # Average for other countries
ANNUAL_COMPLIANCE_COST = 50_000  # Reporting and monitoring

def get_licensing_requirements(num_satellites: int,
                              frequency_ghz: float,
                              countries_served: List[str] = None) -> Dict[str, any]:
    """
    Determine licensing requirements based on constellation parameters.
    
    Args:
        num_satellites: Number of satellites
        frequency_ghz: Operating frequency
        countries_served: List of countries for service
        
    Returns:
        Licensing requirements and costs
    """
    if countries_served is None:
        countries_served = ["US"]
    
    requirements = []
    costs = {}
    timeline_months = 0
    
    # FCC Requirements (if US-based or serving US)
    if "US" in countries_served:
        requirements.append("FCC Space Station License")
        requirements.append("FCC Earth Station License")
        costs['fcc_license'] = FCC_LICENSE_COST
        timeline_months = max(timeline_months, 12)
        
        # Market access filing
        if num_satellites > 10:
            requirements.append("FCC Market Access Filing")
            costs['market_access'] = 100_000
    
    # ITU Frequency Coordination (international)
    if len(countries_served) > 1 or num_satellites > 5:
        requirements.append("ITU Frequency Coordination")
        costs['itu_coordination'] = ITU_COORDINATION_COST
        timeline_months = max(timeline_months, 18)
    
    # Spectrum allocation
    if frequency_ghz < 3:
        requirements.append("S-band spectrum allocation")
    elif frequency_ghz < 8:
        requirements.append("C-band spectrum allocation")
    elif frequency_ghz < 18:
        requirements.append("Ku-band spectrum allocation")
    else:
        requirements.append("Ka-band spectrum allocation")
    
    # National licenses for each country
    num_other_countries = len(countries_served) - (1 if "US" in countries_served else 0)
    if num_other_countries > 0:
        requirements.append(f"Landing rights in {num_other_countries} countries")
        costs['national_licenses'] = num_other_countries * NATIONAL_LICENSE_COST
    
    # Debris mitigation plan (required by most agencies)
    requirements.append("Orbital Debris Mitigation Plan")
    costs['debris_plan'] = 50_000
    
    # Annual compliance
    costs['annual_compliance'] = ANNUAL_COMPLIANCE_COST
    
    # Total upfront cost
    total_upfront = sum(v for k, v in costs.items() if k != 'annual_compliance')
    
    return {
        'requirements': requirements,
        'costs': costs,
        'total_upfront_cost': total_upfront,
        'annual_cost': costs['annual_compliance'],
        'timeline_months': timeline_months,
        'num_countries': len(countries_served)
    }

def get_frequency_coordination_status(frequency_ghz: float) -> Dict[str, str]:
    """
    Get frequency band coordination requirements.
    
    Args:
        frequency_ghz: Operating frequency
        
    Returns:
        Coordination requirements
    """
    if frequency_ghz < 2:
        band = "L-band"
        congestion = "High"
        difficulty = "Hard"
        notes = "Crowded band. GPS and mobile services. Long coordination."
    elif frequency_ghz < 4:
        band = "S-band"
        congestion = "Moderate"
        difficulty = "Medium"
        notes = "Weather and some satellite services. 6-12 month coordination."
    elif frequency_ghz < 8:
        band = "C-band"
        congestion = "Moderate"
        difficulty = "Medium"
        notes = "Traditional satellite band. 6-9 month coordination."
    elif frequency_ghz < 12:
        band = "X-band"
        congestion = "Low"
        difficulty = "Easy"
        notes = "Military and government. Requires special authorization."
    elif frequency_ghz < 18:
        band = "Ku-band"
        congestion = "High"
        difficulty = "Hard"
        notes = "Popular for satellite internet. 9-15 month coordination."
    else:
        band = "Ka-band"
        congestion = "Moderate"
        difficulty = "Medium"
        notes = "High-speed data. Rain attenuation concerns. 6-12 months."
    
    return {
        'band': band,
        'congestion': congestion,
        'difficulty': difficulty,
        'notes': notes
    }

def get_international_cooperation_opportunities() -> Dict[str, List[str]]:
    """
    Identify international cooperation frameworks and opportunities.
    
    Returns:
        Cooperation opportunities by category
    """
    return {
        'data_sharing': [
            "Space Data Association (collision avoidance)",
            "Inter-Agency Space Debris Coordination Committee (IADC)",
            "Committee on Space Research (COSPAR)",
            "International Telecommunication Union (ITU)"
        ],
        'ground_infrastructure': [
            "NASA Near Space Network (NSN)",
            "ESA ground station network",
            "Commercial ground station partnerships",
            "Shared tracking facilities"
        ],
        'regulatory': [
            "United Nations Committee on Peaceful Uses of Outer Space (COPUOS)",
            "International Organization for Standardization (ISO)",
            "Space safety coalitions",
            "National space agency partnerships"
        ],
        'research': [
            "International Space Station collaborations",
            "Joint technology development",
            "Academic partnerships",
            "Standards development organizations"
        ]
    }

def calculate_compliance_timeline(num_satellites: int,
                                 frequency_ghz: float,
                                 countries_served: List[str] = None) -> Dict[str, any]:
    """
    Estimate timeline for regulatory compliance.
    
    Args:
        num_satellites: Number of satellites
        frequency_ghz: Operating frequency
        countries_served: List of countries
        
    Returns:
        Timeline breakdown
    """
    if countries_served is None:
        countries_served = ["US"]
    
    milestones = []
    
    # Pre-filing preparation (3-6 months)
    milestones.append({
        'phase': 'Pre-filing preparation',
        'duration_months': 4,
        'activities': [
            'Technical documentation',
            'Frequency analysis',
            'Debris mitigation plan',
            'Business plan finalization'
        ]
    })
    
    # FCC filing and review (6-12 months)
    if "US" in countries_served:
        milestones.append({
            'phase': 'FCC license application',
            'duration_months': 9,
            'activities': [
                'Submit application',
                'Public comment period',
                'Technical review',
                'License grant'
            ]
        })
    
    # ITU coordination (12-18 months)
    if len(countries_served) > 1:
        milestones.append({
            'phase': 'ITU frequency coordination',
            'duration_months': 15,
            'activities': [
                'Advance publication',
                'Coordination with administrations',
                'Frequency assignment',
                'Recording in Master Register'
            ]
        })
    
    # National licenses (varies by country)
    num_other = len(countries_served) - (1 if "US" in countries_served else 0)
    if num_other > 0:
        milestones.append({
            'phase': 'National landing rights',
            'duration_months': 6 * num_other,
            'activities': [
                'Country-specific applications',
                'Local partner identification',
                'Technical compliance',
                'Service authorization'
            ]
        })
    
    # Insurance and bonding (2-3 months)
    milestones.append({
        'phase': 'Insurance and bonding',
        'duration_months': 3,
        'activities': [
            'Launch insurance',
            'Third-party liability',
            'FCC bond requirement',
            'Debris mitigation bond'
        ]
    })
    
    # Total timeline (critical path)
    total_months = max([m['duration_months'] for m in milestones])
    
    return {
        'milestones': milestones,
        'total_months': total_months,
        'total_years': total_months / 12,
        'critical_path': 'ITU coordination' if len(countries_served) > 1 else 'FCC licensing'
    }

def get_regulatory_risk_assessment(num_satellites: int,
                                  altitude_km: float,
                                  frequency_ghz: float) -> Dict[str, str]:
    """
    Assess regulatory approval risks.
    
    Args:
        num_satellites: Number of satellites
        altitude_km: Orbital altitude
        frequency_ghz: Operating frequency
        
    Returns:
        Risk assessment
    """
    risks = []
    risk_level = "Low"
    
    # Constellation size risks
    if num_satellites > 100:
        risks.append("Large constellation requires extensive coordination")
        risk_level = "High"
    elif num_satellites > 50:
        risks.append("Medium constellation requires careful planning")
        risk_level = "Moderate"
    
    # Altitude risks
    if altitude_km > 700:
        risks.append("High altitude increases debris concerns")
        if risk_level == "Low":
            risk_level = "Moderate"
    
    # Frequency risks
    freq_status = get_frequency_coordination_status(frequency_ghz)
    if freq_status['congestion'] == "High":
        risks.append(f"{freq_status['band']} is congested. Expect delays.")
        if risk_level == "Low":
            risk_level = "Moderate"
    
    # Standard risks
    risks.append("Regulatory landscape evolves. Monitor changes.")
    
    if not risks:
        risks.append("Standard regulatory process expected")
    
    return {
        'risk_level': risk_level,
        'risks': risks,
        'mitigation': [
            "Engage regulatory consultants early",
            "Start ITU coordination immediately",
            "Build relationships with agencies",
            "Monitor policy developments"
        ]
    }

