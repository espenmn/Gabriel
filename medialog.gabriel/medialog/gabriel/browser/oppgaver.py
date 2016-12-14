from pp.client.plone.browser.compatible import InitializeClass
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class OppgaveView(BrowserView):
    """ Converter view for Oppgave.
    """

    template = ViewPageTemplateFile('oppgaver.pt')

    def __call__(self, *args, **kw):
        return self.template(self.context)

InitializeClass(OppgaveView)

