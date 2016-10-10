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
from plotly.graph_objs import Bar, Scatter, Figure, Layout,  Surface
from plotly.tools import FigureFactory as FF
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

import json
import datetime 

class YearGraphViewlet(ViewletBase):
    """ javascript for histogram """

    def javascript(self):
        """construct a javascript to show the histogram"""

        context = self.context
        
        if context.history_graph_url == "http://146.185.167.10/api/v1/turbidity/temp.json":
			return """<script>drawHistoryGraph();
				function drawHistoryGraph() {
				var historyGraphURL = '%(history_graph_url)s';
				console.log("Loading history graph, URL: " + historyGraphURL);
				d3.json(historyGraphURL, function(err, fig) {
					fig.layout = {
					  title: '%(graph_title)s',
					  xaxis: {
					  	title: 'Tid', 
					  	showline: true, 
					  	mirror: 'allticks', 
					  	ticks: 'inside',
					  },
					  yaxis: {
						title: '%(yaxis_title)s',
						type: 'linear',
						showline: true,
						autorange:true,
						mirror: 'allticks',
						ticks: 'inside',
					  },
					};
					Plotly.newPlot('history-graph', fig.data, fig.layout);
				});
			}
			</script>
			""" % {
					'history_graph_url': context.history_graph_url,
					'graph_title': context.graph_title,
					'yaxis_title': context.yaxis_title,
					}
		
        
        return """<script>drawHistoryGraph();
			function drawHistoryGraph() {
				var historyGraphURL = '%(history_graph_url)s';
				console.log("Loading history graph, URL: " + historyGraphURL);
				d3.json(historyGraphURL, function(err, fig) {
					fig.layout = {
					  title: '%(graph_title)s',
					  yaxis: {
						title: '%(yaxis_title)s',
					  },
					};
					Plotly.newPlot('history-graph', fig.data, fig.layout);
				});
			}
			</script>
			""" % {
					'history_graph_url': context.history_graph_url,
					'graph_title': context.graph_title,
					'yaxis_title': context.yaxis_title,
					}
			

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
    
    def yesterday(self):
        return datetime.date.today() - datetime.timedelta(1)
    
    def graph(self):
        """return the html generated from plotly"""
        
        context = self.context        
        #today we will show yesterdays graph
        yesterday = datetime.date.today() - datetime.timedelta(1)
        
        if context.dato != yesterday:  
            try: 
                dtype = context.dtype
                trace = []
                trace2 = []
       
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
                    graphname = name + ' m '
        
                    # Create a trace
                    trace.append(go.Scatter(
                                x = xaxis,
                                y = this_preassure[dtype],
                                name = graphname,
                    ))
                    trace2.append(go.Scatter(
                                x = xaxis,
                                y = this_preassure[dtype],
                                name = graphname,
                                mode = 'markers'
                    ))
            
                layout = go.Layout(
                    height=700,
                    width=1200,
                    autosize=False,
                    xaxis=dict(
                    title='Tidspunkt',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=14,
                            color='#7f7f7f'
                        )
                    ),
                    yaxis=dict(
                        title=dtype,
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=14,
                            color='#7f7f7f'
                        )
                    )
                )
                
                fig = go.Figure(data=trace, layout=layout)
                context.plotly_html = plotly.offline.plot(fig, show_link=True, include_plotlyjs = False, output_type='div')

                #graph 2
                fig = go.Figure(data=trace2,layout=layout)
                context.plotly2_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')

                #and now the 3D graphs
                z = []
        
                #construct the 3d z
                for i in range(0,len(df)):
                    this_z = pd.DataFrame(df['divedata'][i]).sort_values('pressure(dBAR)', ascending=True)
                    z.append(this_z[dtype])
                    #.values.tolist())

                data = [
                    go.Surface(
                    z= z,
                    x= pd.DataFrame(df['divedata'][0])['pressure(dBAR)'].sort_values(),
                    y = df['ts']
                    )
                ]
                data2 = [
                    go.Heatmap(
                    z=  z,
                    x= pd.DataFrame(df['divedata'][0])['pressure(dBAR)'].sort_values(),
                    y = df['ts']
                    )
                ]
                
                layout = go.Layout(
                    autosize=False,
                    scene=dict(
                        xaxis=dict(
                            title="Dybde"
                        ),
                        yaxis=dict(
                            title="Tid"
                        ),
                        zaxis=dict(
                            title=dtype
                        )
                    ),
                    width=1200,
                    height=700,
                    margin=dict(
                        l=5,
                        r=5,
                        b=25,
                        t=9
                    )
                )

                fig = go.Figure(data=data, layout=layout)
                context.plotly3_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
                
                fig = go.Figure(data=data2, layout=layout)
                context.plotly4_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
                
                context.dato = yesterday
            
            except:
                "Gabriel data ble ikke funnet"
                
        return context.plotly_html
        
        