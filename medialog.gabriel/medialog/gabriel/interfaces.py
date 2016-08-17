from zope.interface import Interface
from z3c.form import interfaces
from zope import schema
from zope.interface import alsoProvides
from plone.directives import form
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.gabriel')


class IGabriel(Interface):
    """Marker interface for plotly graphs"""


class IPlotlySettings(form.Schema):
    """Adds settings to medialog.controlpanel
    """

    form.fieldset(
        'plotly',
        label=_(u'Plotly'),
        fields=[
             'plotly_username',
             'plotly_api_key'
        ],
     )
    
    plotly_username = schema.TextLine(
        title = _("label_plotly_username", default=u"Plotly Username"),
        description = _("help_plotly",
                      default="Your Plotly ID"),

    )

    plotly_api_key = schema.TextLine(
        title = _("label_plotly_api_key", default=u"Plotly API key"),
        description = _("help_plotly_api",
                      default="Your Plotly API key"),

    )
    
alsoProvides(IPlotlySettings, IMedialogControlpanelSettingsProvider)