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
    date=schema.Date(
            title=_(u"Dato"),
            defaultFactory=theDefaultValue,
            min=datetime.date(2015, 5, 12),
            max=datetime.date.today(),
    )
    
    directives.widget(
        'date',
        pattern_options={
            'date': {
                min: [2015, 5, 12],
                max: [2016, 8, 12]
                }
            }
        )

class IGabrielBehavior(form.Schema):
    """ Fields to consgtruct the gabriel
    graphs from JSON URLs"""
    
    dates = schema.Tuple(
    	title=_(u"Datoer"),
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


