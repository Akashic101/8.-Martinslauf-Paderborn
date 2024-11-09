import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

conn = sqlite3.connect('results.db')
cursor = conn.cursor()

cursor.execute('''
SELECT ageGroupShort, COUNT(*) 
FROM results_2023 
GROUP BY ageGroupShort;
''')
data_2023 = cursor.fetchall()

cursor.execute('''
SELECT ageGroupShort, COUNT(*) 
FROM results_2024 
GROUP BY ageGroupShort;
''')
data_2024 = cursor.fetchall()

total_2023 = sum(row[1] for row in data_2023)
total_2024 = sum(row[1] for row in data_2024)

age_groups_2023 = {row[0]: row[1] for row in data_2023}
age_groups_2024 = {row[0]: row[1] for row in data_2024}

age_groups = [
    'MHK', 'M30', 'M40', 'M35', 'M45', 'W30', 'WHK', 'M55', 'M50',
    'MJ U20', 'MJ U18', 'MJ U16', 'W50', 'M65', 'W35', 'W40', 'WJ U18',
    'W60', 'M60', 'WJ U16', 'M70', 'W45', 'WJ U20', 'W65', 'W55', 
    'MJ U14', 'WJ U14', 'M75'
]

counts_2023 = [age_groups_2023.get(group, 0) for group in age_groups]
counts_2024 = [age_groups_2024.get(group, 0) for group in age_groups]

differences = [c_2024 - c_2023 for c_2024, c_2023 in zip(counts_2024, counts_2023)]

combined_data = list(zip(age_groups, counts_2023, counts_2024, differences))

sorted_data = sorted(combined_data, key=lambda x: x[2], reverse=True)

sorted_age_groups, sorted_counts_2023, sorted_counts_2024, sorted_differences = zip(*sorted_data)

fig, ax = plt.subplots(figsize=(15, 20))
ax.set_facecolor('#181a1b')

y_pos = np.arange(len(sorted_age_groups))

ax.barh(y_pos, -np.array(sorted_counts_2023), color='#add8e6', edgecolor='#181a1b', height=0.8, label='2023 Runners')
ax.barh(y_pos, np.array(sorted_counts_2024), color='#ff7f0e', edgecolor='#181a1b', height=0.8, label='2024 Runners')

ax.set_yticks(y_pos)
ax.set_yticklabels(sorted_age_groups, color='white')

ax.set_xlabel('Number of Runners', color='white')
ax.set_title(f'Population Pyramid: Runners by Age Group (2023 vs 2024)\nTotal Runners: 2023 = {total_2023}, 2024 = {total_2024}', color='white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax.axvline(x=0, color='white', linewidth=1)

ax.grid(axis='x', linestyle='--', color='grey', alpha=0.2)

for tick in ax.get_yticks():
    ax.axhline(y=tick, color='grey', linestyle=':', linewidth=0.5)

for i, diff in enumerate(sorted_differences):
    color = 'green' if diff > 0 else 'red'
    ax.text(sorted_counts_2024[i] + 2, y_pos[i], f'+{diff}' if diff > 0 else f'{diff}', 
            color=color, va='center', fontsize=10)

ax.set_xticklabels([abs(int(tick)) for tick in ax.get_xticks()])

fig.patch.set_facecolor('#181a1b')

if not os.path.exists('results'):
    os.makedirs('results')

plt.savefig('results/population_pyramid.png', facecolor='#181a1b')
plt.close()

conn.close()
