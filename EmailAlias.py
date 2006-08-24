import Webwidgets, Grimoire, traceback

class EmailAlias(Webwidgets.HtmlWidget):
    html = """
    <div class="actions">
     <div class="newDomain">
      <h2>New domain</h2>
      <div>Domain name: %(newDomainName)s</div>
      <div>%(newDomain)s</div>
     </div>
     <div class="newEmailAlias">
      <h2>New email alias</h2>
      <div>User name: %(newAliasName)s</div>
      <div>Email address to redirect to: %(newAliasAddress)s</div>
      <div>%(newAlias)s</div>
     </div>
    </div>
    <div class="listings">
     <h1>Domain: %(currentDomain)s</h1>
     <div class="domainListing">%(domainListing)s</div>
     <div class="aliasListing">%(aliasListing)s</div>
    </div>
    """

    def update(self):
        self.children['domainListing'].update()
        self.children['aliasListing'].update()

    class newDomainName(Webwidgets.StringInputWidget): value = ''
    class newDomain(Webwidgets.ButtonInputWidget):
        title = 'Add'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['create', 'domain'] + list(self.winId[0][1:])
                                                  )(self.parent.children['newDomainName'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
            self.parent.children['newDomainName'].value = ''
            self.parent.update()

    class newAliasName(Webwidgets.StringInputWidget): value = ''
    class newAliasAddress(Webwidgets.StringInputWidget): value = ''
    class newAlias(Webwidgets.ButtonInputWidget):
        title = 'Add'
        def clicked(self):
            objs = self.parent.children
            try:
                result = self.program.__._getpath(path=['create', 'emailalias'] + list(self.winId[0][1:])
                                                  )(objs['newAliasName'].value,
                                                    objs['newAliasAddress'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
            self.parent.update()
            objs['newAliasName'].value = ''
            objs['newAliasAddress'].value = ''

    class currentDomain(Webwidgets.HtmlWidget):
        html = "%(domain)s"
        def __init__(self, program, winId):
            if winId[0][1:]:
                domain = str(Grimoire.Types.DNSDomain(winId[0][1:]))
            else:
                domain = "Top level domain"
            Webwidgets.HtmlWidget.__init__(self, program, winId, domain = domain)

    class domainListing(Webwidgets.HtmlWidget):
        html = """
        <div id="%(id)s">
         <h2>Sub-domains</h2>
         %(upDir)s
         %(listing)s
        </div>
        """

        def update(self):
            self.children['listing'].update()

        class upDir(Webwidgets.ButtonInputWidget):
            title = 'Go to parent domain'
            def clicked(self):
                self.program.redirectToWindow(self.winId[0][:-1], self.winId[1])

        class listing(Webwidgets.ListWidget):

            pre = "<table>"
            sep = '\n'
            post = "</table>"

            def __init__(self, program, winId):
                Webwidgets.ListWidget.__init__(self, program, winId)
                self.update()

            def update(self):
                entries = set([path[0]
                               for leaf, path in self.program.__._getpath(
                                   path=['introspection', 'dir', 'create', 'emailalias'] + list(self.winId[0][1:]))(1)
                               if leaf and len(path) == 1])
                self.children.clear()
                self.children['pre'] = self.pre
                self.children['sep'] = self.sep
                self.children['post'] = self.post
                self.children.update(
                    dict([(str(name), self.Entry(self.program, self.winId, name=name))
                          for name in entries]))

            class Entry(Webwidgets.HtmlWidget):
                __explicit_load__ = True
                __attributes__ = Webwidgets.HtmlWidget.__attributes__ + ('name',)
                html = """
                <tr>
                 <td>
                  %(goTo)s
                 </td>
                 <td>
                  %(delete)s
                 </td>
                </tr>"""
                class GoTo(Webwidgets.ButtonInputWidget):
                    __explicit_load__ = True
                    def clicked(self):
                        self.program.redirectToWindow(self.winId[0] + (self.title,), self.winId[1])
                class delete(Webwidgets.ButtonInputWidget):
                    title='Delete'
                    def clicked(self):
                        class Dialog(Webwidgets.DialogWidget):
                            entry = self.parent
                            head="Really delete domain?"
                            class body(Webwidgets.HtmlWidget):
                                html = 'Do you really want to delete %s' % self.parent.name
                            def clicked(self, yes):
                                 Webwidgets.DialogWidget.clicked(self, yes)
                                 if int(yes):
                                     try:
                                         result = self.program.__._getpath(
                                             path=['delete', 'domain'] + list(self.winId[0][1:]) + [self.entry.name])()
                                     except Exception, result:
                                         traceback.print_exc()
                                     self.parent.children['message'].children['message'] = result and str(result)
                                     self.entry.parent.update()
                        self.parent.parent.parent.parent.parent.children['dialog'] = Dialog(self.program, self.winId)
                    
                def __init__(self, program, winId, **attrs):
                    Webwidgets.HtmlWidget.__init__(self, program, winId, **attrs)
                    self.children['goTo'] = self.GoTo(program, winId, title = self.name)

    class aliasListing(Webwidgets.HtmlWidget):
        html = """
        <div id="%(id)s">
         <h2>Email aliases for this domain</h2>
         %(listing)s
        </div>
        """

        def update(self):
            self.children['listing'].update()

        class listing(Webwidgets.ListWidget):

            pre = "<table>"
            sep = '\n'
            post = "</table>"

            def __init__(self, program, winId, **attrs):
                Webwidgets.ListWidget.__init__(self, program, winId, **attrs)
                self.update()

            def update(self):
                entries = set([path[0]
                               for leaf, path in self.program.__._getpath(
                                   path=['introspection', 'dir', 'delete', 'emailalias'] + list(self.winId[0][1:]))(1)
                               if leaf and len(path) == 1])
                self.children.clear()
                self.children['pre'] = self.pre
                self.children['sep'] = self.sep
                self.children['post'] = self.post
                self.children.update(
                    dict([(str(name), self.Entry(self.program, self.winId, name=name))
                          for name in entries]))

            class Entry(Webwidgets.HtmlWidget):
                __explicit_load__ = True
                __children__ = Webwidgets.HtmlWidget.__children__ + ('name',)
                html = """
                <tr>
                 <td>
                  %(name)s
                 </td>
                 <td>
                  %(delete)s
                 </td>
                </tr>"""
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
                                             path=['delete', 'emailalias'] + list(self.winId[0][1:]) + [self.entry.name])()
                                     except Exception, result:
                                         traceback.print_exc()
                                     self.parent.children['message'].children['message'] = result and str(result)
                                     self.entry.parent.update()
                        self.parent.parent.parent.parent.parent.children['dialog'] = Dialog(self.program, self.winId)



