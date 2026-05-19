# Lifeguard Scheduling & Analytics Tool

Python-based analytics system using sample pool sign-in data to model how attendance logs can support staffing decisions.

## Overview

This project parses operational log data from a paper-based sign-in system and converts it into structured insights. The system estimates total pool occupancy, identifies peak usage patterns, and recommends lifeguard staffing levels.

## Features

- Parses sample log data (day | time | name | guest count)
- Estimates total swimmers from incomplete data (member + guests)
- Identifies busiest days and hours
- Ranks all days by total attendance
- Recommends lifeguard staffing levels using configurable safety ratios
- Detects anomalies (unusual spikes in attendance) using threshold-based logic

## Example Output

```
================================================
      POOL ANALYTICS SUMMARY
================================================

Safety policy          : 1 guard per 20 swimmers
Entries processed      : 55
Entries skipped        : 0
Total estimated swimmers: 169
Average per day        : 24.14

--- Daily Breakdown (Ranked) ---
  Saturday : 51 swimmers
  Sunday : 34 swimmers
  Friday : 20 swimmers

--- Anomaly Detection ---
Baseline average: 24.14 swimmers/day

 [HIGH]      Saturday -> 51 swimmers (2x above average)

--- Staffing Recommendation ---
Recommended guards for peak day: 3
```

## Technical Concepts

- File I/O and log parsing
- Data aggregation using dictionaries
- Time-based analysis (day + hour grouping)
- Basic anomaly detection
- Configurable system parameters

## Real-World Context

This project is based on a real lifeguard operations problem, but the public version uses sample data only. It models how manually recorded attendance logs can be converted into useful staffing insights.

## Future Improvements

- CSV-based data ingestion
- Visualization of attendance trends
- Per-hour staffing recommendations
- Advanced anomaly detection

## How to Run

1. Upload `logs.txt` to your environment
2. Run `main.py`
3. View analytics output in the console

## Author

Dante Fanelli — West Valley College, Computer Science  
Planned Transfer: San José State University, Fall 2027
