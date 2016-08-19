from zope import schema
from plone.directives import form
import plone.directives
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.gabriel')


class IGabrielBehavior(form.Schema):
    """ Can be 'plotlified
    graphs from JSON URLs"""
    
    form.fieldset(
        'plotly',
        label=_(u'Plotly'),
        fields=[
              'plotly_html'
        ],
     )
    
    form.mode(plotly_html='hidden')
    plotly_html = schema.Text(
        title=u'Plotly html',
        default=u'You must reload the page to see the graph',
        required=False,
    )
    
alsoProvides(IGabrielBehavior, IFormFieldProvider)






