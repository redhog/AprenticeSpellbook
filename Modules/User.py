import Webwidgets, Grimoire, traceback

class User(Webwidgets.HtmlWidget):
    html = """
    <div class="objinfo">
     <h2>Account details for %(userName)s</h2>
     <div>Passphrase: %(userPassphrase)s</div>
     <div>%(save)s</div>
    </div>
    """

    def __init__(self, program, winId, **attrs):
        Webwidgets.HtmlWidget.__init__(
            self, program, winId,
            userName = winId[0][-1],
            **attrs)

    class userPassphrase(Webwidgets.NewPasswordInputWidget): value = ''

    class save(Webwidgets.ButtonInputWidget):
        title = 'Save'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['change', 'password'] + list(self.winId[0][1:-2]) + [self.winId[0][-1]]
                                                  )(self.parent.children['userPassphrase'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
