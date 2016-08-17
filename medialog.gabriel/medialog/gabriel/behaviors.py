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
              'json_url',
              'plotly_html'
        ],
     )
    
    form.mode(plotly_html='hidden')
    plotly_html = schema.Text(
        title=u'Plotly html',
        default=u'You must reload the page to see the graph',
        required=False,
    )
         
    json_url = schema.URI(
        title = _("label_json_url", default=u"URL to JSON data"),
        description = _("help_json_url",
                      default=""),
        required = True,
     )
    
alsoProvides(IGabrielBehavior, IFormFieldProvider)






