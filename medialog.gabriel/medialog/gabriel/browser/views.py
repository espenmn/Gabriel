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
        
        if context.dato != yesterday:  
            #history_graph_id = 'history-graph-' + context.id
            graph_url = context.history_graph_url
        
            colorscale= context.colorscale
        
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