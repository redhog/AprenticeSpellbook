import Webwidgets, Grimoire, traceback

class AdslAccountConfig(Webwidgets.HtmlWidget):
    html = """
    <div class="objinfo">
     Information on account.
    </div>
    """
    html = """
    <div class="objinfo">
     <h2>ADSL peer</h2>
     <div>Name: %(peerName)s</div>
     <div>Client (user@host): %(peerClient)s</div>
     <div>Passphrase: %(peerPassphrase)s</div>
     <div>IP number: %(peerIP)s</div>
     <div>%(save)s</div>
    </div>
    """

    def __init__(self, program, winId, **attrs):
        params = Grimoire.Types.getValue(
            program.__._getpath(path=['introspection', 'params', 'change', 'adsl', 'peer', 'properties'] + list(winId[0][1:])
                                )())
        peerClient = Webwidgets.StringInputWidget(program, winId, value=Grimoire.Types.getValue(params.argdict['user']).values[0])
        peerPassphrase = Webwidgets.NewPasswordInputWidget(program, winId, value=Grimoire.Types.getValue(params.argdict['secret']).values[0])
        peerIP = Webwidgets.StringInputWidget(program, winId, value=Grimoire.Types.getValue(params.argdict['ip']).values[0])
        Webwidgets.HtmlWidget.__init__(
            self, program, winId,
            peerName=winId[0][-1], peerClient=peerClient, peerPassphrase=peerPassphrase, peerIP=peerIP)

    class save(Webwidgets.ButtonInputWidget):
        title = 'Save'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['change', 'adsl', 'peer', 'properties'] + list(self.winId[0][1:])
                                                  )(user = self.parent.children['peerClient'].value,
                                                    secret = self.parent.children['peerPassphrase'].value,
                                                    ip = self.parent.children['peerIP'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
