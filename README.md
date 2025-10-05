# 🛰️ Satellite Communication Link Simulation Platform

A comprehensive Python-based interactive web application for evaluating satellite communication scenarios using NASA data. This platform enables users to analyze link performance, compare different mission scenarios, and make informed decisions about satellite communication systems.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Dash](https://img.shields.io/badge/dash-2.14.1-green.svg)
![NASA Data](https://img.shields.io/badge/data-NASA%20Powered-red.svg)
![License](https://img.shields.io/badge/license-NASA%20Open%20Source%20Agreement-orange.svg)

## Features

### **Multi-Ground Station Analysis**
- **12 NASA-recommended ground station locations** worldwide
- **Real-time weather data integration** from NASA POWER API
- **Individual station performance analysis** with weather-specific calculations
- **Global coverage optimization** for satellite communication links

### **Comprehensive Cost Analysis**
- **NASA-based cost models** using Small Satellite Technology Program data
- **Multiple satellite types**: CubeSat ($50K) to Large Sat ($10M)
- **Ground station tiers**: Basic ($200K) to Military Grade ($5M)
- **10-year cost projections** including operations, insurance, and maintenance
- **Launch cost calculations** using NASA Commercial Crew Program data

### **Advanced Scenario Comparison**
- **Side-by-side analysis** of two different mission scenarios
- **Interactive visualizations**: line plots, bar charts, radar charts
- **Automated recommendation system** based on user priorities
- **Detailed reasoning** for scenario selection

### **Technical Performance Metrics**
- **Friis transmission equation** calculations
- **Free-space path loss** analysis
- **Signal-to-noise ratio (SNR)** computation
- **Link margin calculations** with atmospheric effects
- **Orbital debris risk assessment** using NASA ODPO data
- **Coverage time estimation** for satellite passes

### **Professional Reporting**
- **Interactive PDF reports** with comprehensive analysis
- **Technical explanations** for power values and calculations
- **NASA data source attribution** and methodology documentation
- **Export capabilities** for further analysis

## Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection (for NASA data API calls)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/satellite-communication-simulator.git
   cd satellite-communication-simulator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the web interface**
   Open your browser and navigate to: `http://127.0.0.1:8050`

## Usage Guide

### 1. **Configure Mission Parameters**
- Select frequency band (L, S, X, Ku, Ka, or optical)
- Set transmit power and antenna gains
- Choose satellite altitude and orbital inclination
- Select number and type of ground stations

### 2. **Select Ground Stations**
- Choose from 12 NASA-recommended locations worldwide
- View coordinates and regional information
- Select multiple stations for optimal coverage

### 3. **Define Scenarios**
- Configure two different mission scenarios (A & B)
- Set satellite types, quantities, and link configurations
- Choose priority: cost, performance, or balanced trade-off

### 4. **Run Analysis**
- Click "Run Simulation" to calculate link performance
- View interactive plots and performance metrics
- Compare scenarios with detailed visualizations
- Review automated recommendations

### 5. **Export Results**
- Download comprehensive PDF reports
- Save analysis data for further processing
- Share results with stakeholders

## Technical Architecture

### **Frontend**
- **Dash/Plotly**: Interactive web interface and visualizations
- **Bootstrap**: Professional UI components and styling
- **Real-time updates**: Dynamic parameter adjustment and results

### **Backend**
- **Flask**: Web server and API endpoints
- **NumPy/SciPy**: Mathematical calculations and signal processing
- **Requests**: NASA API integration for real-time data

### **Data Sources**
- **NASA POWER API**: Real-time weather data
- **NASA ODPO**: Orbital debris information
- **NASA Small Satellite Technology Program**: Cost models
- **ITU-R Recommendations**: Atmospheric attenuation models

## Sample Analysis

### **Link Performance Metrics**
- **Maximum SNR**: Signal-to-noise ratio at optimal range
- **Link Margin**: Safety margin above required threshold
- **Coverage Time**: Duration of satellite visibility
- **Atmospheric Attenuation**: Weather-dependent signal loss

### **Cost Analysis**
- **Initial Investment**: Satellites, ground stations, launch
- **Operational Costs**: 10-year projections with maintenance
- **Total Cost of Ownership**: Complete mission lifecycle analysis

### **Scenario Comparison**
- **Performance vs. Cost**: Trade-off analysis
- **Reliability Assessment**: Weather and operational factors
- **Coverage Analysis**: Global communication capabilities

## Scientific Methodology

### **Link Budget Calculations**
The platform implements the Friis transmission equation:
```
Received Power (dBW) = Transmit Power + Gain_tx + Gain_rx - Path Loss - Atmospheric Loss
```

### **Atmospheric Attenuation**
- **ITU-R models** for different frequency bands
- **Weather-dependent calculations** using NASA data
- **Rain attenuation** for high-frequency bands (Ku/Ka)

### **Orbital Mechanics**
- **Coverage time estimation** based on orbital parameters
- **Range calculations** for different elevation angles
- **Debris risk assessment** using NASA ODPO data

## Project Structure

```
satellite-communication-simulator/
├── app.py                 # Main application file
├── nasa_data.txt         # NASA data and models
├── requirements.txt      # Python dependencies
├── instructions.txt      # Detailed usage instructions
├── README.md            # This file
└── LICENSE              # NASA Open Source Agreement
```

## Contributing

We welcome contributions to improve the satellite communication simulation platform! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### **Areas for Contribution**
- Additional ground station locations
- Enhanced atmospheric models
- New visualization types
- Performance optimizations
- Documentation improvements

## License

This project is licensed under the **NASA Open Source Agreement** - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **NASA** for providing comprehensive satellite and atmospheric data
- **ITU-R** for international telecommunications standards
- **Plotly/Dash** community for excellent visualization tools
- **Open source contributors** who make projects like this possible

## Support

For questions, issues, or feature requests:
- **Email**: [your-email@domain.com]
- **Issues**: [GitHub Issues](https://github.com/yourusername/satellite-communication-simulator/issues)
- **Documentation**: [Project Wiki](https://github.com/yourusername/satellite-communication-simulator/wiki)

## Related Projects

- [NASA POWER API](https://power.larc.nasa.gov/)
- [NASA Orbital Debris Program Office](https://orbitaldebris.jsc.nasa.gov/)
- [ITU-R Recommendations](https://www.itu.int/rec/R-REC/en)

*This project uses NASA data and follows NASA open source guidelines for scientific and educational purposes.*

