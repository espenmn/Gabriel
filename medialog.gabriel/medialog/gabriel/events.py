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
    title = self.title
    
    if len(dybder) != 0:
        dates =  self.dates 
        dtypes = self.dtypes
        ant_types = len(dtypes)
                
        trace=[]
    
        graph_count=0
        title1 = ''
        title2 = ''
        title3 = ''
        title4 = ''
        title5 = ''
        color1 = '#FFF'
        color2 = '#FFF'
        color3 = '#FFF'
        color4 = '#FFF'
        color5 = '#FFF'
        color6 = '#FFF'
        color7 = '#FFF'
        color8 = '#FFF'
        color9 = '#FFF'
    

    
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
                    xaksis = df['ts'].replace(to_replace=':00:00 GMT', value='', regex=True)
                    df.head()
                    this_dive = pd.DataFrame(df['divedata'].values.tolist())
    
                    for i in range(1,this_dive.shape[1]):
                        this_preassure = pd.DataFrame(this_dive[i-1].values.tolist())
                        name=str(this_preassure['pressure(dBAR)'][0])
                        graphname = name + ' dBar: '  + dtype
        
                        #visible = "legendonly"
                        #visible = False
                                              if unicode(name) in dybder:
                            #visible = True 
                            # Create a trace
                            if graph_count % ant_types == 0 and ant_types != 1:
                                trace.append(go.Bar(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    )
                                )
                                title1=dtype
                                color1='#123456'
                                
                            if graph_count % ant_types == 1 or ant_types == 1:
                                trace.append(go.Scatter(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    line = dict(
                                        width = 2,
                                        ),
                                    yaxis='y2'
                                    )
                                )
                                title2=dtype
                                color2='#ff4444'

                            if graph_count % ant_types == 2:
                                trace.append(go.Scatter(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    yaxis='y3',
                                    line = dict(
                                        width = 2,
                                        ),
                                    mode='lines'
                                    )
                                )
                                title3=dtype
                                color3='#3399ff'

                            if graph_count % ant_types == 3:
                                trace.append(go.Scatter(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    line = dict(
                                        width = 3,
                                        dash = 'dash',
                                        ),
                                    yaxis='y4',
                                    )
                                )
                                title4=dtype
                                color4='#333333'
                                                        
                            if graph_count % ant_types == 4:
                                trace.append(go.Scatter(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    yaxis='y5',
                                    line = dict(
                                        width = 3,
                                        dash = 'dot'
                                        ),
                                    )
                                )
                                title5=dtype
                                color5='#CCCCCC'

                            if graph_count % ant_types == 5:
                                trace.append(go.Scatter(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    yaxis='y6',
                                    line = dict(
                                        width = 1,
                                        ),
                                    )
                                )
                                title6=dtype
                                color6='#CCCCCC'

                            if graph_count % ant_types == 6:
                                trace.append(go.Scatter(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    yaxis='y7',
                                    line = dict(
                                        width = 1,
                                        ),
                                    )
                                )
                                title7=dtype
                                color7='#CCCCCC'
                                
                            if graph_count % ant_types == 7:
                                trace.append(go.Scatter(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    yaxis='y8',
                                    line = dict(
                                        width = 1,
                                        ),
                                    )
                                )
                                title8=dtype
                                color8='#CCCCCC'
                                
                            if graph_count % ant_types == 8:
                                trace.append(go.Scatter(
                                    x = xaksis,
                                    y = this_preassure[dtype],
                                    name = graphname,
                                    yaxis='y9',
                                    line = dict(
                                        width = 1,
                                        ),
                                    )
                                )
                                title9=dtype
                                color9='#CCCCCC'
                            
        #data = trace
        layout = go.Layout(
                title=title,
                legend=dict(orientation= "v"),
                yaxis=dict(
                    title=title1,
                    rangemode='tozero',
                    titlefont=dict(
                        color='rgb(248, 23, 189)'
                    ),
                    tickfont=dict(
                        color='rgb(248, 23, 189)'
                    ),
                    side='right'
                ),
                yaxis2=dict(
                    title=title2,
                    rangemode='tozero',
                    titlefont=dict(
                        color=color2
                    ),
                    tickfont=dict(
                        color=color2
                    ),
                    overlaying='y',
                    side='left'
                ),
                yaxis3=dict(
                    title=title3,
                    rangemode='tozero',
                    titlefont=dict(
                        color=color3
                    ),
                    tickfont=dict(
                        color=color3
                    ),
                    overlaying='y',
                    side='left',
                ),
                yaxis4=dict(
                    rangemode='tozero',
                    title=title4,
                    titlefont=dict(
                        color=color4
                    ),
                    tickfont=dict(
                        color=color4
                    ),
                    overlaying='y',
                    side='right',
                ),
                yaxis5=dict(
                    title=title5,
                    rangemode='tozero',
                    titlefont=dict(
                        color=color5
                    ),
                    tickfont=dict(
                        color=color5
                    ),
                    overlaying='y',
                    side='left',
                )
            )
        
        fig = go.Figure(data=trace, layout=layout)
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