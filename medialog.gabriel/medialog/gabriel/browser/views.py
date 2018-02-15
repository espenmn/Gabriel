from zope.interface import implements, Interface
#, Attribute
from Products.Five import BrowserView
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.browser.view import DefaultView

import json
import urllib

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np

import datetime

class YearGraphView(DefaultView, BrowserView):
    """default view for yeargraph content type"""

    def plotly_html(self):
        """construct a javascript to show the histogram"""

        context = self.context

        #today we will show yesterdays graph
        yesterday = datetime.date.today() - datetime.timedelta(1)

        if context.dato != yesterday or context.debug_mode:
            #history_graph_id = 'history-graph-' + context.id
            graph_url = context.history_graph_url

            colorscale= context.colorscale

            if colorscale == 'Egen1':
                colorscale = [[0, 'rgb(166,206,227)'],
                              [0.25, 'rgb(31,120,180)'],
                              [0.45, 'rgb(178,223,138)'],
                              [0.65, 'rgb(51,160,44)'],
                              [0.85, 'rgb(251,154,153)'],
                              [1, 'rgb(227,26,28)']]

            if colorscale == 'Egen2':
                colorscale = [[0, 'rgb(255,204,255)'],
                              [0.20, 'rgb(255,102,255)'],
                              [0.35, 'rgb(102,02,255)'],
                              [0.55, 'rgb(153,255,153)'],
                              [0.75, 'rgb(255,255,102)'],
                              [0.85, 'rgb(255,51,51)'],
                              [1, 'rgb(227,26,28)']]

            if colorscale == 'Egen3':
                colorscale = [[0, 'rgb(255,204,255)'],
                              [0.05, 'rgb(255,102,255)'],
                              [0.10, 'rgb(102,02,255)'],
                              [0.15, 'rgb(153,255,153)'],
                              [0.25, 'rgb(255,255,102)'],
                              [0.50, 'rgb(255,51,51)'],
                              [1, 'rgb(227,26,28)']]


            f = urllib.urlopen(graph_url)
            jsonfile=f.read()
            year_data=json.loads(jsonfile)
            df = pd.DataFrame(year_data['data'])
            lowest = context.minimum
            highest = context.maximum
            zlist = pd.DataFrame(df['z'][0])

            if lowest:
                zlist = zlist.where(zlist > lowest)

            if highest:
                zlist = zlist.where(zlist < highest)

            data = [
                    go.Heatmap(
                    z = zlist.values.tolist(),
                    x = df['x'][0],
                    y = df['y'][0],
                    colorscale = colorscale,
                    colorbar=dict(
                            title=context.colorbar_title
                        ),
                    )
                ]
            layout = go.Layout(
                    autosize=True,
                    showlegend=True,
                    title= context.graph_title,
                    yaxis=dict(
                            title=context.yaxis_title
                        ),
                    xaxis=dict(
                            title="Tid"
                        ),
                    width=1200,
                )


            fig = go.Figure(data=data, layout=layout)
            context.plotly_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')

            context.dato = yesterday

        return context.plotly_html
