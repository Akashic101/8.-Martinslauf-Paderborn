import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import os

conn = sqlite3.connect('results.db')
cursor = conn.cursor()

cursor.execute('''
SELECT nettoTime, rankTotal, ageGroupShort FROM results_2024
''')

data = cursor.fetchall()

age_groups = [
    "MHK", "M30", "M40", "M35", "M45", "W30", "WHK", "M55", "M50", "MJ U20", 
    "MJ U18", "MJ U16", "W50", "M65", "W35", "W40", "WJ U18", "W60", "M60", 
    "WJ U16", "M70", "W45", "WJ U20", "W65", "W55", "MJ U14", "WJ U14", "M75"
]

age_group_times = {age_group: [] for age_group in age_groups}

def seconds_to_hms(seconds):
    return f"{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}"

for row in data:
    netto_time_str = row[0]
    age_group_short = row[2]
    
    try:
        if age_group_short in age_groups:
            h, m, s = map(int, netto_time_str.split(":"))
            total_seconds = h * 3600 + m * 60 + s
            age_group_times[age_group_short].append(total_seconds)
    except (ValueError, TypeError) as e:
        continue

age_group_data = {age_group: pd.Series(times) for age_group, times in age_group_times.items() if times}

plt.figure(figsize=(20, 8), facecolor='#181a1b')
ax = plt.gca()
ax.set_facecolor('#181a1b')

plt.boxplot(age_group_data.values(), vert=False, patch_artist=True, 
            boxprops=dict(facecolor='#add8e6', color='#d3d3d3'),
            whiskerprops=dict(color='#d3d3d3'),
            capprops=dict(color='#d3d3d3'),
            flierprops=dict(markerfacecolor='r', marker='o', markersize=5))

plt.yticks(range(1, len(age_group_data) + 1), list(age_group_data.keys()), color='white')
plt.xlabel('Netto Time (HH:MM:SS)', color='white')
plt.title('Boxplot of Netto Time by Age Group', color='white')

xticks = ax.get_xticks()
xticklabels = [seconds_to_hms(int(x)) for x in xticks]
plt.xticks(xticks, xticklabels, color='white')

ax.tick_params(axis='y', colors='white')

ax.set_xlim(left=30*60)

for tick in xticks:
    ax.axvline(x=tick, color='#d3d3d3', linestyle=':', linewidth=0.5)

yticks = ax.get_yticks()
for tick in yticks:
    ax.axhline(y=tick, color='#d3d3d3', linestyle=':', linewidth=0.5)

ax.spines['top'].set_color('#181a1b')
ax.spines['bottom'].set_color('#181a1b')
ax.spines['left'].set_color('#181a1b')
ax.spines['right'].set_color('#181a1b')

if not os.path.exists('results'):
    os.makedirs('results')

plt.savefig('results/box_plot.png')
plt.close()

conn.close()
