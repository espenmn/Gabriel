from zope import schema
from plone.directives import form
import plone.directives
from plone import directives
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from zope.i18nmessageid import MessageFactory
import datetime 

from plone.supermodel import model
from plone.autoform import directives

_ = MessageFactory('medialog.gabriel')

def theDefaultValue():
    return datetime.date.today() - datetime.timedelta(1)

def minValue():
    return datetime.date(2015, 5, 12)

def maxValue():
    return datetime.date.today()

class IDate(schema.Date):
    """ Data field for tuple. min and max are not working inside the tuple
    they need to be set in the tuple instead"""
    date=schema.Date(
            defaultFactory=theDefaultValue,
            min=datetime.date(2015, 5, 12),
			max=datetime.date.today(),
    )


class IYearGraphBehavior(form.Schema):
    """ Fields to construct text to use in graph application"""
    
    history_graph_url = schema.URI(
        title=u'URL to graph data',
        required=True,
        default="https://ektedata.uib.no/gabrieldata/api/v1/heatmap/temp.json",
    )
    
    colorscale = schema.Choice(
        title=u'Colorscale',
        required=True,
        values=( "Greys", 
        		"YlGnBu", 
        		"Greens", 
        		"YlOrRd", 
        		"Bluered", 
        		"RdBu", 
        		"Reds", 
        		"Blues", 
        		"Picnic", 
        		"Rainbow", 
        		"Portland", 
        		"Jet", 
        		"Hot", 
        		"Blackbody", 
        		"Earth", 
        		"Electric", 
        		"Viridis",
            ),
    )
    
    
    
    graph_title = schema.TextLine(
        title=u'Heatmap title',
        default=u'Heatmap Tittel',
        required=True,
    )
    
    yaxis_title = schema.TextLine(
        title=u'Y-axis title',
        default=u'Y akse',
        required=True,
    )

    form.mode(plotly_html='hidden')
    plotly_html = schema.Text(
        title=u'Plotly html',
        default=u'Ingen relevante data ble funnet hos Gabriel',
        required=False,
    )
    
    form.mode(dato='hidden')
    dato=schema.Date(
            title=_(u"Dato"),
            default=datetime.date(2015, 5, 12),
    )

alsoProvides(IYearGraphBehavior, IFormFieldProvider)



class IGraphBehavior(form.Schema):
    """ Fields to construct text to use in graph application"""
    
    dtype = schema.Choice(
        title=u'type',
        required=True,
        values=(
                "salt",
                "fluorescens",
                "oxygene",
                "temp",
                "turbidity",
            ),
    )
    
    date1=schema.Date(
            defaultFactory=theDefaultValue,
            min=datetime.date(2015, 5, 12),
			max=datetime.date.today(),
    )
    
    date2=schema.Date(
            defaultFactory=theDefaultValue,
            min=datetime.date(2015, 5, 12),
			max=datetime.date.today(),
    )
    
    form.mode(plotly_html='hidden')
    plotly_html = schema.Text(
        title=u'Plotly html',
        default=u'Ingen relevante data ble funnet hos Gabriel',
        required=False,
    )

alsoProvides(IGraphBehavior, IFormFieldProvider)

    

    
class IGabrielBehavior(form.Schema):
    """ Fields to construct the gabriel
    graphs from JSON URLs"""
    
    dates = schema.Tuple(
    	title=_(u"Datoer"),
    	description=_(u"Velg og legg til datoer du vil ha grafer av"),
    	required=True,
    	default = (theDefaultValue(),),
    	value_type=IDate(
            title=_(u"Dato"),
        )
    )
    
    form.mode(plotly_html='hidden')
    plotly_html = schema.Text(
        title=u'Plotly html',
        default=u'Ingen relevante data ble funnet hos Gabriel',
        required=False,
    )
    
    
alsoProvides(IGabrielBehavior, IFormFieldProvider)



class IGabrielGraphBehavior(form.Schema):
    """ Fields to construct todays
    graphs from JSON URLs"""
    
    dtype = schema.Choice(
        title=u'type',
        required=True,
        values=(
                "salt",
                "fluorescens",
                "oxygene",
                "temp",
                "turbidity",
            ),
    )
    
    form.mode(plotly_html='hidden')
    plotly_html = schema.Text(
        title=u'Plotly html',
        default=u'Ingen relevante data ble funnet hos Gabriel',
        required=False,
    )
        
    form.mode(plotly2_html='hidden')
    plotly2_html = schema.Text(
        title=u'Plotly2 html',
        default=u'Ingen relevante data ble funnet hos Gabriel',
        required=False,
    )
    
    form.mode(plotly3_html='hidden')
    plotly3_html = schema.Text(
        title=u'Plotly3 html',
        default=u'Ingen relevante data ble funnet hos Gabriel',
        required=False,
    )
    
    form.mode(plotly4_html='hidden')
    plotly4_html = schema.Text(
        title=u'Plotly4 html',
        default=u'Ingen relevante data ble funnet hos Gabriel',
        required=False,
    )
    
    form.mode(dato='hidden')
    dato=schema.Date(
            title=_(u"Dato"),
            default=datetime.date(2015, 5, 12),
    )
    
alsoProvides(IGabrielGraphBehavior, IFormFieldProvider)


class IShareBehavior(form.Schema):
    """ Share this on facebook"""
    
    form.fieldset(
		'Settings',
		fields=[
			'fb_enable',
		],
	)

    fb_enable = schema.Bool(
    	title=_(u"Enable FB sharing"),
    	description=_(u"Enabler facebook sharing"),
    	required=False,
    	default=True,
    )

    
alsoProvides(IShareBehavior, IFormFieldProvider)


