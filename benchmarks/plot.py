import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def _timeouts(l):
    return sum(1 for i in l if i >= 10)


df1 = pd.read_csv('cherrypy_redis_ratings_10000_high_json.csv')
df1['server'] = 'cheroot'
df1['workload'] = 'high'

df11 = pd.read_csv('cherrypy_redis_ratings_10000_low_json.csv')
df11['server'] = 'cheroot'
df11['workload'] = 'low'

df2 = pd.read_csv('flask_redis_ratings_10000_high_json.csv')
df2['server'] = 'flask'
df2['workload'] = 'high'

df22 = pd.read_csv('flask_redis_ratings_10000_low_json.csv')
df22['server'] = 'flask'
df22['workload'] = 'low'

df = df1.append(df11).append(df2).append(df22)
df = df[df['response-time'] < 10]
ax = sns.boxplot(x='server', y='response-time', hue='workload', data=df, width=1)

medians = df.groupby(['server'])['response-time'].median().values
medians[0] += 0.0
l1 = _timeouts(df1["response-time"]) + _timeouts(df11["response-time"])
s1 = df1["response-time"].size + df11["response-time"].size
l2 = _timeouts(df2["response-time"]) + _timeouts(df22["response-time"])
s2 = df2["response-time"].size + df22["response-time"].size
timeouts_labels = [f'timeouts: {l1}/{s1}', f'timeouts: {l2}/{s2}']
pos = range(len(timeouts_labels))
for tick, label in zip(pos, ax.get_xticklabels()):
    ax.text(pos[tick], medians[tick] - 2, timeouts_labels[tick],
            horizontalalignment='center', size='small', color='black')

plt.title('Redis ratings without json.loads().\nResponses longer than 10s are considered timeouts.')
plt.ylabel('response time [s]')
plt.show()
