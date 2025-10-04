# 🛰️ OrbLink Simulator

A Python based **LEO satellite constellation link feasibility simulator** that compares two architecture strategies:
1. **Ground-Station-Only** (satellites communicate only via ground stations)
2. **Crosslinked** (satellites communicate with each other + minimal ground stations)

Built for hackathon demonstrations and feasibility studies.

## Team Members
- Mubasshirah Khan
- Gaurav Mishra
- Syun M. Dixit
- Surith Hariharan Thogulava
- Sofia Adelentado Lopez

---

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to project directory
cd LEO_Link_Simulator

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
LEO_Link_Simulator/
│
├── main.py                  # Streamlit web interface
├── constellations.py        # Satellite & GroundStation classes
├── link_budget.py           # Friis equation, SNR, latency calculations
├── simulation.py            # Orbit propagation & simulation engine
├── cost_model.py            # Cost analysis & CapEx calculations
├── plots.py                 # Interactive visualization functions
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── data/
    └── tle/                # (Optional) NASA TLE data files
```

---

## 🔧 Features

### Link Budget Analysis
- **Friis Transmission Equation**: Calculate received power with path loss, atmospheric loss, and system losses
- **SNR Calculation**: Signal-to-Noise Ratio with configurable threshold (default: 10 dB)
- **Link Margin**: Determine link feasibility based on SNR requirements
- **Latency Modeling**: 
  - Ground stations: ~500-1000 ms (includes ground processing)
  - Crosslinks: ~30-50 ms (satellite-to-satellite)

### Orbital Simulation
- Circular orbit propagation for LEO satellites (400-800 km altitude)
- Line-of-sight visibility calculations
- Multi-satellite constellation support (4-12 satellites)
- Global ground station distribution

### Cost Analysis
- **CapEx Breakdown**:
  - Ground station costs: $5M per station
  - Satellite base cost: $2M per satellite
  - ISL hardware: $500K per satellite
- **ROI Metrics**: Calculate return on investment with performance improvements
- **Savings Analysis**: Compare architectures and identify optimal strategy

### Interactive Visualizations
- SNR over time comparison
- Latency trends
- Coverage and availability metrics
- Cost breakdown charts
- Link distance distributions
- Satellite coverage heatmaps

---

## 📊 Technical Models

### Friis Equation
```
Pr(dBW) = Pt(dBW) + Gt(dBi) + Gr(dBi) - Lp(dB) - Latm(dB) - Lsys(dB)

where:
  Lp(dB) = 20 * log10(4 * π * d / λ)
```

### SNR Calculation
```
SNR = Pr / (k * T * B)
SNR_dB = Pr(dBW) - 10*log10(k * T * B)

Threshold: SNR > 10 dB = feasible link
```

### Latency
- **Ground-station-only**: t = 2 * (d_sat-GS / c) + t_processing (~500-1000 ms)
- **Crosslink**: t = d_sat-sat / c + t_processing (~30-50 ms)

### Coverage Metrics
- **Availability**: Link available if LOS exists AND SNR > threshold
- **Coverage %**: (time_link_available / total_orbit_time) * 100%
- **Downtime**: total_orbit_time - link_available_time

---

## 🎮 Usage

### Sidebar Controls

**Satellite Configuration**:
- Number of satellites: 4-12
- Orbit altitude: 400-800 km
- Transmit power: 10-30 dBW
- Antenna gain: 10-30 dBi
- Frequency: 1-30 GHz

**Ground Station Configuration**:
- Ground stations (GS-Only): 3-10
- Ground stations (Crosslinked): 1-5

**Simulation Settings**:
- Time steps: 50-200
- Orbit period: 80-100 minutes

### Output Tabs

1. **Simulation Results**: SNR, latency, coverage plots and metrics
2. **Cost Analysis**: CapEx comparison and breakdown
3. **Value Dashboard**: KPIs, ROI, and business impact summary
4. **Data Tables**: Raw data export and detailed metrics

---

## 🌍 Default Configuration

### Satellites
- **Count**: 6 satellites
- **Altitude**: 500 km (LEO)
- **Orbit**: Circular, equatorial (simplified)
- **Distribution**: Evenly spaced around orbit

### Ground Stations (5 global locations)
1. New York, USA (40.71°N, 74.01°W)
2. London, UK (51.51°N, 0.13°W)
3. Tokyo, Japan (35.68°N, 139.65°E)
4. Sydney, Australia (33.87°S, 151.21°E)
5. Moscow, Russia (55.76°N, 37.62°E)

---

## 📈 Example Results

### Typical Performance Comparison

| Metric | Ground-Station-Only | Crosslinked | Improvement |
|--------|---------------------|-------------|-------------|
| Coverage | 65-75% | 85-95% | +15-20% |
| Avg Latency | 800-1000 ms | 40-60 ms | -93% |
| Avg SNR | 15-20 dB | 20-25 dB | +5 dB |
| Ground Stations | 5 | 2 | -60% |
| Total CapEx | $37M | $16M | -57% |

---

## 🔬 Technical Details

### Physical Constants
- **Boltzmann Constant**: 1.380649×10⁻²³ J/K
- **Speed of Light**: 299,792,458 m/s
- **Earth Radius**: 6,371 km

### Assumptions
- Circular orbits (simplified orbital mechanics)
- Equatorial plane orbits
- Atmospheric loss: 2 dB (simplified)
- System loss: 3 dB
- System noise temperature: 290 K
- Processing delay: 5 ms base + 50 ms for ground stations

---

## 🛠️ Dependencies

```txt
streamlit>=1.28.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
plotly>=5.15.0
skyfield>=1.46
scipy>=1.10.0
```

Python 3.10+ recommended

---

## 🎯 Use Cases

1. **Feasibility Studies**: Evaluate constellation architectures before deployment
2. **Cost Optimization**: Compare infrastructure investment strategies
3. **Performance Analysis**: Understand SNR, latency, and coverage trade-offs
4. **Educational Tool**: Learn satellite communication link budgets
5. **Hackathon Demos**: Quick, visual satellite network simulations

---

## 🚧 Future Enhancements

- [ ] Integration with real NASA TLE data
- [ ] Non-circular orbit support (elliptical, polar)
- [ ] Advanced atmospheric models
- [ ] Multi-plane constellation configurations
- [ ] Real-time satellite tracking
- [ ] Earth coverage maps
- [ ] Doppler shift calculations
- [ ] Weather impact modeling

---

## 📝 Notes

- **Simulation Speed**: Runs in seconds for 100 time steps
- **Data Export**: Download CSV files of simulation results
- **Customizable**: All parameters adjustable via UI
- **No External Data Required**: Works with built-in defaults

---

## 🤝 Contributing

This is a prototype designed for rapid demonstration. Feel free to extend with:
- More sophisticated orbital mechanics
- Additional ground station networks
- Advanced link budget models
- Machine learning for optimization

---

## 📄 License

Open source - built for educational and demonstration purposes.

---

## 🙏 Acknowledgments

- **Orbital Mechanics**: Simplified circular orbit propagation
- **Ground Station Locations**: Based on major global cities
- **Cost Models**: Industry-standard CapEx estimates
- **Link Budget**: Standard RF link budget equations

---

## 📧 Contact

Built as a hackathon prototype for LEO satellite constellation analysis.

**Ready to simulate!** 🛰️✨

---

*Last Updated: October 2025*




