import datetime
import plotly.graph_objects as go
import numpy as np

def plotGen(Title,Data1,Label1,Data2=None,Label2=None,ts=None,Yaxis=None):
    # Generate datetime list at 15-min intervals
    start_datetime = datetime.datetime(2025, 1, 1, 0, 0)
    date_list = [start_datetime + datetime.timedelta(minutes=15 * t) for t in range(ts)]

    # Determine the time span
    total_days = (date_list[-1] - date_list[0]).days

    # Set tick format and interval dynamically
    if total_days <= 1:
        # Show hours for 1 day
        tickformat = "%H:%M"
        dtick = 3600000 * 2  # every 2 hours
    elif total_days <= 31:
        # Show days for up to a month
        tickformat = "%d %b"
        dtick = "D1"
    elif total_days <= 366:
        # Show months for up to a year
        tickformat = "%b"
        dtick = "M1"
    else:
        # Show years if longer
        tickformat = "%Y"
        dtick = "M3"

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=date_list,
        y=Data1,
        mode='lines',
        name=Label1,
        line=dict(color='#85c069', width=2)
    ))

    if Data2 is not None and Label2 is not None:
        fig.add_trace(go.Scatter(
            x=date_list,
            y=Data2,
            mode='lines',
            name=Label2,
            line=dict(color='#00b8c8', width=2)
    ))

    fig.update_layout(
        title=Title,
        xaxis_title='Time',
        yaxis_title=Yaxis,
        xaxis=dict(
            tickformat=tickformat,
            dtick=dtick,
            tickangle=0,
        ),
        hovermode='x',
        template='plotly_white',
        width=1000,
        height=500
    )

    if Data2 is not None and Label2 is not None:
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
        )
)

    return fig

def save(name,data,fig,saveDir):
    np.savetxt(f"{saveDir}{name}.csv",data, delimiter=";")
    fig.write_html(f"{saveDir}{name}_plot.html")
    fig.write_image(f"{saveDir}{name}_plot.png", scale=4)  
    fig.write_image(f"{saveDir}{name}_plot.svg")