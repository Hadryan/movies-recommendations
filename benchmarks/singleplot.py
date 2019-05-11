import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def _timeouts(l):
    return sum(1 for i in l if i >= 10)


df1 = pd.read_csv('cherrypy_redis_ratings_10000_high_post.csv')
df1['server'] = 'cheroot'

df2 = pd.read_csv('flask_redis_ratings_10000_high_post.csv')
df2['server'] = 'flask'

df = df1.append(df2)
df = df[df['response-time'] < 10]
ax = sns.boxplot(x='server', y='response-time', data=df, width=1)

medians = df.groupby(['server'])['response-time'].median().values
medians[0] += 0.078
l1 = _timeouts(df1["response-time"])
s1 = df1["response-time"].size
l2 = _timeouts(df2["response-time"])
s2 = df2["response-time"].size
timeouts_labels = [f'timeouts: {l1}/{s1}', f'timeouts: {l2}/{s2}']
pos = range(len(timeouts_labels))
for tick, label in zip(pos, ax.get_xticklabels()):
    ax.text(pos[tick], medians[tick]-0.165, timeouts_labels[tick],
            horizontalalignment='center', size='small', color='black')

plt.title('Redis POST on ratings.\nResponses longer than 10s are considered timeouts.')
plt.ylabel('response time [s]')
plt.show()
