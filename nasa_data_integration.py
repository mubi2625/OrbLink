"""
NASA Data Integration Module

This module demonstrates how to integrate real NASA TLE (Two-Line Element) data
and other NASA sources into the LEO Link Simulator.

Data Sources:
1. TLE Data: https://celestrak.org or https://www.space-track.org
2. Ground Stations: NASA SCaN (Space Communications and Navigation)
3. Atmospheric Models: NASA atmospheric databases (simplified)
"""

import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from constellations import Satellite, GroundStation

# ============================================================================
# TLE DATA INTEGRATION
# ============================================================================

def parse_tle_file(filepath: str) -> List[Dict[str, str]]:
    """
    Parse a TLE (Two-Line Element) file.
    
    TLE Format Example:
    ISS (ZARYA)
    1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
    2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
    
    Args:
        filepath: Path to TLE file (e.g., 'data/tle/starlink.txt')
        
    Returns:
        List of dictionaries containing parsed TLE data
    """
    satellites = []
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Parse TLE in groups of 3 lines (name, line1, line2)
        for i in range(0, len(lines), 3):
            if i + 2 >= len(lines):
                break
                
            name = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()
            
            # Basic validation
            if line1.startswith('1 ') and line2.startswith('2 '):
                satellites.append({
                    'name': name,
                    'line1': line1,
                    'line2': line2
                })
    
    except FileNotFoundError:
        print(f"Warning: TLE file not found at {filepath}")
        return []
    
    return satellites

def tle_to_satellite_objects(tle_data: List[Dict[str, str]], 
                             transmit_power_dBW: float = 20.0,
                             antenna_gain_dBi: float = 20.0,
                             frequency_GHz: float = 2.4) -> List[Satellite]:
    """
    Convert parsed TLE data to Satellite objects using Skyfield.
    
    Args:
        tle_data: List of parsed TLE dictionaries
        transmit_power_dBW: Transmit power for all satellites
        antenna_gain_dBi: Antenna gain for all satellites
        frequency_GHz: Operating frequency
        
    Returns:
        List of Satellite objects with positions from TLE
    """
    from skyfield.api import load, EarthSatellite
    
    satellites = []
    ts = load.timescale()
    t = ts.now()  # Current time
    
    for i, tle in enumerate(tle_data):
        try:
            # Create Skyfield satellite object
            sat = EarthSatellite(tle['line1'], tle['line2'], tle['name'], ts)
            
            # Get position at current time
            geocentric = sat.at(t)
            position_m = geocentric.position.m  # Position in meters (ECI)
            velocity_m_s = geocentric.velocity.m_per_s  # Velocity in m/s
            
            # Extract orbital altitude (approximate)
            altitude_km = (np.linalg.norm(position_m) - 6371000) / 1000
            
            # Create Satellite object
            satellite = Satellite(
                satellite_id=f"{tle['name'][:10]}_{i:02d}",
                position=position_m,
                velocity=velocity_m_s,
                transmit_power_dBW=transmit_power_dBW,
                antenna_gain_dBi=antenna_gain_dBi,
                frequency_GHz=frequency_GHz,
                orbit_altitude_km=altitude_km
            )
            
            satellites.append(satellite)
            
        except Exception as e:
            print(f"Warning: Could not process TLE for {tle['name']}: {e}")
            continue
    
    return satellites

# ============================================================================
# NASA GROUND STATION DATA
# ============================================================================

# NASA Deep Space Network (DSN) Stations
NASA_DSN_STATIONS = [
    {
        'name': 'Goldstone (DSS-14)',
        'location': 'California, USA',
        'latitude': 35.4267,
        'longitude': -116.8900,
        'altitude': 1001,
        'antenna_gain': 74.0  # Large dish, very high gain
    },
    {
        'name': 'Canberra (DSS-43)',
        'location': 'Australia',
        'latitude': -35.4021,
        'longitude': 148.9817,
        'altitude': 692,
        'antenna_gain': 74.0
    },
    {
        'name': 'Madrid (DSS-63)',
        'location': 'Spain',
        'latitude': 40.4280,
        'longitude': -4.2508,
        'altitude': 834,
        'antenna_gain': 74.0
    }
]

# NASA Near Earth Network (NEN) / SCaN Stations
NASA_NEN_STATIONS = [
    {
        'name': 'White Sands (WSC)',
        'location': 'New Mexico, USA',
        'latitude': 32.5449,
        'longitude': -106.6130,
        'altitude': 1474,
        'antenna_gain': 45.0
    },
    {
        'name': 'Alaska (AGS)',
        'location': 'Alaska, USA',
        'latitude': 64.8592,
        'longitude': -147.8560,
        'altitude': 303,
        'antenna_gain': 40.0
    },
    {
        'name': 'Svalbard (SGS)',
        'location': 'Norway',
        'latitude': 78.2300,
        'longitude': 15.4070,
        'altitude': 458,
        'antenna_gain': 40.0
    }
]

def create_nasa_ground_stations(network: str = 'NEN') -> List[GroundStation]:
    """
    Create GroundStation objects from NASA station data.
    
    Args:
        network: 'DSN' for Deep Space Network or 'NEN' for Near Earth Network
        
    Returns:
        List of GroundStation objects
    """
    if network.upper() == 'DSN':
        station_data = NASA_DSN_STATIONS
    elif network.upper() == 'NEN':
        station_data = NASA_NEN_STATIONS
    else:
        # Use both networks
        station_data = NASA_DSN_STATIONS + NASA_NEN_STATIONS
    
    ground_stations = []
    
    for i, station in enumerate(station_data):
        gs = GroundStation(
            station_id=f"NASA_{network}_{i:02d}",
            latitude_deg=station['latitude'],
            longitude_deg=station['longitude'],
            altitude_m=station['altitude'],
            antenna_gain_dBi=station['antenna_gain'],
            system_temperature_K=290.0
        )
        ground_stations.append(gs)
    
    return ground_stations

# ============================================================================
# ATMOSPHERIC LOSS MODELS (NASA DATA)
# ============================================================================

def calculate_atmospheric_loss_nasa(frequency_GHz: float, 
                                   elevation_angle_deg: float,
                                   weather: str = 'clear') -> float:
    """
    Calculate atmospheric loss based on NASA atmospheric models (simplified).
    
    Real NASA models: ITU-R P.676 (gaseous attenuation)
                     ITU-R P.618 (rain attenuation)
    
    Args:
        frequency_GHz: Operating frequency in GHz
        elevation_angle_deg: Elevation angle in degrees
        weather: 'clear', 'rain', or 'heavy_rain'
        
    Returns:
        Atmospheric loss in dB
    """
    # Zenith attenuation (simplified model)
    # Real NASA data would use measured atmospheric profiles
    
    if frequency_GHz < 10:
        zenith_loss = 0.5  # Low loss at low frequencies
    elif frequency_GHz < 20:
        zenith_loss = 1.0
    elif frequency_GHz < 30:
        zenith_loss = 2.0
    else:
        zenith_loss = 3.0
    
    # Adjust for elevation angle (more atmosphere at low angles)
    if elevation_angle_deg < 5:
        elevation_factor = 5.0
    elif elevation_angle_deg < 10:
        elevation_factor = 3.0
    elif elevation_angle_deg < 30:
        elevation_factor = 1.5
    else:
        elevation_factor = 1.0
    
    base_loss = zenith_loss * elevation_factor
    
    # Weather effects (simplified)
    weather_loss = {
        'clear': 0.0,
        'rain': 2.0,
        'heavy_rain': 5.0
    }
    
    total_loss = base_loss + weather_loss.get(weather, 0.0)
    
    return total_loss

# ============================================================================
# EXAMPLE USAGE FUNCTIONS
# ============================================================================

def load_constellation_from_tle(tle_filepath: str = 'data/tle/starlink.txt') -> List[Satellite]:
    """
    Complete function to load a constellation from a TLE file.
    
    Args:
        tle_filepath: Path to TLE file
        
    Returns:
        List of Satellite objects
    """
    print(f"Loading TLE data from: {tle_filepath}")
    
    # Parse TLE file
    tle_data = parse_tle_file(tle_filepath)
    
    if not tle_data:
        print("No TLE data found. Using default constellation.")
        from constellations import create_default_constellation
        return create_default_constellation()
    
    print(f"Found {len(tle_data)} satellites in TLE file")
    
    # Convert to Satellite objects
    satellites = tle_to_satellite_objects(tle_data)
    
    print(f"Successfully created {len(satellites)} satellite objects")
    
    return satellites

# ============================================================================
# HOW TO GET NASA DATA
# ============================================================================

"""
WHERE TO GET NASA TLE DATA:

1. CELESTRAK (Free, no registration)
   URL: https://celestrak.org/NORAD/elements/
   
   Popular constellations:
   - Starlink: https://celestrak.org/NORAD/elements/starlink.txt
   - OneWeb: https://celestrak.org/NORAD/elements/oneweb.txt
   - Iridium: https://celestrak.org/NORAD/elements/iridium.txt
   - ISS: https://celestrak.org/NORAD/elements/stations.txt
   
   Download and save to: data/tle/starlink.txt

2. SPACE-TRACK.ORG (Free, requires registration)
   URL: https://www.space-track.org
   - More detailed and frequently updated
   - API access available
   - Requires account (free for non-commercial use)

3. NASA OFFICIAL SOURCES
   - NASA SCaN: https://www.nasa.gov/directorates/heo/scan/
   - Ground station info: https://www.nasa.gov/directorates/heo/scan/services/networks/
   
USAGE IN THIS SIMULATOR:

1. Download TLE file (e.g., starlink.txt)
2. Place in: data/tle/starlink.txt
3. In main.py, add option to load from TLE:

   from nasa_data_integration import load_constellation_from_tle
   
   # In sidebar:
   use_nasa_data = st.sidebar.checkbox("Use NASA TLE Data")
   
   if use_nasa_data:
       satellites = load_constellation_from_tle('data/tle/starlink.txt')
   else:
       satellites = create_default_constellation()

TLE FILE FORMAT:

Each satellite has 3 lines:
Line 0: Satellite name
Line 1: Orbital elements (1/2)
Line 2: Orbital elements (2/2)

Example:
ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
"""

# ============================================================================
# EXAMPLE: INTEGRATION WITH MAIN APP
# ============================================================================

def example_integration():
    """
    Example showing how to integrate NASA data into the main simulation.
    Add this code to main.py:
    """
    example_code = '''
    # In main.py, add to sidebar:
    
    st.sidebar.subheader("NASA Data Integration")
    use_nasa_tle = st.sidebar.checkbox("Use NASA TLE Data", value=False)
    
    if use_nasa_tle:
        tle_file = st.sidebar.text_input(
            "TLE File Path", 
            "data/tle/starlink.txt"
        )
        
        try:
            from nasa_data_integration import load_constellation_from_tle
            satellites = load_constellation_from_tle(tle_file)
            st.sidebar.success(f"Loaded {len(satellites)} satellites from TLE")
        except Exception as e:
            st.sidebar.error(f"Error loading TLE: {e}")
            satellites = create_default_constellation(num_satellites, orbit_altitude_km)
    else:
        satellites = create_default_constellation(num_satellites, orbit_altitude_km)
    
    # For NASA ground stations:
    use_nasa_gs = st.sidebar.checkbox("Use NASA Ground Stations", value=False)
    
    if use_nasa_gs:
        from nasa_data_integration import create_nasa_ground_stations
        ground_stations = create_nasa_ground_stations(network='NEN')
        st.sidebar.success(f"Using {len(ground_stations)} NASA stations")
    else:
        ground_stations = create_default_ground_stations()
    '''
    
    return example_code

if __name__ == "__main__":
    # Test the functions
    print("NASA Data Integration Module - Example Usage\n")
    print("=" * 60)
    
    # Example 1: Parse TLE (will show warning if file doesn't exist)
    print("\n1. Parsing TLE file...")
    tle_data = parse_tle_file('data/tle/starlink.txt')
    print(f"   Found {len(tle_data)} satellites")
    
    # Example 2: Create NASA ground stations
    print("\n2. Creating NASA ground stations...")
    nasa_stations = create_nasa_ground_stations('NEN')
    print(f"   Created {len(nasa_stations)} NASA NEN stations")
    
    for station in nasa_stations:
        print(f"   - {station.station_id}: ({station.latitude_deg:.2f}°, {station.longitude_deg:.2f}°)")
    
    # Example 3: Atmospheric loss
    print("\n3. Calculating atmospheric loss...")
    loss = calculate_atmospheric_loss_nasa(2.4, 30, 'clear')
    print(f"   Atmospheric loss at 2.4 GHz, 30° elevation: {loss:.2f} dB")
    
    print("\n" + "=" * 60)
    print("\nTo use NASA TLE data:")
    print("1. Download TLE from https://celestrak.org/NORAD/elements/")
    print("2. Save to: data/tle/yourfile.txt")
    print("3. Call: load_constellation_from_tle('data/tle/yourfile.txt')")
    print("\nModule ready for integration!")

