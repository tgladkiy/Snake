import sys
import pandas as pd
import matplotlib.pyplot as plt

try:
    var = sys.argv[1]
except IndexError:
    var = ''

plt.style.use('seaborn-whitegrid')

file_name = "snake_statistics_" + str(var) + ".csv"
data = pd.read_csv(file_name)
data = data.query('time_label == @var')

smooth_rolling = 3
pt_mean = data.pivot_table(index='family', columns='epoch', values='score', aggfunc='max').T

fig, ax = plt.subplots()
fig.set_size_inches(7, 3.5)
fig.set_facecolor('#F5F5F5')
ax.set_facecolor('#F5F5F5')

ax.plot(pt_mean.rolling(smooth_rolling).mean(), label=pt_mean.columns)

ax.set_title('Score for TOP-1 snakes                       (smooth rolling: 3 epochs)', fontsize=12)
ax.set_ylabel('Score', fontsize=12)
ax.set_xlabel("Epochs", fontsize=12)
ax.set_xlim(0,100)
ax.set_ylim(0)
if len(pt_mean.count()) > 1: fig.legend(title='Family', loc='right', fontsize=7)

fig.savefig("snake_plot.png", dpi=100)
