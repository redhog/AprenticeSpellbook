import Webwidgets, Grimoire, traceback

class Self(Webwidgets.HtmlWidget):
    html = """
    <div class="objinfo">
     <h2>Your account details</h2>
     <div>Passphrase: %(selfPassphrase)s</div>
     <div>%(save)s</div>
    </div>
    """

    class selfPassphrase(Webwidgets.NewPasswordInputWidget): value = ''

    class save(Webwidgets.ButtonInputWidget):
        title = 'Save'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['change', 'own', 'password']
                                                  )(self.parent.children['selfPassphrase'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
