import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

covid_paper_df = pd.read_csv('covid-19_research.csv')
covid_paper_df.set_index("Date", inplace=True)

new_df = pd.DataFrame(index=covid_paper_df.index.drop_duplicates(keep='first'))

new_df['count']=pd.Series(covid_paper_df['Title'].groupby(covid_paper_df.index).count())
new_df.sort_index(inplace=True)


abstract_unc_df = pd.read_csv("Articles_and_uncertainty.csv")
to_plot_data = abstract_unc_df[["Date", "Uncertainty"]].groupby("Date").mean()


mortality_df = pd.read_csv("COVID-19_Impact/Mortality_rates.csv")
mortality_df.set_index("Country/Region", inplace=True)
countries_list = list(mortality_df.index)

recovery_df = pd.read_csv("COVID-19_Impact/Rec_rates.csv")
recovery_df.set_index("Country/Region", inplace=True)


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
					    html.Div([
					        html.Div([
					            html.H3('Research Papers Published during Corona Period'),
								dcc.Graph(
									id = "papers_per_day",
									figure={
											'data':[
											
											{'x': new_df.index , 'y': new_df['count'], 'type': 'bar', 'name': "Count of paper published"},
											],
									
											'layout':{
											'title': 'Papers published on COVID-19',
											'xaxis': {'title': "Months ------------>"},
											'yaxis': {'title': "Number of papers published"}
											}
											
											})
        							]),
					        ]),
					    html.Div([
					        html.Div([
					            html.H3('Uncertainty expressed in Research Papers Published during Corona Period'),
								dcc.Graph(
									id = "uncertainty",
									figure={
											'data':[
											
											{'x': to_plot_data.index , 'y': to_plot_data['Uncertainty'][2:], 'type': 'line', 'name': "Uncertainty in Papers"},
											],
									
											'layout':{
											'title': 'Uncertainty expressed in Research Papers',
											'xaxis': {'title': "Time"},
											# 'xaxis_tickformat' :'%d %B (%a)<br>%Y',
											'yaxis': {'title': "Percentage of uncertainty"}
											}
											
											})
        							]),
					        ]),

        html.Div([
	        dcc.Dropdown(
	            id='xaxis-dropdown',
	            options=[{'label':country_name, 'value':country_name} for country_name in countries_list],
	            value = countries_list[0],
	            clearable = False
	            ),
	            ],style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
        	dcc.RadioItems(
        		id = 'xaxis-type',
        		options = [{'label': rate_type, 'value': rate_type} for rate_type in ['Mortality Rate', 'Recovery Rate']],
        		value = "Mortality Rate"
        		)
        	]),

        
        html.Div(id='output-graph')

], style={'font-family': "Comic Sans MS"})

@app.callback(
	Output(component_id='output-graph', component_property='children'),
	[Input(component_id='xaxis-dropdown', component_property='value'),
	Input(component_id='xaxis-type', component_property='value'),
	]
	)
def update_graph(xaxis_dropdown, xaxis_type):
	if xaxis_type==None:
		return html.H3("Choose a value",style={'text-align':"center"})
	elif xaxis_type == "Mortality Rate":
		return dcc.Graph(
				id = "Mortality_rates",
				figure={
						'data':[
						{'x': mortality_df.columns[2:-1] , 'y': mortality_df.loc[xaxis_dropdown].values, 'type': 'bar', 'name': mortality_df.loc[xaxis_dropdown]},					
						
						],
				
						'layout':{
						'title': 'Mortality_rates on COVID-19',
						'xaxis': {'title': "Months ------------>"},
						'yaxis': {'title': "Mortality_rates"}
						}
						
				})
	elif xaxis_type == "Recovery Rate":
		return dcc.Graph(
				id = "Recovery rates",
				figure={
						'data':[
						{'x': recovery_df.columns[2:-1] , 'y': recovery_df.loc[xaxis_dropdown].values, 'type': 'bar', 'name': recovery_df.loc[xaxis_dropdown]},
						
						],
				
						'layout':{
						'title': 'Recovery rates on COVID-19',
						'xaxis': {'title': "Months ------------>"},
						'yaxis': {'title': "Recovery rates"}
						}
						
				})

	


if __name__ == "__main__":
	app.run_server(debug=True)