import pandas as pd
import plotly.express as px


def generateBarChart(data):
    """
    returns HTML div of bar chart of data
    :param data: list of tuples
    """
    data_frame = pd.DataFrame(data, columns=["Word", "Number of Times Used"])
    bar_chart = px.bar(data_frame, x="Word", y="Number of Times Used")
    return bar_chart.to_html(full_html=False)


def generatePieChart(data):
    """
    returns HTML div of pie chart of data
    :param data: list of tuples
    """
    data_frame = pd.DataFrame(data, columns=["Word", "Number of Times Used"])
    pie_chart = px.pie(
        data_frame,
        values="Number of Times Used",
        names="Word",
        title="Top 10 Words Used",
    )
    return pie_chart.to_html(full_html=False)