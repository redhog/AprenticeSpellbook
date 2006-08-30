import Webwidgets, Grimoire, traceback

class AdslConfig(Webwidgets.HtmlWidget):
    html = """
    <div class="actions">
     <div class="newPeer">
      <h2>New ADSL peer</h2>
      <div>Name: %(newPeerName)s</div>
      <div>Client (user@host): %(newPeerClient)s</div>
      <div>Passphrase: %(newPeerPassphrase)s</div>
      <div>IP number: %(newPeerIP)s</div>
      <div>%(newPeer)s</div>
     </div>
    </div>
    <div class="listings">
     <h1>ADSL configuration</h1>
     <div class="peerListing">%(peerListing)s</div>
    </div>
    """

    def update(self):
        self.children['peerListing'].update()

    class newPeerName(Webwidgets.StringInputWidget): value = ''
    class newPeerClient(Webwidgets.StringInputWidget): value = ''
    class newPeerPassphrase(Webwidgets.NewPasswordInputWidget): value = ''
    class newPeerIP(Webwidgets.StringInputWidget): value = ''
    class newPeer(Webwidgets.ButtonInputWidget):
        title = 'Add'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['create', 'adsl', 'peer'] + list(self.winId[0][1:])
                                                  )(self.parent.children['newPeerName'].value,
                                                    self.parent.children['newPeerClient'].value,
                                                    self.parent.children['newPeerPassphrase'].value,
                                                    self.parent.children['newPeerIP'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
            self.parent.children['newPeerName'].value = ''
            self.parent.children['newPeerClient'].value = ''
            self.parent.children['newPeerPassphrase'].value = ''
            self.parent.children['newPeerIP'].value = ''
            self.parent.update()

    class peerListing(Webwidgets.HtmlWidget):
        html = """
        <div id="%(id)s">
         <h2>ADSL peers</h2>
         %(updateListing)s
         %(listing)s
        </div>
        """

        def update(self):
            self.children['listing'].update()

        class updateListing(Webwidgets.ButtonInputWidget):
            title = 'Update'
            def clicked(self):
                self.parent.update()

        class listing(Webwidgets.ListWidget):

            pre = """<table>
                      <tr>
                       <th>
                        Name
                       </th>
                       <th>
                        User
                       </th>
                       <th>
                        Interface
                       </th>
                       <th>
                        Local IP#
                       </th>
                       <th>
                        Remote IP#
                       </th>
                       <th colspan="2">
                        Actions
                       </th>
                      </tr>"""
            sep = '\n'
            post = "</table>"

            def __init__(self, program, winId, **attrs):
                Webwidgets.ListWidget.__init__(self, program, winId, **attrs)
                self.update()

            def update(self):
                entries = self.program.__._callWithUnlockedTree(
                    lambda: self.program.__._getpath(
                       path=['list', 'adsl', 'peers'] + list(self.winId[0][1:]))(1, False))
                self.children.clear()
                self.children['pre'] = self.pre
                self.children['sep'] = self.sep
                self.children['post'] = self.post
                self.children.update(
                    dict([(name, self.Entry(self.program, self.winId, title = name, connection=peer.connection, client=peer.properties['user']))
                          for name, peer in entries.iteritems()
                          if 'user' in peer.properties]))

            class Entry(Webwidgets.HtmlWidget):
                __explicit_load__ = True
                html = """
                <tr>
                 <td>
                  %(account)s
                 </td>
                 <td>
                  %(client)s
                 </td>
                 <td>
                  %(ifname)s
                 </td>
                 <td>
                  %(local)s
                 </td>
                 <td>
                  %(remote)s
                 </td>
                 <td>
                  %(control)s
                 </td>
                 <td>
                  %(delete)s
                 </td>
                </tr>"""
                def __init__(self, program, winId, title, connection, client, **attrs):
                    account = self.Account(program, winId, title=title)
                    if connection:
                        control = self.Disable(program, winId)
                        ifname = connection['if']
                        local = connection['local']
                        remote = connection['remote']           
                    else:
                        control = self.Enable(program, winId)
                        ifname = ''
                        local = ''
                        remote = ''
                    Webwidgets.HtmlWidget.__init__(
                        self, program, winId,
                        title=title, account=account, client=client, control=control, ifname=ifname, local=local, remote=remote,
                        **attrs)

                class Account(Webwidgets.ButtonInputWidget):
                    __explicit_load__ = True
                    def clicked(self):
                        self.program.redirectToWindow(self.winId[0] + (self.parent.title,), self.winId[1])

                class Enable(Webwidgets.ButtonInputWidget):
                    __explicit_load__ = True
                    title = 'Enable'
                    def clicked(self):
                        try:
                            result = self.program.__._getpath(path=['enable', 'adsl', 'peer'] + list(self.winId[0][1:]) + [self.parent.title])()
                        except Exception, result:
                            traceback.print_exc()
                        self.parent.parent.parent.parent.parent.children['message'].children['message'] = result and str(result)
                        self.parent.parent.parent.parent.update()

                class Disable(Webwidgets.ButtonInputWidget):
                    __explicit_load__ = True
                    title = 'Disable'
                    def clicked(self):
                        try:
                            result = self.program.__._getpath(path=['disable', 'adsl', 'peer'] + list(self.winId[0][1:]) + [self.parent.title])()
                        except Exception, result:
                            traceback.print_exc()
                        self.parent.parent.parent.parent.parent.children['message'].children['message'] = result and str(result)
                        self.parent.parent.parent.parent.update()
                
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
                                             path=['delete', 'adsl', 'peer'] + list(self.winId[0][1:]) + [self.entry.title])()
                                     except Exception, result:
                                         traceback.print_exc()
                                     self.parent.children['message'].children['message'] = result and str(result)
                                     self.entry.parent.update()
                        self.parent.parent.parent.parent.parent.children['dialog'] = Dialog(self.program, self.winId)
