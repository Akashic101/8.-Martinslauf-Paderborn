import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

conn = sqlite3.connect('results.db')
cursor = conn.cursor()

cursor.execute('''
SELECT firstName, lastName, nettoTime
FROM results_2023
WHERE (firstName, lastName) IN (SELECT firstName, lastName FROM results_2024);
''')
data_2023 = cursor.fetchall()

cursor.execute('''
SELECT firstName, lastName, nettoTime
FROM results_2024
WHERE (firstName, lastName) IN (SELECT firstName, lastName FROM results_2023);
''')
data_2024 = cursor.fetchall()

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(":"))
    return h * 3600 + m * 60 + s

def seconds_to_hms(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def seconds_to_mmss(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{m:02}:{s:02}"

times_2023 = {}
times_2024 = {}
names = []

for row in data_2023:
    name = f"{row[0]} {row[1]}"
    netto_time = row[2]
    times_2023[name] = time_to_seconds(netto_time)

for row in data_2024:
    name = f"{row[0]} {row[1]}"
    netto_time = row[2]
    times_2024[name] = time_to_seconds(netto_time)

runners = []
time_diff = []
time_2023_list = []
time_2024_list = []

for name in times_2023:
    if name in times_2024:
        runners.append(name)
        time_2023_list.append(times_2023[name])
        time_2024_list.append(times_2024[name])
        time_diff.append(times_2023[name] - times_2024[name])

sorted_indices = np.argsort(time_diff)[::-1]
sorted_runners = [runners[i] for i in sorted_indices]
sorted_time_2023 = [time_2023_list[i] for i in sorted_indices]
sorted_time_2024 = [time_2024_list[i] for i in sorted_indices]
sorted_time_diff = [time_diff[i] for i in sorted_indices]

fig, ax = plt.subplots(figsize=(25, 10))

bar_width = 0.35
index = np.arange(len(sorted_runners))

bar1 = ax.bar(index, sorted_time_2023, bar_width, label='2023', color='#add8e6')
bar2 = ax.bar(index + bar_width, sorted_time_2024, bar_width, label='2024', color='#ff7f0e')

ax.set_xlabel('Runners', color='white')
ax.set_ylabel('Netto Time (HH:MM:SS)', color='white')
ax.set_title('Comparison of Runners Time: 2023 vs 2024', color='white')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(sorted_runners, rotation=90, color='white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

yticks = np.arange(0, max(max(sorted_time_2023), max(sorted_time_2024)), 3600)
ax.set_yticks(yticks)
ax.set_yticklabels([seconds_to_hms(int(tick)) for tick in yticks])

ax.legend()

for i in range(len(sorted_runners)):
    diff_str = seconds_to_mmss(abs(sorted_time_diff[i])) if abs(sorted_time_diff[i]) > 60 else str(abs(sorted_time_diff[i])) 
    if sorted_time_diff[i] > 0:
        diff_str = '-' + diff_str
    ax.text(index[i] + bar_width, max(sorted_time_2023[i], sorted_time_2024[i]), 
            f'{diff_str}', color='white', ha='center', va='bottom', fontsize=8, rotation=45)

fig.patch.set_facecolor('#181a1b')
ax.set_facecolor('#181a1b')

ax.grid(axis='y', linestyle='--', color='grey', alpha=0.2)

if not os.path.exists('results'):
    os.makedirs('results')

plt.tight_layout()
plt.savefig('results/grouped_bar_time_comparison.png', facecolor='#181a1b')
plt.close()

conn.close()
