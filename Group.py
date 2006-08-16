import Webwidgets, Grimoire, traceback

class Group(Webwidgets.HtmlWidget):
    html = """
    <div class="actions">
     <div class="newGroup">
      <h2>New group</h2>
      <div>Group name: %(newGroupName)s</div>
      <div>%(newGroup)s</div>
     </div>
     <div class="newMember">
      <h2>Add member</h2>
      <div>User name: %(addMemberName)s</div>
      <div>%(addMember)s</div>
     </div>
    </div>
    <div class="listings">
     <div class="groupListing">%(groupListing)s</div>
    </div>
    """

    def update(self):
        self.children['groupListing'].update()

    class newGroupName(Webwidgets.StringInputWidget): value = ''
    class newGroup(Webwidgets.ButtonInputWidget):
        title = 'Add'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['create', 'group'] + list(self.winId[0][1:])
                                                  )(self.parent.children['newGroupName'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
            self.parent.children['newGroupName'].value = ''
            self.parent.update()

    class addMemberName(Webwidgets.StringInputWidget): value = ''
    class addMember(Webwidgets.ButtonInputWidget):
        title = 'Add'
        def clicked(self):
            try:
                result = self.program.__._getpath(path=['change', 'group', 'add member'] + list(self.winId[0][1:])
                                                  )(self.parent.children['newGroupName'].value)
            except Exception, result:
                traceback.print_exc()
            self.parent.parent.children['message'].children['message'] = result and str(result)
            self.parent.children['addMemberName'].value = ''
            self.parent.update()

    class groupListing(Webwidgets.HtmlWidget):
        html = """
        <div id="%(id)s">
         <h2>Groups</h2>
         %(upDir)s
         %(listing)s
        </div>
        """

        def update(self):
            self.children['listing'].update()

        class upDir(Webwidgets.ButtonInputWidget):
            title = 'Go to parent group'
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
                                   path=['introspection', 'dir', 'create', 'group'] + list(self.winId[0][1:]))(1)
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
                class delete(Webwidgets.ButtonInputWidget): title='Delete'
                def __init__(self, program, winId, **attrs):
                    Webwidgets.HtmlWidget.__init__(self, program, winId, **attrs)
                    self.children['goTo'] = self.GoTo(program, winId, title = self.name)
