# 🚀 Quick Setup Guide

## Step-by-Step Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web interface
- `numpy` - Numerical computations
- `pandas` - Data manipulation
- `matplotlib` - Static plots
- `plotly` - Interactive visualizations
- `skyfield` - Orbital calculations (optional)
- `scipy` - Scientific computing

### 2. Verify Installation

Run the test script to ensure everything works:

```bash
python test_simulation.py
```

You should see output like:
```
🧪 Testing LEO Link Simulator...
✅ Test 1: Creating satellite constellation...
✅ Test 2: Creating ground stations...
✅ Test 3: Testing link budget calculations...
✅ Test 4: Running mini simulation...
✅ Test 5: Calculating coverage metrics...
✅ Test 6: Testing cost model...
✨ All tests passed! System is ready to run.
```

### 3. Launch the Streamlit App

```bash
streamlit run main.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 🎮 First Simulation

1. **Default Parameters** are pre-configured - just click "🚀 Run Simulation"
2. **Wait 5-10 seconds** for the simulation to complete
3. **Explore the tabs**:
   - 📊 Simulation Results - SNR, latency, coverage
   - 💰 Cost Analysis - CapEx comparison
   - 📈 Value Dashboard - KPIs and ROI
   - 📋 Data Tables - Export data

---

## 🛠️ Troubleshooting

### Issue: "Import could not be resolved"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Streamlit not found"
**Solution**: Make sure streamlit is installed
```bash
pip install streamlit
```

### Issue: Port 8501 already in use
**Solution**: Use a different port
```bash
streamlit run main.py --server.port 8502
```

### Issue: Simulation takes too long
**Solution**: Reduce time steps in the sidebar (try 50 instead of 100)

---

## 📊 Recommended First Run

Use these settings for a quick demo:

**Satellite Configuration**:
- Number of Satellites: 6
- Orbit Altitude: 500 km
- Transmit Power: 20 dBW
- Antenna Gain: 20 dBi
- Frequency: 2.4 GHz

**Ground Station Configuration**:
- Ground Stations (GS-Only): 5
- Ground Stations (Crosslinked): 2

**Simulation Settings**:
- Time Steps: 100
- Orbit Period: 90 minutes

Click **Run Simulation** and wait ~10 seconds!

---

## 🎯 What to Expect

### Typical Results:
- **Coverage Improvement**: +15-25% with crosslinked architecture
- **Latency Reduction**: ~93% faster (1000ms → 50ms)
- **Cost Savings**: ~50-60% CapEx reduction
- **Ground Stations**: 60% fewer stations needed

### Performance:
- Simulation time: 5-15 seconds
- Data points generated: 100-600 per constellation
- Plots: 8 interactive visualizations
- Export: CSV data available for download

---

## 📱 Interface Overview

### Sidebar (Left)
- Configuration sliders
- Run simulation button
- Parameter controls

### Main Area (Tabs)
1. **Simulation Results**
   - SNR vs Time plot
   - Latency comparison
   - Coverage metrics
   - Distance distribution

2. **Cost Analysis**
   - Total CapEx comparison
   - Cost breakdown charts
   - Savings calculation

3. **Value Dashboard**
   - KPI metrics
   - Business impact summary
   - ROI analysis

4. **Data Tables**
   - Raw simulation data
   - CSV export buttons
   - Detailed metrics

---

## 💡 Tips

- **Adjust parameters** to see how they affect performance
- **Compare architectures** side-by-side in the plots
- **Export data** for external analysis
- **Run multiple simulations** with different configurations
- **Check the Value Dashboard** for business case summary

---

## 🔧 Advanced Configuration

### Custom Ground Stations
Edit `constellations.py` line 259-266:
```python
ground_stations = [
    GroundStation("GS_01", lat, lon, alt, gain),
    # Add more stations...
]
```

### Adjust Cost Models
Edit `cost_model.py` lines 4-6:
```python
COST_PER_GROUND_STATION = 5_000_000
COST_PER_ISL_HARDWARE = 500_000
COST_PER_SATELLITE_BASE = 2_000_000
```

### Modify Link Thresholds
Edit `link_budget.py` lines 60-66:
```python
def is_link_feasible(snr_dB: float, required_snr_dB: float = 10.0) -> bool:
    return snr_dB >= required_snr_dB
```

---

## 📚 Next Steps

1. **Run the test script** to verify everything works
2. **Launch the app** and run your first simulation
3. **Experiment with parameters** to understand the trade-offs
4. **Export data** for presentations or further analysis
5. **Customize** the code for your specific use case

---

## ✅ Checklist

- [ ] Installed Python 3.10+
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Ran test script successfully (`python test_simulation.py`)
- [ ] Launched Streamlit app (`streamlit run main.py`)
- [ ] Ran first simulation with default parameters
- [ ] Explored all four tabs
- [ ] Experimented with parameter adjustments

---

**You're ready to simulate!** 🛰️✨

For questions or issues, refer to the main README.md file.

