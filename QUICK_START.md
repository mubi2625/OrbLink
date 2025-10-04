# ⚡ QUICK START GUIDE

## 🚀 How to Run (3 Steps)

Open PowerShell or Command Prompt in this folder and run:

```powershell
# Step 1: Install (first time only)
pip install -r requirements.txt

# Step 2: Test (optional but recommended)
python test_simulation.py

# Step 3: Launch the app
streamlit run main.py
```

**That's it!** The app opens automatically in your browser at `http://localhost:8501`

---

## 📁 GitHub Checklist

✅ **YES - It's GitHub Ready!** Here's what's included:

- ✅ All source code (7 Python modules)
- ✅ `requirements.txt` (dependencies)
- ✅ `README.md` (full documentation)
- ✅ `SETUP_GUIDE.md` (detailed setup)
- ✅ `.gitignore` (proper exclusions)
- ✅ `LICENSE` (MIT license)
- ✅ `test_simulation.py` (verification script)
- ✅ `nasa_data_integration.py` (NASA data module)

### To Push to GitHub:

```bash
git init
git add .
git commit -m "Initial commit: LEO Link Simulator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/LEO_Link_Simulator.git
git push -u origin main
```

---

## 🛰️ NASA Data Integration

### **Current Status**: Uses DEFAULT/DUMMY DATA
The simulator works perfectly **without NASA data** using built-in defaults.

### **Where NASA Data Would Go**:

1. **TLE (Orbital) Data** → `data/tle/` folder
2. **Ground Stations** → `nasa_data_integration.py` (already configured)
3. **Atmospheric Models** → `nasa_data_integration.py` (simplified model included)

### **How to Add NASA TLE Data**:

#### Option 1: Download from CelesTrak (Easiest)

```bash
# Download Starlink constellation
curl https://celestrak.org/NORAD/elements/starlink.txt -o data/tle/starlink.txt

# Or download manually:
# Visit: https://celestrak.org/NORAD/elements/
# Save to: data/tle/starlink.txt
```

#### Option 2: Use Space-Track.org (More detailed)
1. Register at https://www.space-track.org (free)
2. Download TLE files
3. Save to `data/tle/` folder

### **TLE File Format**:

```
STARLINK-1007
1 44713U 19074A   24275.12345678  .00001234  00000-0  12345-4 0  9999
2 44713  53.0000 123.4567 0001234  12.3456 347.1234 15.01234567123456

STARLINK-1008
1 44714U 19074B   24275.23456789  .00002345  00000-0  23456-4 0  9998
2 44714  53.0000 124.5678 0002345  23.4567 336.5678 15.02345678234567
```

3 lines per satellite:
- **Line 0**: Satellite name
- **Line 1**: Orbital elements (part 1)
- **Line 2**: Orbital elements (part 2)

### **Available NASA Data Sources**:

| Source | Type | URL | Format |
|--------|------|-----|--------|
| **CelesTrak** | TLE Data | https://celestrak.org/NORAD/elements/ | .txt |
| **Space-Track** | TLE Data | https://www.space-track.org | .txt, API |
| **NASA SCaN** | Ground Stations | https://www.nasa.gov/directorates/heo/scan/ | Documentation |
| **NASA Earthdata** | Atmospheric | https://earthdata.nasa.gov/ | Multiple |

### **Popular Constellations (TLE):**

- **Starlink**: https://celestrak.org/NORAD/elements/starlink.txt
- **OneWeb**: https://celestrak.org/NORAD/elements/oneweb.txt
- **Iridium**: https://celestrak.org/NORAD/elements/iridium.txt
- **GPS**: https://celestrak.org/NORAD/elements/gps-ops.txt
- **ISS**: https://celestrak.org/NORAD/elements/stations.txt

### **To Use NASA Data in the App**:

See `nasa_data_integration.py` for complete examples. Here's a quick snippet:

```python
# In your code or main.py:
from nasa_data_integration import load_constellation_from_tle

# Load real Starlink data
satellites = load_constellation_from_tle('data/tle/starlink.txt')

# Or use NASA ground stations
from nasa_data_integration import create_nasa_ground_stations
ground_stations = create_nasa_ground_stations(network='NEN')
```

---

## 🎯 Current vs NASA Data

### **RIGHT NOW (Default Data)**:
- ✅ 6 simulated satellites at 500 km
- ✅ 5 global ground stations (major cities)
- ✅ Simplified atmospheric model (2 dB loss)
- ✅ Works perfectly for demo/hackathon
- ✅ **No external data needed**

### **WITH NASA TLE DATA**:
- 🛰️ Real satellite positions from orbital elements
- 🛰️ Actual constellation configurations (Starlink, OneWeb, etc.)
- 🛰️ Real-time or historical orbital data
- 🛰️ More accurate link calculations
- 📡 NASA ground station locations (DSN, NEN)

---

## 💡 Recommendation

**For your hackathon/demo**: 
- ✅ Use the **default data** (it's ready now!)
- ✅ Mention "NASA TLE integration supported"
- ✅ Show the `nasa_data_integration.py` file

**After the hackathon**:
- 📥 Download real TLE data for production use
- 🔧 Integrate with live TLE feeds
- 📊 Compare against real constellations

---

## 📞 Quick Commands Reference

```bash
# Run the simulator
streamlit run main.py

# Test everything
python test_simulation.py

# Test NASA integration
python nasa_data_integration.py

# Install dependencies
pip install -r requirements.txt

# Run on different port
streamlit run main.py --server.port 8502
```

---

## ✅ You're Ready!

- ✅ Code is complete
- ✅ GitHub ready
- ✅ NASA data module included
- ✅ Works with default data NOW
- ✅ Can add NASA data LATER

**Run it**: `streamlit run main.py`

🎉 **Happy Simulating!**

