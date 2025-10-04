# LEO Link Simulator - Quick Reference Card

## Key Numbers to Remember

### Cost Benchmarks
- Ground Station: **$10M** each
- ISL Hardware: **$500K** per satellite
- Ground Station OpEx: **$500K** per year
- FCC License: **$500K**
- ITU Coordination: **$200K**

### Performance Targets
- Minimum SNR: **10 dB** (for feasible link)
- Ground latency: **500-1000 ms**
- Crosslink latency: **30-50 ms**
- Target coverage: **>90%**

### Regulatory Timelines
- FCC approval: **12 months**
- ITU coordination: **18 months**
- FCC deorbit rule: **25 years** maximum

### Debris Risk Thresholds
- Low risk: **<1% collision probability**
- Moderate risk: **1-5%**
- High risk: **5-15%**
- Critical risk: **>15%**

---

## Parameter Quick Guide

| Parameter | Typical Range | Impact |
|-----------|---------------|--------|
| Transmit Power | 10-30 dBW | Higher power = better SNR, more battery drain |
| Frequency | 2-30 GHz | Higher frequency = more bandwidth, more losses |
| Antenna Gain | 10-30 dBi | Higher gain = better link, larger antenna |
| Orbit Altitude | 400-800 km | Lower = better for debris, shorter decay time |
| Satellites | 5-100 | More satellites = better coverage, higher collision risk |
| Ground Stations | 3-10 | More stations = better coverage, higher cost |

---

## Decision Matrix: Ground vs Crosslink

| Factor | Ground-Station-Only | Crosslinked |
|--------|---------------------|-------------|
| **CapEx** | High (many GS) | Lower (ISL hardware cheaper) |
| **OpEx** | High (GS operations) | Lower (fewer GS) |
| **Latency** | 500-1000 ms | 30-50 ms |
| **Coverage** | Limited by GS locations | Global with fewer GS |
| **Complexity** | Simpler | More complex routing |
| **Best for** | <10 satellites | >20 satellites |
| **Tipping point** | Varies by GS count | Typically 15-30 satellites |

---

## Altitude Selection Guide

| Altitude (km) | Pros | Cons | Deorbit |
|---------------|------|------|---------|
| **400-500** | Fast natural decay (1-5 yrs), low collision risk | Drag, frequent reboosting | Natural |
| **500-600** | Moderate decay (5-15 yrs), good coverage | Moderate risk | Natural or active |
| **600-800** | Long lifetime, good coverage | High debris density, active deorbit required | Active required |
| **>800** | Very long lifetime | Critical debris risk, expensive deorbit | Active required |

**Recommended:** 500-600 km for most applications

---

## Frequency Band Selection

| Band | Frequency | Best For | Challenges |
|------|-----------|----------|------------|
| **L-band** | 1-2 GHz | Mobile, low bandwidth | Crowded, long licensing |
| **S-band** | 2-4 GHz | Weather, moderate data | Some congestion |
| **C-band** | 4-8 GHz | Traditional satellite | Moderate congestion |
| **Ku-band** | 12-18 GHz | High-speed internet | Crowded, rain fade |
| **Ka-band** | 18-40 GHz | Very high-speed | Rain attenuation |

**Recommended:** Ku-band (12-18 GHz) for high-speed data

---

## Sustainability Score Targets

| Score | Grade | Meaning | Actions |
|-------|-------|---------|---------|
| **85-100** | Excellent | Fully compliant, low risk | Maintain standards |
| **70-84** | Good | Minor improvements needed | Review recommendations |
| **55-69** | Acceptable | Significant gaps | Address compliance issues |
| **<55** | Poor | Major problems | Redesign required |

**Target:** >70 for responsible operations

---

## Tab-by-Tab Guide

### Tab 1: Simulation Results
**What to look for:**
- SNR stays above 10 dB
- Coverage >90%
- Low downtime
- Compare ground vs crosslink

### Tab 2: Cost Analysis
**What to look for:**
- Total cost difference
- Tipping point satellite count
- Payback period
- Break-even analysis

### Tab 3: Value Dashboard
**What to look for:**
- Quick metrics comparison
- Performance improvements
- Cost savings percentage
- Infrastructure requirements

### Tab 4: Data Tables
**What to look for:**
- Raw simulation data
- Export for analysis
- Detailed link statistics

### Tab 5: Executive Report
**What to look for:**
- Recommendation (which architecture)
- Key findings summary
- Decision factors
- Technical verification

### Tab 6: Sustainability & Debris
**What to look for:**
- Collision risk level
- FCC compliance status
- Deorbit requirements
- Mitigation costs

### Tab 7: Regulatory Compliance
**What to look for:**
- Licensing costs
- Approval timeline
- Required filings
- Risk assessment

### Tab 8: Business Model
**What to look for:**
- Service tiers
- Revenue projections
- Market opportunity
- Go-to-market strategy

---

## Common Scenarios

### Scenario 1: Earth Observation (10 satellites)
- Altitude: **550 km**
- Frequency: **8 GHz** (X-band)
- Transmit Power: **20 dBW**
- Architecture: **Ground-station-only** (fewer satellites)
- Ground Stations: **5**

### Scenario 2: IoT Connectivity (50 satellites)
- Altitude: **600 km**
- Frequency: **2 GHz** (S-band)
- Transmit Power: **15 dBW**
- Architecture: **Crosslinked** (many satellites)
- Ground Stations: **3**

### Scenario 3: High-Speed Internet (100+ satellites)
- Altitude: **550 km**
- Frequency: **18 GHz** (Ka-band)
- Transmit Power: **25 dBW**
- Architecture: **Crosslinked** (large constellation)
- Ground Stations: **3-5**

### Scenario 4: Scientific Mission (5 satellites)
- Altitude: **500 km**
- Frequency: **8 GHz** (X-band)
- Transmit Power: **20 dBW**
- Architecture: **Ground-station-only** (small fleet)
- Ground Stations: **4**

---

## Red Flags to Watch For

### Technical
- SNR below 10 dB consistently
- Coverage below 80%
- Latency above 1500 ms for ground links
- High downtime (>30 minutes per orbit)

### Sustainability
- Collision risk "High" or "Critical"
- Altitude >700 km without active deorbit
- Sustainability score <55
- Non-compliant with FCC 25-year rule

### Financial
- CapEx >$500M for small constellations
- Payback period >7 years
- Ground stations >10 (consider crosslinks)
- Negative ROI at any scale

### Regulatory
- Approval timeline >24 months
- Frequency band "High" congestion
- Risk level "High"
- Multiple country filings without budget

---

## Optimization Tips

### Reduce Cost
1. Use crosslinks for constellations >20 satellites
2. Minimize ground stations
3. Choose less congested frequency bands
4. Partner for ground infrastructure

### Improve Performance
1. Increase transmit power (within limits)
2. Use higher gain antennas
3. Add more satellites for coverage
4. Lower orbit altitude (better link budget)

### Improve Sustainability
1. Select altitude 500-600 km
2. Add active deorbit system if >600 km
3. Budget for debris tracking
4. Design for demise on reentry

### Accelerate Regulatory
1. Start ITU coordination early
2. Engage regulatory consultants
3. Choose less congested bands
4. Minimize countries served initially

---

## Keyboard Shortcuts & Tips

### Navigation
- Use tabs at top to switch views
- Sidebar on left for parameters
- Run button at bottom of sidebar

### Data Export
- Executive Report: Download as TXT
- Comparison Table: Download as CSV
- Charts: Hover for details (no export yet)

### Simulation Speed
- Simulated data: Fast (<5 seconds)
- NASA TLE data: Slower (loading files)

---

## When to Get Professional Help

### You should hire consultants when:
- Constellation >100 satellites
- Mission-critical application (lives depend on it)
- Budget >$100M
- Regulatory filing preparation
- Detailed engineering needed
- International expansion to >10 countries

### This tool is sufficient for:
- Feasibility studies
- Architecture trade-offs
- Budget estimates
- Early-stage design
- Education and learning
- Benchmarking against competitors

---

## Useful Formulas

### Link Budget
```
SNR (dB) = Transmit Power + Antenna Gains - Path Loss - Atmospheric Loss - System Loss - Noise
```

### Path Loss
```
Path Loss (dB) = 20*log10(distance_km) + 20*log10(frequency_GHz) + 92.45
```

### Tipping Point
```
Tipping Point Satellites = (Ground Stations Saved × $10M) / ($500K per satellite)
```

### Payback Period
```
Payback (years) = CapEx Difference / Annual OpEx Savings
```

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Low SNR | Increase power, lower altitude, or improve antenna gain |
| Poor coverage | Add satellites or ground stations |
| High cost | Use crosslinks for large constellations |
| High collision risk | Lower altitude below 600 km |
| Long regulatory timeline | Choose less congested frequency band |
| Low sustainability score | Add deorbit capability, lower altitude |

---

## Key Takeaways

1. **Cost tipping point matters:** Crosslinks win at scale (typically >20 satellites)
2. **Sustainability is not optional:** Budget for debris mitigation and deorbit
3. **Regulatory takes time:** Plan 12-18 months for approvals
4. **Altitude is critical:** 500-600 km balances performance and sustainability
5. **Ground-station-only has value:** Best for small constellations (<15 satellites)
6. **Real data is valuable:** Benchmark against Starlink, GPS, etc.
7. **Business model matters:** Service economics depend on market positioning

---

## Getting Help

- Read: `COMPREHENSIVE_FEATURES_GUIDE.md` for full details
- Check: `PARAMETER_GUIDE.md` for parameter explanations
- Review: `NASA_DATA_GUIDE.md` for TLE data usage
- Run: `python -m streamlit run main.py` to start simulator

---

**Remember:** This tool helps you make informed decisions. For mission-critical applications, always validate with professional aerospace analysis tools and consultants.

