import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

conn = sqlite3.connect('results.db')
cursor = conn.cursor()

cursor.execute('''
SELECT ageGroupShort FROM results
''')

data = cursor.fetchall()

age_groups_men = [
    "MHK", "M30", "M35", "M40", "M45", "M50", "M55", "M60", "M65", "M70", "M75",
    "MJ U20", "MJ U18", "MJ U16", "MJ U14"
]

age_groups_women = [
    "WHK", "W30", "W35", "W40", "W45", "W50", "W55", "W60", "W65",
    "WJ U20", "WJ U18", "WJ U16", "WJ U14"
]

male_counts = {age_group: 0 for age_group in age_groups_men}
female_counts = {age_group: 0 for age_group in age_groups_women}

for row in data:
    age_group = row[0]
    if age_group in male_counts:
        male_counts[age_group] += 1
    elif age_group in female_counts:
        female_counts[age_group] += 1

def plot_circular_bar_chart(counts, title, filename):
    # Sort counts by value in descending order
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    labels = [item[0] for item in sorted_counts]
    values = [item[1] for item in sorted_counts]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'}, facecolor='#181a1b')
    ax.set_facecolor('#181a1b')
    
    num_labels = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_labels, endpoint=False)
    angles += np.pi / num_labels

    min_height = 5
    adjusted_values = [np.log(value + 1) * 10 if value > 0 else min_height for value in values]

    bars = ax.bar(angles, adjusted_values, width=2 * np.pi / num_labels, color='#add8e6', edgecolor='#d3d3d3', linewidth=1, alpha=0.7)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color='white')
    ax.set_title(title, color='white', pad=20)
    
    for angle, value, original_value in zip(angles, adjusted_values, values):
        display_value = str(original_value) if original_value > 0 else ""
        ax.text(angle, value + 1, display_value, ha='center', va='bottom', color='white')
    
    if not os.path.exists('results'):
        os.makedirs('results')
    
    plt.savefig(f'results/{filename}.png', facecolor='#181a1b')
    plt.close()

plot_circular_bar_chart(male_counts, 'Participants by Age Group (Men)', 'circular_bar_men')
plot_circular_bar_chart(female_counts, 'Participants by Age Group (Women)', 'circular_bar_women')

conn.close()
