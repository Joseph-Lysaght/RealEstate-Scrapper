from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import mysql.connector
import pandas as pd
import plotly.graph_objs as go
import numpy as np

db_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "seppiesrealestate"
)

cursor = db_connection.cursor()
query = "SELECT * FROM `listings_tbl`"
cursor.execute(query)
results = cursor.fetchall()
cursor.close()

df = pd.DataFrame(results)
df.columns = ['Zillow ID','Address','beds','baths','Square Footage','Date Added']
df['Price'] = None

#For each listing find the latest price
for row in df.itertuples():
    cursor = db_connection.cursor()
    query = "SELECT `dateChanged`,`price` FROM `price_tbl` WHERE `id` = " + str(row._1)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    #extract just the dates changed
    dates = [x[0] for x in results]
    latestprice = results[dates.index(max(dates))][1]
    #Write current price into df
    df.at[row.Index, 'Price'] = latestprice




db_connection.close()

# Create the Dash app
app = Dash(__name__)

# Create scatter plot function using data from the DataFrame
def create_scatter_plot_with_fit(x_col, y_col, title):
    # Extract x and y data from DataFrame
    x = df[x_col]
    y = df[y_col]
    
    # Perform linear regression (best fit line)
    slope, intercept = np.polyfit(x, y, 1)
    fit_line = slope * x + intercept
    
    # Scatter plot trace
    scatter_trace = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(size=8, color='lightblue'),
        name=f'{title} (Data)'
    )
    
    # Best fit line trace
    fit_line_trace = go.Scatter(
        x=x,
        y=fit_line,
        mode='lines',
        line=dict(color='red'),
        name=f'{title} (Best Fit Line)'
    )
    
    return [scatter_trace, fit_line_trace]

# Define the layout of the app
app.layout = html.Div(
    style={'backgroundColor': 'black', 'padding': '20px'},
    children=[
        html.H1("Scatter Plots with Best Fit Line from Pandas DataFrame", style={'color': 'white', 'textAlign': 'center'}),

        # Row 1 with 2 scatter plots and best fit lines
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-between'},
            children=[
                dcc.Graph(
                    id='scatter-plot-1',
                    figure={
                        'data': create_scatter_plot_with_fit("beds", "baths", "Plot 1: Beds vs Baths"),
                        'layout': go.Layout(
                            title="Scatter Plot 1: Beds vs Baths",
                            plot_bgcolor='black',
                            paper_bgcolor='black',
                            font={'color': 'white'}
                        )
                    },
                    style={'width': '48%'}
                ),
                dcc.Graph(
                    id='scatter-plot-2',
                    figure={
                        'data': create_scatter_plot_with_fit("Square Footage", "Price", "Plot 2: Square Footage vs Price"),
                        'layout': go.Layout(
                            title="Scatter Plot 2: Square Footage vs Price",
                            plot_bgcolor='black',
                            paper_bgcolor='black',
                            font={'color': 'white'}
                        )
                    },
                    style={'width': '48%'}
                )
            ]
        ),

        # Row 2 with 2 scatter plots and best fit lines
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-between', 'marginTop': '20px'},
            children=[
                dcc.Graph(
                    id='scatter-plot-3',
                    figure={
                        'data': create_scatter_plot_with_fit("beds", "Square Footage", "Plot 3: Beds vs Square Footage"),
                        'layout': go.Layout(
                            title="Scatter Plot 3: Beds vs Square Footage",
                            plot_bgcolor='black',
                            paper_bgcolor='black',
                            font={'color': 'white'}
                        )
                    },
                    style={'width': '48%'}
                ),
                dcc.Graph(
                    id='scatter-plot-4',
                    figure={
                        'data': create_scatter_plot_with_fit("baths", "Price", "Plot 4: Baths vs Price"),
                        'layout': go.Layout(
                            title="Scatter Plot 4: Baths vs Price",
                            plot_bgcolor='black',
                            paper_bgcolor='black',
                            font={'color': 'white'}
                        )
                    },
                    style={'width': '48%'}
                )
            ]
        ),
    ]
)

if __name__ == '__main__':
    app.run(debug=False)
