import numpy as np
import math
from typing import Tuple, Optional

class Satellite:
    """
    Represents a LEO satellite with orbital parameters and communication capabilities.
    """
    
    def __init__(self, 
                 satellite_id: str,
                 position: np.ndarray,
                 velocity: np.ndarray,
                 transmit_power_dBW: float = 20.0,
                 antenna_gain_dBi: float = 20.0,
                 frequency_GHz: float = 2.4,
                 orbit_altitude_km: float = 500.0):
        """
        Initialize a satellite.
        
        Args:
            satellite_id: Unique identifier for the satellite
            position: 3D position vector [x, y, z] in meters (ECI coordinates)
            velocity: 3D velocity vector [vx, vy, vz] in m/s
            transmit_power_dBW: Transmit power in dBW
            antenna_gain_dBi: Antenna gain in dBi
            frequency_GHz: Operating frequency in GHz
            orbit_altitude_km: Orbital altitude in km
        """
        self.satellite_id = satellite_id
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.transmit_power_dBW = transmit_power_dBW
        self.antenna_gain_dBi = antenna_gain_dBi
        self.frequency_GHz = frequency_GHz
        self.orbit_altitude_km = orbit_altitude_km
        
        # Derived parameters
        self.earth_radius = 6371000  # Earth radius in meters
        self.orbit_radius = self.earth_radius + orbit_altitude_km * 1000
        
    def compute_distance(self, other) -> float:
        """
        Compute 3D distance to another satellite or ground station.
        
        Args:
            other: Another Satellite or GroundStation object
            
        Returns:
            Distance in meters
        """
        return np.linalg.norm(self.position - other.position)
    
    def is_visible(self, other, min_elevation_deg: float = 0.0) -> bool:
        """
        Check if another satellite or ground station is visible (line of sight).
        
        Args:
            other: Another Satellite or GroundStation object
            min_elevation_deg: Minimum elevation angle in degrees
            
        Returns:
            True if visible, False otherwise
        """
        # For satellite-to-satellite links, always assume visibility in LEO
        if isinstance(other, Satellite):
            return True
            
        # For satellite-to-ground station links, check elevation angle
        if isinstance(other, GroundStation):
            # Vector from ground station to satellite
            vec_to_sat = self.position - other.position
            
            # Distance to satellite
            distance = np.linalg.norm(vec_to_sat)
            
            # Elevation angle calculation
            # For ground stations, we need to consider Earth's curvature
            # Simplified: check if satellite is above horizon
            elevation_angle = np.arcsin(np.dot(vec_to_sat, other.position) / 
                                      (distance * np.linalg.norm(other.position)))
            elevation_deg = np.degrees(elevation_angle)
            
            return elevation_deg >= min_elevation_deg
    
    def update_position(self, dt: float):
        """
        Update satellite position based on orbital mechanics (simplified).
        
        Args:
            dt: Time step in seconds
        """
        # Simplified circular orbit propagation
        # In a real implementation, this would use proper orbital mechanics
        omega = np.sqrt(3.986004418e14 / (self.orbit_radius ** 3))  # Angular velocity
        
        # Update position based on circular orbit
        current_angle = np.arctan2(self.position[1], self.position[0])
        new_angle = current_angle + omega * dt
        
        # Update position maintaining circular orbit
        self.position[0] = self.orbit_radius * np.cos(new_angle)
        self.position[1] = self.orbit_radius * np.sin(new_angle)
        # Z component remains constant for equatorial orbit (simplified)
        
        # Update velocity
        self.velocity[0] = -omega * self.orbit_radius * np.sin(new_angle)
        self.velocity[1] = omega * self.orbit_radius * np.cos(new_angle)
        self.velocity[2] = 0.0


class GroundStation:
    """
    Represents a ground station with location and communication capabilities.
    """
    
    def __init__(self, 
                 station_id: str,
                 latitude_deg: float,
                 longitude_deg: float,
                 altitude_m: float = 0.0,
                 antenna_gain_dBi: float = 30.0,
                 system_temperature_K: float = 290.0):
        """
        Initialize a ground station.
        
        Args:
            station_id: Unique identifier for the ground station
            latitude_deg: Latitude in degrees
            longitude_deg: Longitude in degrees
            altitude_m: Altitude above sea level in meters
            antenna_gain_dBi: Antenna gain in dBi
            system_temperature_K: System noise temperature in Kelvin
        """
        self.station_id = station_id
        self.latitude_deg = latitude_deg
        self.longitude_deg = longitude_deg
        self.altitude_m = altitude_m
        self.antenna_gain_dBi = antenna_gain_dBi
        self.system_temperature_K = system_temperature_K
        
        # Convert to ECI coordinates
        self.position = self._lat_lon_to_eci(latitude_deg, longitude_deg, altitude_m)
    
    def _lat_lon_to_eci(self, lat_deg: float, lon_deg: float, alt_m: float) -> np.ndarray:
        """
        Convert latitude, longitude, altitude to ECI coordinates.
        
        Args:
            lat_deg: Latitude in degrees
            lon_deg: Longitude in degrees
            alt_m: Altitude in meters
            
        Returns:
            3D position vector in ECI coordinates
        """
        earth_radius = 6371000  # Earth radius in meters
        r = earth_radius + alt_m
        
        lat_rad = np.radians(lat_deg)
        lon_rad = np.radians(lon_deg)
        
        x = r * np.cos(lat_rad) * np.cos(lon_rad)
        y = r * np.cos(lat_rad) * np.sin(lon_rad)
        z = r * np.sin(lat_rad)
        
        return np.array([x, y, z])
    
    def compute_distance(self, other) -> float:
        """
        Compute 3D distance to another satellite or ground station.
        
        Args:
            other: Another Satellite or GroundStation object
            
        Returns:
            Distance in meters
        """
        return np.linalg.norm(self.position - other.position)
    
    def is_visible(self, other, min_elevation_deg: float = 0.0) -> bool:
        """
        Check if a satellite is visible from this ground station.
        
        Args:
            other: A Satellite object
            min_elevation_deg: Minimum elevation angle in degrees
            
        Returns:
            True if visible, False otherwise
        """
        if not isinstance(other, Satellite):
            return False
            
        # Vector from ground station to satellite
        vec_to_sat = other.position - self.position
        
        # Distance to satellite
        distance = np.linalg.norm(vec_to_sat)
        
        # Elevation angle calculation
        # Simplified: check if satellite is above horizon
        elevation_angle = np.arcsin(np.dot(vec_to_sat, self.position) / 
                                  (distance * np.linalg.norm(self.position)))
        elevation_deg = np.degrees(elevation_angle)
        
        return elevation_deg >= min_elevation_deg


def create_default_constellation(num_satellites: int = 6, 
                                altitude_km: float = 500.0) -> list:
    """
    Create a default constellation of satellites in circular orbits.
    
    Args:
        num_satellites: Number of satellites in the constellation
        altitude_km: Orbital altitude in km
        
    Returns:
        List of Satellite objects
    """
    satellites = []
    earth_radius = 6371000
    orbit_radius = earth_radius + altitude_km * 1000
    
    for i in range(num_satellites):
        # Distribute satellites evenly around the orbit
        angle = 2 * np.pi * i / num_satellites
        
        # Initial position
        x = orbit_radius * np.cos(angle)
        y = orbit_radius * np.sin(angle)
        z = 0.0  # Simplified: equatorial orbit
        
        # Initial velocity (circular orbit)
        omega = np.sqrt(3.986004418e14 / (orbit_radius ** 3))
        vx = -omega * orbit_radius * np.sin(angle)
        vy = omega * orbit_radius * np.cos(angle)
        vz = 0.0
        
        satellite = Satellite(
            satellite_id=f"SAT_{i+1:02d}",
            position=[x, y, z],
            velocity=[vx, vy, vz],
            orbit_altitude_km=altitude_km
        )
        satellites.append(satellite)
    
    return satellites


def create_default_ground_stations() -> list:
    """
    Create a default set of ground stations globally distributed.
    
    Returns:
        List of GroundStation objects
    """
    ground_stations = [
        GroundStation("GS_01", 40.7128, -74.0060, 0, 30.0),  # New York
        GroundStation("GS_02", 51.5074, -0.1278, 0, 30.0),   # London
        GroundStation("GS_03", 35.6762, 139.6503, 0, 30.0),  # Tokyo
        GroundStation("GS_04", -33.8688, 151.2093, 0, 30.0), # Sydney
        GroundStation("GS_05", 55.7558, 37.6176, 0, 30.0),   # Moscow
    ]
    return ground_stations
