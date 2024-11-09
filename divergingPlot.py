import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

conn = sqlite3.connect('results.db')
cursor = conn.cursor()

cursor.execute('''
SELECT 
    teamName,
    COUNT(*) AS runnerCount,
    COUNT(CASE WHEN rankMale IS NOT NULL THEN 1 END) AS maleCount,
    COUNT(CASE WHEN rankFemale IS NOT NULL THEN 1 END) AS femaleCount
FROM 
    results_2024
WHERE 
    teamName != ''
GROUP BY 
    teamName
ORDER BY 
    runnerCount DESC, maleCount DESC;
''')

data = cursor.fetchall()

team_names = []
male_counts = []
female_counts = []

for row in data:
    team_names.append(row[0])
    male_counts.append(row[2])
    female_counts.append(row[3])

fig, ax = plt.subplots(figsize=(20, 30))

ax.set_facecolor('#181a1b')

y_pos = np.arange(len(team_names))

ax.barh(y_pos, -np.array(male_counts), color='#add8e6', edgecolor='#181a1b', height=1, label='Male Runners')
ax.barh(y_pos, np.array(female_counts), color='#ff7f0e', edgecolor='#181a1b', height=1, label='Female Runners')

ax.set_yticks(y_pos)
ax.set_yticklabels(team_names, color='white')

ax.set_xlabel('Number of Runners', color='white')
ax.set_title('Team Composition: Male vs Female Runners', color='white')

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.grid(axis='x', linestyle='--', color='grey', alpha=0.2)

ax.axvline(x=0, color='white', linewidth=1)

max_runners = max(max(male_counts), max(female_counts)) + 1
ax.set_xticks(np.arange(-max_runners, max_runners + 1, 1))

xticks = ax.get_xticks()
ax.set_xticklabels([abs(int(tick)) for tick in xticks], color='white')

for tick in ax.get_xticks():
    ax.axvline(x=tick, color='grey', linestyle=':', linewidth=0.5)

for tick in ax.get_yticks():
    ax.axhline(y=tick, color='grey', linestyle=':', linewidth=0.5)

# Rotate the y-axis labels to avoid overlap
ax.set_yticklabels(team_names, color='white', rotation=0, ha='right')

ax.legend(loc='upper right', frameon=False, fontsize=12, labelcolor='white')

if not os.path.exists('results'):
    os.makedirs('results')

plt.savefig('results/diverging_plot_teams.png', facecolor='#181a1b')
plt.close()

conn.close()
