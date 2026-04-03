# ============================================================
# Lifeguard Analytics Tool
# Almaden Golf & Country Club — Pool Operations
# Dante Fanelli | 2026
# ============================================================
# Reads pool sign-in logs and analyzes:
#   - Total estimated swimmers per day
#   - Busiest day and hour
#   - Peak hour per day
#   - Average daily attendance
#   - Anomaly detection for unusual traffic spikes
#   - Recommended lifeguard coverage
#
# Log format: day | time | member_name | guest_count
# Example:    Saturday | 1:00 PM | John Smith | 3
# ============================================================

# --- Configurable safety policy ---
SWIMMERS_PER_GUARD = 20  # adjust based on pool safety requirements

day_totals = {}
hour_totals = {}
hours_by_day = {}
total_people_all = 0
entry_count = 0
skipped = 0

with open("/content/logs.txt") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        parts = line.split("|")

        if len(parts) != 4:
            skipped = skipped + 1
            continue

        day = parts[0].strip()
        time = parts[1].strip()
        name = parts[2].strip()

        try:
            guests = int(parts[3].strip())
        except:
            guests = 0

        total_people = 1 + guests
        total_people_all = total_people_all + total_people
        entry_count = entry_count + 1

        # --- Day totals ---
        if day in day_totals:
            day_totals[day] = day_totals[day] + total_people
        else:
            day_totals[day] = total_people

        # --- Hour parsing (safer split) ---
        try:
            parts_time = time.split()
            hour_raw = parts_time[0].split(":")[0]
            period = parts_time[1]
            hour = hour_raw + " " + period
        except:
            hour = "Unknown"

        # --- Overall hour totals ---
        if hour in hour_totals:
            hour_totals[hour] = hour_totals[hour] + total_people
        else:
            hour_totals[hour] = total_people

        # --- Hour totals by day ---
        if day not in hours_by_day:
            hours_by_day[day] = {}

        if hour in hours_by_day[day]:
            hours_by_day[day][hour] = hours_by_day[day][hour] + total_people
        else:
            hours_by_day[day][hour] = total_people

# --- Find busiest day ---
max_day = ""
max_day_value = 0

for day in day_totals:
    if day_totals[day] > max_day_value:
        max_day_value = day_totals[day]
        max_day = day

# --- Find busiest hour overall ---
max_hour = ""
max_hour_value = 0

for hour in hour_totals:
    if hour_totals[hour] > max_hour_value:
        max_hour_value = hour_totals[hour]
        max_hour = hour

# --- Staffing recommendation ---
recommended_guards = max_day_value // SWIMMERS_PER_GUARD + 1

# --- Average daily attendance ---
avg_per_day = total_people_all / len(day_totals)

# --- Output ---
print("=" * 48)
print("      POOL ANALYTICS SUMMARY")
print("=" * 48)
print()
print("Safety policy          : 1 guard per", SWIMMERS_PER_GUARD, "swimmers")
print("Entries processed      :", entry_count)
print("Entries skipped        :", skipped)
print("Total estimated swimmers:", total_people_all)
print("Average per day        :", round(avg_per_day, 2))
print()

print("--- Daily Breakdown (Ranked) ---")
sorted_days = sorted(day_totals.items(), key=lambda x: x[1], reverse=True)
for day, count in sorted_days:
    print(" ", day, ":", count, "swimmers")

print()
print("--- Peak Hour Per Day ---")
for day, hours in hours_by_day.items():
    peak_hour = ""
    peak_val = 0
    for hour in hours:
        if hours[hour] > peak_val:
            peak_val = hours[hour]
            peak_hour = hour
    print(" ", day, "-> peak at", peak_hour, "(", peak_val, "swimmers)")

print()
print("--- Overall Peak Analysis ---")
print("Busiest Day  :", max_day, "->", max_day_value, "swimmers")
print("Busiest Hour :", max_hour, "->", max_hour_value, "swimmers")
print()

# --- Anomaly Detection ---
print("--- Anomaly Detection ---")
print("Baseline average:", round(avg_per_day, 2), "swimmers/day")
print()

flagged = False
for day in day_totals:
    count = day_totals[day]
    if count > avg_per_day * 2:
        print(" [HIGH]     ", day, "->", count, "swimmers (2x above average)")
        flagged = True
    elif count > avg_per_day * 1.5:
        print(" [MODERATE] ", day, "->", count, "swimmers (1.5x above average)")
        flagged = True

if not flagged:
    print("  No anomalies detected this period.")

print()
print("--- Staffing Recommendation ---")
print("Recommended guards for peak day:", recommended_guards)
print()
print("=" * 48)
