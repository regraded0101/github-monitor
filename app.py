import pandas as pd
import requests
import json
import plotly_express as px
from flask import Flask

app = Flask(__name__)

@app.route('/')
def get_plotly():
    endpoint = 'https://api.github.com/repos'
    r = requests.get(f'{endpoint}/pandas-dev/pandas/commits')
    content = r.content.decode('utf-8')

    data = json.loads(content)

    commit_dates = [commit["commit"]["author"]["date"] for commit in data]
    commit_dates = pd.to_datetime(commit_dates).date

    commit_data = pd.DataFrame(commit_dates, columns=['commit_date'])
    commit_counts = commit_data.groupby('commit_date').agg({'commit_date': 'count'}).reset_index(names=['temp'])
    commit_counts.columns = ['commit_date', 'count']

    return px.line(data_frame=commit_counts, x='commit_date', y='count', line_shape='spline')

if __name__ == "__main__":
    fig = get_plotly()
    fig.show()