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


class YearGraphView(DefaultView, BrowserView):
    """default view for yeargraph content type"""
    
    def javascript(self):
        """construct a javascript to show the histogram"""

        context = self.context
        history_graph_id = 'history-graph-' + context.id
        graph_url = context.history_graph_url
        
        colorscale= context.colorscale
        
        if graph_url == "shttp://146.185.167.10/api/v1/heatmap/turbidity.json":
            colorscale= [[0.0, 'rgb(165,0,38)'], 
            [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]      

        f = urllib.urlopen(graph_url)   
        jsonfile=f.read()
        year_data=json.loads(jsonfile)
        df = pd.DataFrame(year_data['data'])
        data = [
                go.Heatmap(
                z=  df['z'][0],
                x=  df['x'][0],
                y = df['y'][0],
                colorscale = colorscale,
                autocolorscale=False, 
                )
            ]
        layout = go.Layout(
                autosize=True,
                scene=dict(
                    xaxis=dict(
                        title="Dybde"
                    ),
                    yaxis=dict(
                        title="Tid"
                    ),
                    zaxis=dict(
                        title='dtype'
                    )
                ),
                width=1200,
            )
            
            
        fig = go.Figure(data=data, layout=layout)
        context.plotly_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
        
        return context.plotly_html