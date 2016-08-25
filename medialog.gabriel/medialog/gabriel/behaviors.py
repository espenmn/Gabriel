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
            title=_(u"Dato"),
            defaultFactory=theDefaultValue,
            min=datetime.date(2015, 5, 12),
            max=datetime.date.today(),
    )
    
class IGabrielBehavior(form.Schema):
    """ Fields to construct the gabriel
    graphs from JSON URLs"""
    
    #form.widget.button_label(dates='fisk')
    dates = schema.Tuple(
    	title=_(u"Datoer"),
    	required=True,
    	default = (theDefaultValue(),),
    	value_type=IDate(
            title=_(u"Dato"),
            min=datetime.date(2015, 5, 12),
            max=datetime.date.today(),
            defaultFactory=theDefaultValue,
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
    
    form.mode(dato='hidden')
    dato=schema.Date(
            title=_(u"Dato"),
            default=datetime.date(2015, 5, 12),
    )
    
alsoProvides(IGabrielGraphBehavior, IFormFieldProvider)
