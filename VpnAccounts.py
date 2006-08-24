import Webwidgets, Grimoire, traceback

class VpnAccounts(Webwidgets.HtmlWidget):
    html = """
    <div class="actions">
     <div class="newAccount">
      <h2>New VPN account</h2>
      <div>Client (user@host): %(newAccountClient)s</div>
      <div>Passphrase: %(newAccountPassphrase)s</div>
      <div>IP number: %(newAccountIP)s</div>
      <div>%(newAccount)s</div>
     </div>
    </div>
    <div class="listings">
     <h1>VPN configuration</h1>
     <div class="accountListing">%(accountListing)s</div>
    </div>
    """

    def update(self):
        self.children['accountListing'].update()

    class newAccountClient(Webwidgets.StringInputWidget): value = ''
    class newAccountPassphrase(Webwidgets.NewPasswordInputWidget): value = ''
    class newAccountIP(Webwidgets.StringInputWidget): value = ''
    class newAccount(Webwidgets.ButtonInputWidget):
        title = 'Add'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['create', 'vpn', 'account'] + list(self.winId[0][1:])
                                                  )(self.parent.children['newAccountClient'].value,
                                                    self.parent.children['newAccountPassphrase'].value,
                                                    self.parent.children['newAccountIP'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
            self.parent.children['newAccountClient'].value = ''
            self.parent.children['newAccountPassphrase'].value = ''
            self.parent.children['newAccountIP'].value = ''
            self.parent.update()

    class accountListing(Webwidgets.HtmlWidget):
        html = """
        <div id="%(id)s">
         <h2>VPN accounts</h2>
         %(listing)s
         %(save)s
        </div>
        """

        def update(self):
            self.children['listing'].update()

        class save(Webwidgets.ButtonInputWidget): title='Save changes' # Do nothing - the valueChanged callbacks do the actual saving...

        class listing(Webwidgets.ListWidget):

            pre = "<table>"
            sep = '\n'
            post = "</table>"

            def __init__(self, program, winId, **attrs):
                Webwidgets.ListWidget.__init__(self, program, winId, **attrs)
                self.update()

            def update(self):
                entries = self.program.__._getpath(
                    path=['list', 'vpn', 'accounts'] + list(self.winId[0][1:]))(1, False)
                self.children.clear()
                self.children['pre'] = self.pre
                self.children['sep'] = self.sep
                self.children['post'] = self.post
                self.children.update(
                    dict([(str(client), self.Entry(self.program, self.winId, client=client, secret=secret, ip=ip))
                          for client, (server, secret, ip) in entries.iteritems()]))

            class Entry(Webwidgets.HtmlWidget):
                __explicit_load__ = True
                html = """
                <tr>
                 <td>
                  %(client)s
                 </td>
                 <td>
                  %(secret)s
                 </td>
                 <td>
                  %(ip)s
                 </td>
                 <td>
                  %(delete)s
                 </td>
                </tr>"""
                def __init__(self, program, winId, client, secret, ip, **attrs):
                    secret = Webwidgets.NewPasswordInputWidget(program, winId, value=secret)
                    ip = Webwidgets.StringInputWidget(program, winId, value=ip)
                    Webwidgets.HtmlWidget.__init__(self, program, winId, client=client, secret=secret, ip=ip, **attrs)
                def valueChanged(self, value):
                    try:
                        result = self.program.__._getpath(path=['change', 'vpn', 'account'] + list(self.winId[0][1:]) + [self.client]
                                                          )(self.children['secret'].value,
                                                            self.children['ip'].value)
                    except Exception, result:
                        traceback.print_exc()
                        self.parent.parent.parent.parent.children['message'].children['message'] = result and str(result)                
                
                class delete(Webwidgets.ButtonInputWidget):
                    title='Delete'
                    def clicked(self):
                        class Dialog(Webwidgets.DialogWidget):
                            entry = self.parent
                            head="Really delete alias?"
                            class body(Webwidgets.HtmlWidget):
                                html = 'Do you really want to delete %s' % self.parent.name
                            def clicked(self, yes):
                                 Webwidgets.DialogWidget.clicked(self, yes)
                                 if int(yes):
                                     try:
                                         result = self.program.__._getpath(
                                             path=['delete', 'vpn', 'account'] + list(self.winId[0][1:]) + [self.entry.client])()
                                     except Exception, result:
                                         traceback.print_exc()
                                     self.parent.children['message'].children['message'] = result and str(result)
                                     self.entry.parent.update()
                        self.parent.parent.parent.parent.parent.children['dialog'] = Dialog(self.program, self.winId)



