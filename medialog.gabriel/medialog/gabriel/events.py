from plone import api
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

from Products.statusmessages.interfaces import IStatusMessage

_ = MessageFactory('medialog.plotly')
 

def login(self):
    username = self.portal_registry['medialog.plotly.interfaces.IPlotlySettings.plotly_username']
    api_key  = self.portal_registry['medialog.plotly.interfaces.IPlotlySettings.plotly_api_key']
    plotly.tools.set_credentials_file(username=username, api_key=api_key)
    


def make_html(self, context):
    """let plottly make the graph
    generating the html from plotly"""
    
    #title = self.chart_title
    #chart_type = self.chart_type
    #ylabel = self.chart_description
	#false = False
    #true = True
    
    #self.login()
    
    import pdb; pdb.set_trace()
    
    df = pd.read_json(self.json_url)
    
    import pdb; pdb.set_trace()
    
    fig = go.Figure(data=df)
    
    #then make graph
    self.plotly_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
        
