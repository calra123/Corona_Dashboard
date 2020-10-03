import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

covid_paper_df = pd.read_csv('covid-19_research.csv')
covid_paper_df.set_index("Date", inplace=True)

new_df = pd.DataFrame(index=covid_paper_df.index.drop_duplicates(keep='first'))

new_df['count']=pd.Series(covid_paper_df['Title'].groupby(covid_paper_df.index).count())
new_df.sort_index(inplace=True)


app = dash.Dash(__name__)

app.layout = html.Div(children=[
								html.H1("Welcome to Research on COVID-19 Dashboard", style={'text-align': "center"}),
								dcc.Graph(
									id = "papers_per_day",
									figure={
											'data':[
											{'x': new_df.index , 'y': new_df['count'], 'type': 'bar', 'name': "Count of papers published"},
											{'x': new_df.index , 'y': new_df['count'], 'type': 'line', 'name': "Count of paper published"},
											],
									
											'layout':{
											'title': 'Papers published on COVID-19',
											'xaxis': {'title': "Months ------------>"},
											'yaxis': {'title': "Number of papers published"}
											}
											
									})
									

								])

if __name__ == "__main__":
	app.run_server(debug=True)