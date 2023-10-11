import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np


def annotate_calibrations(dataset, fig):
    cals = dataset.cals
    for i in range(cals["n"]):
        fig.add_annotation(
            x=cals["ts"][i], y=cals["glucose"][i] + .2, text="Calibration",
            showarrow=True, arrowhead=1, arrowsize=1,
        )


def annotate_food_intakes(dataset, fig):
    food = dataset.food
    for i in range(food["n"]):
        fig.add_annotation(
            x=food["ts"][i], y=food["glucose"][i], text=f"{food['carbs'][i]}g",
            showarrow=False
        )


def get_cgm_figure(dataset):

    # variables
    glucose = dataset.glucose
    food = dataset.food
    bolus = dataset.bolus
    basal = dataset.basal

    # figure settings
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, row_heights=[.75, .25], vertical_spacing=0
    )

    # continuous glucose monitoring data
    fig.add_trace(
        go.Scatter(x=glucose["ts"], y=glucose["values"], name="Glucose value"),
        row=1, col=1
    )
    # carbohydrates intakes
    fig.add_trace(
        go.Scatter(x=food["ts"], y=food["glucose"], text=food["carbs"],
                   mode="markers", name="Carbohydrates intake",
                   marker=dict(
                       color="Khaki", size=food["marker"],
                   )),
        row=1, col=1
    )
    # bolus treatments
    fig.add_trace(
        go.Scatter(x=bolus["ts"], y=np.zeros_like(bolus["values"]) + 1.5, text=bolus["values"],
                   mode="markers", name="Insulin Bolus",
                   marker=dict(
                       color="LightCoral", size=bolus["marker"]
                   )),
        row=1, col=1
    )
    # temp basal treatments
    fig.add_trace(
        go.Scatter(x=basal["ts"], y=basal["values"],
                   name="Insulin Basal", fill="tozeroy", fillcolor="#F3C1C1",
                   line=dict(
                       shape="hvh", color="LightCoral"
                   )),
        row=2, col=1
    )

    # add annotations
    annotate_calibrations(dataset, fig)
    annotate_food_intakes(dataset, fig)

    # range slider
    fig.update_layout(
        # add range slider buttons
        xaxis=dict(
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1 hour", step="hour", stepmode="backward"),
                    dict(count=3, label="3 hours", step="hour", stepmode="backward"),
                    dict(count=6, label="6 hours", step="hour", stepmode="backward"),
                    dict(count=12, label="12 hours", step="hour", stepmode="backward"),
                    dict(count=24, label="24 hours", step="hour", stepmode="backward"),
                ]
            ),
        ),
        # add range slider
        xaxis2=dict(
            rangeslider=dict(visible=True),
            type="date",
            title=dict(text="Time range selector")
        ),
        # set the range for both axes
        yaxis=dict(
            range=[0, glucose["max"]],
            tickvals=list(range(5, 25, 5)),
            title=dict(text="Glucose, <i>mmol/L</i>")
        ),
        yaxis2=dict(
            range=[0, basal["max"] + .25],
            tickvals=np.arange(.5, basal["max"] + .5),
            title=dict(text="Insulin")
        ),
        height=700
    )

    return fig
