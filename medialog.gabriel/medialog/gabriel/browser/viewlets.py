#plone stuff
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#from plone import api
from zope.i18nmessageid import MessageFactory

import urllib

#plotly stuff
import plotly 
from plotly.graph_objs import Bar, Scatter, Figure, Layout
from plotly.tools import FigureFactory as FF
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

import json
import datetime 

class PlotView(ViewletBase):
    """ plot something """

    @property
    def plotly_html(self):
        """return the html generated from plotly"""

        context = self.context
        
        if not context.plotly_html:
            self.make_plot()
        
        return context.plotly_html
        
        
        
class GraphView(ViewletBase):
    """ return graph for current day """
    
        
    @property
    def yesterday(self):
    	return datetime.date.today() - datetime.timedelta(1)
    
    @property
    def graph(self):
        """return the html generated from plotly"""
        
        context = self.context
        
        #today we will show yesterdays graph
        yesterday = datetime.date.today() - datetime.timedelta(1)
        
        if context.dato != yesterday:  
            dtype = context.dtype
            trace = []
       
            date = yesterday.strftime("%Y%m%d")
            day_url = 'http://146.185.167.10/resampledday/%s/' %dtype
            #on its own line, in case of looping
            json_url = day_url + date + '.json'
            f = urllib.urlopen(json_url)   
            jsonfile=f.read()
            daydata=json.loads(jsonfile)
            df = pd.DataFrame(daydata)
            xaxis = df['ts'].replace(to_replace=':00:00 GMT', value='', regex=True)
            df.head()
            this_dive = pd.DataFrame(df['divedata'].values.tolist())
    
            #seven dives a day, usually
            for i in range(1,this_dive.shape[1]):
                this_preassure = pd.DataFrame(this_dive[i-1].values.tolist())
                name=str(this_preassure['pressure(dBAR)'][0])
                graphname = name + ' dBar '
        
                # Create a trace
                trace.append(go.Scatter(
                            x = xaxis,
                            y = this_preassure[dtype],
                            name = graphname,
                ))
            
            layout = go.Layout(
                height=1000,
                xaxis=dict(
                title='Tidspunkt',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                ),
                yaxis=dict(
                    title='Verdi',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            )
    
            fig = go.Figure(data=trace)
            context.plotly_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
            context.dato = yesterday

        return context.plotly_html
        
        