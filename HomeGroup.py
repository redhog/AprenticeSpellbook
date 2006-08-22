import Webwidgets, Grimoire, traceback

class HomeGroup(Webwidgets.HtmlWidget):
    html = """
    <div class="actions">
     <div class="newGroup">
      <h2>New group</h2>
      <div>Group name: %(newGroupName)s</div>
      <div>%(newGroup)s</div>
     </div>
     <div class="newUser">
      <h2>New user</h2>
      <div>User name: %(newUserName)s</div>
      <div>Given name: %(newUserGivenName)s</div>
      <div>Surname: %(newUserSurName)s</div>
      <div>Password: %(newUserPassword)s</div>
      <div>%(newUser)s</div>
     </div>
    </div>
    <div class="listings">
     <h1>Department: %(currentGroup)s</h1>
     <div class="groupListing">%(groupListing)s</div>
     <div class="userListing">%(userListing)s</div>
    </div>
    """

    def update(self):
        self.children['groupListing'].update()
        self.children['userListing'].update()

    class newGroupName(Webwidgets.StringInputWidget): value = ''
    class newGroup(Webwidgets.ButtonInputWidget):
        title = 'Add'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['create', 'home group'] + list(self.winId[0][1:])
                                                  )(self.parent.children['newGroupName'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
            self.parent.children['newGroupName'].value = ''
            self.parent.update()

    class newUserName(Webwidgets.StringInputWidget): value = ''
    class newUserGivenName(Webwidgets.StringInputWidget): value = ''
    class newUserSurName(Webwidgets.StringInputWidget): value = ''
    class newUserPassword(Webwidgets.NewPasswordInputWidget): value = ''
    class newUser(Webwidgets.ButtonInputWidget):
        title = 'Add'
        def clicked(self):
            objs = self.parent.children
            try:
                result = self.program.__._getpath(path=['create', 'user'] + list(self.winId[0][1:])
                                                  )(Grimoire.Types.UsernameType(objs['newUserName'].value),
                                                    Grimoire.Types.NewPasswordType(objs['newUserPassword'].value),
                                                    Grimoire.Types.NonemptyUnicodeType(objs['newUserSurName'].value),
                                                    Grimoire.Types.NonemptyUnicodeType(objs['newUserGivenName'].value))
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
            self.parent.update()
            objs['newUserName'].value = ''
            objs['newUserGivenName'].value = ''
            objs['newUserSurName'].value = ''
            objs['newUserPassword'].value = ''

    class currentGroup(Webwidgets.HtmlWidget):
        html = "%(group)s"
        def __init__(self, program, winId):
            if winId[0][1:]:
                group = str(Grimoire.Types.GrimoirePath(winId[0][1:]))
            else:
                group = "Top level department"
            Webwidgets.HtmlWidget.__init__(self, program, winId, group = group)

    class groupListing(Webwidgets.HtmlWidget):
        html = """
        <div id="%(id)s">
         <h2>Sub-departments</h2>
         %(upDir)s
         %(listing)s
        </div>
        """

        def update(self):
            self.children['listing'].update()

        class upDir(Webwidgets.ButtonInputWidget):
            title = 'Go to parent department'
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
                                   path=['introspection', 'dir', 'create', 'user'] + list(self.winId[0][1:]))(1)
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
                            head="Really delete user?"
                            class body(Webwidgets.HtmlWidget):
                                html = 'Do you really want to delete %s' % self.parent.name
                            def clicked(self, yes):
                                 Webwidgets.DialogWidget.clicked(self, yes)
                                 if int(yes):
                                     try:
                                         result = self.program.__._getpath(
                                             path=['delete', 'home group'] + list(self.winId[0][1:]) + [self.entry.name])()
                                     except Exception, result:
                                         traceback.print_exc()
                                     self.parent.children['message'].children['message'] = result and str(result)
                                     self.entry.parent.update()
                        self.parent.parent.parent.parent.parent.children['dialog'] = Dialog(self.program, self.winId)
                    
                def __init__(self, program, winId, **attrs):
                    Webwidgets.HtmlWidget.__init__(self, program, winId, **attrs)
                    self.children['goTo'] = self.GoTo(program, winId, title = self.name)

    class userListing(Webwidgets.HtmlWidget):
        html = """
        <div id="%(id)s">
         <h2>Users in this department</h2>
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
                                   path=['introspection', 'dir', 'change', 'user'] + list(self.winId[0][1:]))(1)
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
                  %(goTo)s
                 </td>
                 <td>
                  %(delete)s
                 </td>
                </tr>"""
                def __init__(self, program, winId, **attrs):
                    Webwidgets.HtmlWidget.__init__(self, program, winId, **attrs)
                    self.children['goTo'] = self.GoTo(program, winId, title = self.name)
                class GoTo(Webwidgets.ButtonInputWidget):
                    __explicit_load__ = True
                    def clicked(self):
                        self.program.redirectToWindow(self.winId[0] + ('Group users', self.title), self.winId[1])
                class delete(Webwidgets.ButtonInputWidget):
                    title='Delete'
                    def clicked(self):
                        class Dialog(Webwidgets.DialogWidget):
                            entry = self.parent
                            head="Really delete user?"
                            class body(Webwidgets.HtmlWidget):
                                html = 'Do you really want to delete %s' % self.parent.name
                            def clicked(self, yes):
                                 Webwidgets.DialogWidget.clicked(self, yes)
                                 if int(yes):
                                     try:
                                         result = self.program.__._getpath(
                                             path=['delete', 'user'] + list(self.winId[0][1:]) + [self.entry.name])()
                                     except Exception, result:
                                         traceback.print_exc()
                                     self.parent.children['message'].children['message'] = result and str(result)
                                     self.entry.parent.update()
                        self.parent.parent.parent.parent.parent.children['dialog'] = Dialog(self.program, self.winId)



