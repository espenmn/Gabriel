from zope.interface import implements, Interface
#, Attribute
from Products.Five import BrowserView
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.browser.view import DefaultView


class YearGraphView(DefaultView, BrowserView):
    """default view for yeargraph content type"""
    
    def javascript(self):
        """construct a javascript to show the histogram"""

        context = self.context
        history_graph_id = 'history-graph-' + context.id
        
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
        Plotly.newPlot('%(history_graph)s', fig.data, fig.layout);
    });
}
</script>
""" % {
        'history_graph_url': context.history_graph_url,
        'graph_title': context.graph_title,
        'yaxis_title': context.yaxis_title,
        'history_graph': history_graph_id,
    }

        