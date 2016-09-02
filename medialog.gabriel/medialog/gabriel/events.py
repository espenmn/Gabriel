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
import json

import datetime 

from Products.statusmessages.interfaces import IStatusMessage

_ = MessageFactory('medialog.plotly')
 

def login(self):
    username = self.portal_registry['medialog.plotly.interfaces.IPlotlySettings.plotly_username']
    api_key  = self.portal_registry['medialog.plotly.interfaces.IPlotlySettings.plotly_api_key']
    plotly.tools.set_credentials_file(username=username, api_key=api_key)
    

def make_html(self, context):
    """let plottly make the graph
    generating the html from plotly"""
    
    #dont need login for offline
    #self.login()
    
    dybder = self.dybder
    
    if len(dybder) != 0:
        dates =  self.dates 
        dtypes = self.dtypes
                
        trace=[]
    
        graph_count=0
        

    
        for dtype in dtypes:
            traces = []
            graph_count += 1
            for dato in dates:
                if dato > datetime.date(2015, 5, 12) and dato <  datetime.date.today():
                    date = dato.strftime("%Y%m%d")
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
    
                    for i in range(1,this_dive.shape[1]):
                        this_preassure = pd.DataFrame(this_dive[i-1].values.tolist())
                        name=str(this_preassure['pressure(dBAR)'][0])
                        graphname = name + ' dBar ' + dato.strftime("%d.%m.%y")  + ': '  + dtype
        
                        #visible = "legendonly"
                        #visible = False
                        if unicode(name) in dybder:
                            #visible = True 
                            # Create a trace
                            if graph_count % 2 == 0:
                                trace.append(go.Bar(
                                    x = xaxis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                ))
                            if graph_count % 2 == 1:
                                trace.append(go.Scatter(
                                    x = xaxis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                ))
            
        import pdb; pdb.set_trace()
        if trace != []:
            fig = go.Figure(data=trace)
            self.plotly_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
            context.plotly_html = self.plotly_html


    else:
        """let plottly make the 3D graph """

    
        dates =  self.dates 
        dtypes = self.dtypes
                
        plotly_html = ''
    
        graph_count=0
    
        for dtype in dtypes:
            graph_count += 1
            for dato in dates:
                if dato > datetime.date(2015, 5, 12) and dato <  datetime.date.today():
                    date = dato.strftime("%Y%m%d")
                    day_url = 'http://146.185.167.10/resampledday/%s/' %dtype
                    #on its own line, in case of looping
                    json_url = day_url + date + '.json'
                    f = urllib.urlopen(json_url)   
                    jsonfile=f.read()
                    daydata=json.loads(jsonfile)
                    df = pd.DataFrame(daydata)
                    df.head()
                
                    #and now the 3D graph
                    z = []
        
                    #construct the 3d z
                    for i in range(0,len(df)):
                        this_z = pd.DataFrame(df['divedata'][i]).sort_values('pressure(dBAR)', ascending=True)
                        z.append(this_z[dtype])
                    
                    data = [
                        go.Surface(
                        z=  z,
                        x= pd.DataFrame(df['divedata'][0])['pressure(dBAR)'].sort_values(),
                        y = df['ts']
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
                            )
                        ),
                        width=900,
                        height=1000,
                        margin=dict(
                            l=5,
                            r=5,
                            b=5,
                            t=9
                        )
                    )

                    fig = go.Figure(data=data, layout=layout)
                    plotly_html += plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
                
            self.plotly_html = plotly_html