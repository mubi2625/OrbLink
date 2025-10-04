# 🛰️ NASA Data Integration Guide

## ✅ **Setup Complete!**

Your simulator now has **real NASA TLE data** for 5 constellations:

- ✅ **Starlink** - 6,000+ satellites
- ✅ **OneWeb** - 600+ satellites  
- ✅ **Iridium** - 100+ satellites
- ✅ **GPS** - 30+ satellites
- ✅ **ISS** - International Space Station

---

## 🚀 **How to Use NASA Data**

### **Step 1: Launch the App**

```powershell
python -m streamlit run main.py
```

### **Step 2: Enable NASA Data**

In the **sidebar**, look for:

**"🛰️ NASA Data (Optional)"**

1. ✅ **Check** the box: "Use Real NASA TLE Data"
2. **Select** a constellation from the dropdown:
   - Starlink (recommended - lots of satellites)
   - OneWeb
   - Iridium
   - GPS
   - ISS
3. (Optional) ✅ Check "Use NASA Ground Stations"
   - Select network: NEN, DSN, or Both

### **Step 3: Run Simulation**

Click **"🚀 Run Simulation"**

The app will:
- Load real satellite positions from NASA TLE data
- Display "✅ Loaded X satellites from [constellation]!"
- Run simulation with real orbital data

---

## 📊 **What's Different with NASA Data?**

### **Default Mode** (unchecked):
- 6 simulated satellites
- Circular orbits at 500 km
- Evenly distributed
- Perfect for demos

### **NASA TLE Mode** (checked):
- Real satellite positions
- Actual orbital elements
- Current constellation state
- More realistic results

---

## 🌐 **Available Constellations**

| Constellation | # Satellites | Altitude | Purpose |
|--------------|--------------|----------|---------|
| **Starlink** | 6,000+ | 340-550 km | Internet |
| **OneWeb** | 600+ | 1,200 km | Internet |
| **Iridium** | 100+ | 780 km | Communications |
| **GPS** | 31 | 20,200 km | Navigation |
| **ISS** | 1 | 408 km | Research |

---

## 📡 **NASA Ground Stations**

When enabled, you can use real NASA ground station locations:

### **NEN (Near Earth Network)**:
- White Sands, New Mexico
- Alaska Ground Station
- Svalbard, Norway

### **DSN (Deep Space Network)**:
- Goldstone, California (74 dBi antenna!)
- Canberra, Australia
- Madrid, Spain

### **Both**:
- All 6 NASA stations

---

## 🔄 **Updating TLE Data**

TLE data changes daily as satellites orbit. To get fresh data:

### **Option 1: Let the App Download**
- Just select a constellation
- If file is missing, app auto-downloads from CelesTrak

### **Option 2: Manual Download**
```powershell
# Starlink
Invoke-WebRequest -Uri "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle" -OutFile "data/tle/starlink.txt"

# OneWeb
Invoke-WebRequest -Uri "https://celestrak.org/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=tle" -OutFile "data/tle/oneweb.txt"

# Iridium
Invoke-WebRequest -Uri "https://celestrak.org/NORAD/elements/gp.php?GROUP=iridium&FORMAT=tle" -OutFile "data/tle/iridium.txt"

# GPS
Invoke-WebRequest -Uri "https://celestrak.org/NORAD/elements/gp.php?GROUP=gps-ops&FORMAT=tle" -OutFile "data/tle/gps.txt"

# ISS
Invoke-WebRequest -Uri "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle" -OutFile "data/tle/iss.txt"
```

---

## 💡 **Pro Tips**

### **For Demos:**
- Use **default mode** for fast, predictable results
- Mention "NASA TLE integration available"

### **For Analysis:**
- Use **Starlink** - largest constellation
- Compare different constellations
- Try NASA ground stations for realistic scenario

### **For Presentations:**
1. Run default first → show baseline
2. Enable NASA data → show real constellation
3. Compare results → demonstrate capability

---

## 📈 **Expected Results**

### **Starlink Example:**
- **Satellites**: ~6,000+
- **Coverage**: Very high (95%+)
- **Latency**: Low (real spacing)
- **Processing**: Takes longer (more satellites)

### **GPS Example:**
- **Satellites**: ~31
- **Altitude**: Very high (20,200 km)
- **Coverage**: Global
- **Latency**: Higher (distance)

---

## 🛠️ **Troubleshooting**

### **"TLE file not found"**
✅ **Solution**: App will auto-download from CelesTrak

### **"Too many satellites"**
✅ **Solution**: Reduce time steps (50 instead of 100)

### **"Processing takes too long"**
✅ **Solution**: 
- Use fewer satellites (ISS = 1 satellite)
- Reduce time steps
- Use default mode

### **"Module skyfield not found"**
✅ **Solution**: 
```powershell
pip install skyfield
```

---

## 📁 **File Locations**

All TLE files are stored in:
```
data/tle/
  ├── starlink.txt   ✅ Downloaded
  ├── oneweb.txt     ✅ Downloaded
  ├── iridium.txt    ✅ Downloaded
  ├── gps.txt        ✅ Downloaded
  └── iss.txt        ✅ Downloaded
```

---

## 🎯 **Quick Start with NASA Data**

1. **Launch**: `python -m streamlit run main.py`
2. **Check**: "Use Real NASA TLE Data"
3. **Select**: "Starlink"
4. **Check**: "Use NASA Ground Stations" → "NEN"
5. **Set Time Steps**: 50 (for faster processing)
6. **Click**: "🚀 Run Simulation"
7. **Wait**: ~20-30 seconds (more satellites = longer)
8. **Explore**: Check all 4 tabs!

---

## 📚 **Data Sources**

- **TLE Data**: https://celestrak.org (CelesTrak)
- **Ground Stations**: NASA SCaN
- **Format**: Two-Line Element (TLE) standard
- **Update Frequency**: Daily
- **Free**: Yes, no API key needed

---

## ✨ **Summary**

You now have:
- ✅ 5 real NASA constellation datasets
- ✅ Automatic TLE download feature
- ✅ NASA ground station integration
- ✅ Real-time orbital calculations
- ✅ Comparison with default data

**Your simulator can now analyze REAL satellite constellations!** 🎉

---

**Ready to simulate?** Launch the app and try Starlink! 🛰️✨

