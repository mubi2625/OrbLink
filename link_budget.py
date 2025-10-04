import numpy as np
import math
from typing import Tuple

# Physical constants
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
SPEED_OF_LIGHT = 299792458  # m/s

def friis_received_power(transmit_power_dBW: float,
                        transmit_gain_dBi: float,
                        receive_gain_dBi: float,
                        distance_m: float,
                        frequency_Hz: float,
                        atmospheric_loss_dB: float = 2.0,
                        system_loss_dB: float = 3.0) -> float:
    """Calculate received power using the Friis transmission equation."""
    # Convert dBW to linear
    Pt_linear = 10**(transmit_power_dBW / 10)
    
    # Convert dBi to linear
    Gt_linear = 10**(transmit_gain_dBi / 10)
    Gr_linear = 10**(receive_gain_dBi / 10)
    
    # Wavelength
    wavelength = SPEED_OF_LIGHT / frequency_Hz
    
    # Free space path loss
    path_loss_linear = (4 * np.pi * distance_m / wavelength) ** 2
    path_loss_dB = 10 * np.log10(path_loss_linear)
    
    # Total losses
    total_loss_dB = path_loss_dB + atmospheric_loss_dB + system_loss_dB
    
    # Received power in dBW
    received_power_dBW = (transmit_power_dBW + 
                         transmit_gain_dBi + 
                         receive_gain_dBi - 
                         total_loss_dB)
    
    return received_power_dBW

def calculate_snr(received_power_dBW: float,
                 bandwidth_Hz: float,
                 system_temperature_K: float = 290.0) -> Tuple[float, float]:
    """Calculate Signal-to-Noise Ratio (SNR)."""
    # Convert received power to linear
    received_power_linear = 10**(received_power_dBW / 10)
    
    # Noise power
    noise_power_linear = BOLTZMANN_CONSTANT * system_temperature_K * bandwidth_Hz
    
    # SNR linear
    snr_linear = received_power_linear / noise_power_linear
    
    # SNR in dB
    snr_dB = 10 * np.log10(snr_linear)
    
    return snr_dB, snr_linear

def calculate_link_margin(snr_dB: float, required_snr_dB: float = 10.0) -> float:
    """Calculate link margin."""
    return snr_dB - required_snr_dB

def is_link_feasible(snr_dB: float, required_snr_dB: float = 10.0) -> bool:
    """Determine if a link is feasible based on SNR threshold."""
    return snr_dB >= required_snr_dB

def calculate_latency(distance_m: float, 
                     processing_delay_ms: float = 5.0,
                     is_crosslink: bool = False) -> float:
    """Calculate communication latency."""
    # Propagation delay
    propagation_delay_ms = (distance_m / SPEED_OF_LIGHT) * 1000
    
    # For ground station links, add additional processing delay
    if not is_crosslink:
        processing_delay_ms += 50  # Additional ground station processing
    
    total_latency_ms = propagation_delay_ms + processing_delay_ms
    
    return total_latency_ms
