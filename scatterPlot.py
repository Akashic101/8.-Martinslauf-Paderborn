import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

conn = sqlite3.connect('results.db')
cursor = conn.cursor()

cursor.execute('''
SELECT nettoTime, rankTotal FROM results
''')

data = cursor.fetchall()

times_in_seconds = []
ranks = []

for row in data:
    netto_time_str = row[0]
    rank_total_str = row[1]
    
    try:
        rank_total_str = rank_total_str.strip('.')
        h, m, s = map(int, netto_time_str.split(":"))
        total_seconds = h * 3600 + m * 60 + s
        rank_total = int(rank_total_str)
        times_in_seconds.append(total_seconds)
        ranks.append(rank_total)
    except (ValueError, TypeError) as e:
        continue

if times_in_seconds and ranks:
    plt.figure(figsize=(20, 8), facecolor='#181a1b')
    ax = plt.gca()
    ax.set_facecolor('#181a1b')

    plt.scatter(ranks, times_in_seconds, alpha=0.6, edgecolors="w", linewidth=0.5, color="#add8e6", s=10)

    plt.xlabel('Rank Total', color='white')
    plt.ylabel('Netto Time (HH:MM:SS)', color='white')
    plt.title('Scatter Plot of Rank Total vs. Netto Time', color='white')

    def seconds_to_hms(seconds):
        return f"{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}"

    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: seconds_to_hms(int(x))))

    if ranks:
        rank_labels = range(0, max(ranks), 50)
        for label in rank_labels:
            plt.axvline(x=label, color='#d3d3d3', linestyle=':', linewidth=0.5)

        plt.xticks(rank_labels, color='white')

    time_intervals = [30 * 60 + 5 * 60 * i for i in range(0, 13)]
    for time_interval in time_intervals:
        plt.axhline(y=time_interval, color='#d3d3d3', linestyle=':', linewidth=0.5)

    plt.yticks(time_intervals, [seconds_to_hms(t) for t in time_intervals], color='white')

    ax.spines['top'].set_color('#181a1b')
    ax.spines['bottom'].set_color('#181a1b')
    ax.spines['left'].set_color('#181a1b')
    ax.spines['right'].set_color('#181a1b')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    if not os.path.exists('results'):
        os.makedirs('results')

    plt.savefig('results/scatter_plot.png')
else:
    print("No valid data available for plotting.")

conn.close()
