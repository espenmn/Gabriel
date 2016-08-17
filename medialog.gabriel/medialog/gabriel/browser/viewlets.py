#plone stuff
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#plotly stuff
#import plotly 
#from plotly.graph_objs import Bar, Scatter, Figure, Layout
#import pandas as pd
#import numpy as np
#import plotly.plotly as py
#import plotly.graph_objs as go
    

class PlotView(ViewletBase):
    """ plot something """

    @property
    def plotly_html(self):
        """return the html generated from plotly"""

        context = self.context
        
        if not context.plotly_html:
        	self.make_plot()
        
        return context.plotly_html
        
    	