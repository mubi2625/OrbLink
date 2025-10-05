#  OrbLink Simulation Platform

A comprehensive Python based interactive web application for evaluating satellite communication scenarios using NASA data. This platform enables users to analyse link performance, compare different mission scenarios, and make informed decisions about satellite communication systems.

# Team Members
- Gaurav Mishra
- Mubasshirah Khan
- Surith Thogulava
- Syun M. Dixit
- Sofia Adelantado Lopez


## Instructions to Run Code

### Prerequisites
- Python 3.7 or higher
- Internet connection (for NASA data API calls)

### Installation

1. **Clone the repository into VSCode Terminal**
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

## Simulator Usage Guide

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
- Compare scenarios with detailed visualisations
- Review automated recommendations

### 5. **Export Results**
- Download comprehensive PDF reports
- Save analysis data for further processing
- Share results with stakeholders

## Technical Architecture

### **Frontend**
- **Dash/Plotly**: Interactive web interface and visualisations
- **Bootstrap**: Professional UI components and styling
- **Real-time updates**: Dynamic parameter adjustment and results

### **Backend**
- **Flask**: Web server and API endpoints
- **NumPy/SciPy**: Mathematical calculations and signal processing
- **Requests**: NASA API integration for real time data

### **Data Sources**
- **NASA POWER API**: Real time weather data
- **NASA ODPO**: Orbital debris information
- **NASA Small Satellite Technology Program**: Cost models
- **ITU-R Recommendations**: Atmospheric attenuation models

## Sample Analysis

### **Link Performance Metrics**
- **Maximum SNR**: Signal-to-noise ratio at optimal range
- **Link Margin**: Safety margin above required threshold
- **Coverage Time**: Duration of satellite visibility
- **Atmospheric Attenuation**: Weather dependent signal loss

### **Cost Analysis**
- **Initial Investment**: Satellites, ground stations, launch
- **Operational Costs**: 10 year projections with maintenance
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
- **Rain attenuation** for high frequency bands (Ku/Ka)

### **Orbital Mechanics**
- **Coverage time estimation** based on orbital parameters
- **Range calculations** for different elevation angles
- **Debris risk assessment** using NASA ODPO data


### **Areas for Contribution**
- Additional ground station locations
- Enhanced atmospheric models
- New visualization types
- Performance optimizations
- Documentation improvements

## License

This project is licensed under the **NASA Open Source Agreement** - see the [LICENSE](LICENSE) file for details.



