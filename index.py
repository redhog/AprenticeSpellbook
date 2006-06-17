import Webwidgets
import Grimoire
import traceback
       
class index(Webwidgets.Program):
    class Main(Webwidgets.Window):
        headers={'Content-Type': 'text/html',
                 'Status': '202 Page loaded'}

        title = 'Log in'

        class head(Webwidgets.StyleLink): style = 'Spellbook.css'

        class body(Webwidgets.HtmlWidget):
            html = """
            %(message)s
            %(dialog)s
            <div id="%(id)s-main">%(main)s</div>
            """

            class message(Webwidgets.HtmlWidget):
                __children__ = Webwidgets.HtmlWidget.__children__ + ('message',)
                message = ''
                def draw(self, path):
                    if self.children['message']:
                        self.html = '<div id="%(id)s">%(message)s</div>'
                    else:
                        self.html = ''
                    return Webwidgets.HtmlWidget.draw(self, path)
                    
            class dialog(Webwidgets.HtmlWidget): html = ''

            class Dialog(Webwidgets.HtmlWidget):
                __explicit_load__ = True
                html = """<div class="dialog">
                 <div>%(question)s</div>
                 <div>%(no)s%(yes)s</div>
                </div>
                """
                class no(Webwidgets.ButtonInputWidget):
                    title = 'No'
                    def clicked(self):
                        self.parent.notify('clicked', False)
                        return True
                class yes(Webwidgets.ButtonInputWidget):
                    title = 'Yes'
                    def clicked(self):
                        self.parent.notify('clicked', True)
                        return True
                def clicked(self, yes):
                    self.parent.children[self.name] = ''
                
            class main(Webwidgets.HtmlWidget):
                html = """<div class="login">
                 <div>Username: %(username)s</div>
                 <div>Password: %(password)s</div>
                 <div>%(logIn)s</div>
                </div>
                """

                class username(Webwidgets.StringInputWidget): value = ''
                class password(Webwidgets.PasswordInputWidget): value = ''
                class logIn(Webwidgets.ButtonInputWidget):
                    title = 'Log in'
                    def clicked(self):
                        try:
                            tree = Grimoire._.trees.local.ldap(self.parent.children['username'].value,
                                                               self.parent.children['password'].value)
                            self.parent.parent.children['message'].children['message'] = Grimoire.Types.getComment(tree) and str(Grimoire.Types.getComment(tree))
                            self.parent.parent.children['main'] = self.parent.parent.GrimoireSession(
                                Grimoire.Types.getValue(tree))
                        except Exception, e:
                            traceback.print_exc()
                            self.parent.parent.children['message'].children['message'] = e and str(e)
            
            class GrimoireSession(Webwidgets.HtmlWidget):
                __explicit_load__ = True
                html = """
                <h1>%(curGroup)s</h1>
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
                 <div class="groupListing">%(groupListing)s</div>
                 <div class="userListing">%(userListing)s</div>
                </div>
                """

                class newGroupName(Webwidgets.StringInputWidget): value = ''
                class newGroup(Webwidgets.ButtonInputWidget):
                    title = 'Add'
                    def clicked(self):
                        try:
                            result = self.parent.__._getpath(path=['create', 'home group'] + self.parent.path
                                                             )(self.parent.children['newGroupName'].value)
                        except Exception, result:
                            traceback.print_exc()
                        self.parent.parent.children['message'].children['message'] = result and str(result)
                        self.parent.changeGroup(self.parent.path)
                        self.parent.children['newGroupName'].value = ''

                class newUserName(Webwidgets.StringInputWidget): value = ''
                class newUserGivenName(Webwidgets.StringInputWidget): value = ''
                class newUserSurName(Webwidgets.StringInputWidget): value = ''
                class newUserPassword(Webwidgets.NewPasswordInputWidget): value = ''
                class newUser(Webwidgets.ButtonInputWidget):
                    title = 'Add'
                    def clicked(self):
                        objs = self.parent.children
                        try:
                            result = self.parent.__._getpath(path=['create', 'user'] + self.parent.path
                                                             )(Grimoire.Types.UsernameType(objs['newUserName'].value),
                                                               Grimoire.Types.NewPasswordType(objs['newUserPassword'].value),
                                                               Grimoire.Types.NonemptyUnicodeType(objs['newUserSurName'].value),
                                                               Grimoire.Types.NonemptyUnicodeType(objs['newUserGivenName'].value))
                        except Exception, result:
                            traceback.print_exc()
                        self.parent.parent.children['message'].children['message'] = result and str(result)
                        self.parent.changeGroup(self.parent.path)
                        objs['newUserName'].value = ''
                        objs['newUserGivenName'].value = ''
                        objs['newUserSurName'].value = ''
                        objs['newUserPassword'].value = ''

                class GroupListing(Webwidgets.HtmlWidget):
                    __explicit_load__ = True
                    html = """
                    <div id="%(id)s">
                     <h2>Groups</h2>
                     %(upDir)s
                     %(listing)s
                    </div>
                    """
                    class upDir(Webwidgets.ButtonInputWidget):
                        title = 'Go to parent group'
                        def clicked(self):
                            self.parent.parent.changeGroup(self.parent.parent.path[:-1])
                    class Listing(Webwidgets.ListWidget):
                        __explicit_load__ = True
                        __attributes__ = Webwidgets.ListWidget.__attributes__ + ('session',)
                        class Entry(Webwidgets.HtmlWidget):
                            __explicit_load__ = True
                            __children__ = Webwidgets.HtmlWidget.__children__ + ('name',)
                            html = """
                            <tr>
                             <td>
                              %(name)s
                             </td>
                             <td>
                              %(goTo)s
                             </td>
                             <td>
                              %(delete)s
                             </td>
                            </tr>"""
                            class goTo(Webwidgets.ButtonInputWidget):
                                title='Go to'
                                def clicked(self):
                                    self.parent.parent.parent.parent.changeGroup(self.parent.parent.parent.parent.path + [self.parent.name])
                            class delete(Webwidgets.ButtonInputWidget): title='Delete'

                        pre = "<table>"
                        sep = '\n'
                        post = "</table>"

                        def __init__(self, **attrs):
                            Webwidgets.ListWidget.__init__(self, **attrs)
                            self.update()

                        def update(self):
                            entries = set([path[0]
                                           for leaf, path in self.session.__._getpath(
                                               path=['introspection', 'dir', 'create', 'user'] + self.session.path)(1)
                                           if leaf and len(path) == 1])
                            self.children.clear()
                            self.children['pre'] = self.pre
                            self.children['sep'] = self.sep
                            self.children['post'] = self.post
                            self.children.update(
                                dict([(str(name), self.Entry(name=name))
                                      for name in entries]))
                            
                    def __init__(self, session, **attrs):
                        Webwidgets.HtmlWidget.__init__(
                            self,
                            listing = self.Listing(session = session),
                            **attrs)

                    def update(self):
                        self.children['listing'].update()
                        
                class UserListing(Webwidgets.HtmlWidget):
                    __explicit_load__ = True
                    html = """
                    <div id="%(id)s">
                     <h2>Users</h2>
                     %(listing)s
                    </div>
                    """
                    class Listing(Webwidgets.ListWidget):
                        __explicit_load__ = True
                        __attributes__ = Webwidgets.ListWidget.__attributes__ + ('session',)
                        class Entry(Webwidgets.HtmlWidget):
                            __explicit_load__ = True
                            __children__ = Webwidgets.HtmlWidget.__children__ + ('name',)
                            html = """
                            <tr>
                             <td>
                              %(name)s
                             </td>
                             <td>
                              %(edit)s
                             </td>
                             <td>
                              %(delete)s
                             </td>
                            </tr>"""
                            class edit(Webwidgets.ButtonInputWidget): title='Edit'
                            class delete(Webwidgets.ButtonInputWidget):
                                title='Delete'
                                def clicked(self):
                                    DialogWidget = self.parent.parent.parent.parent.parent.Dialog
                                    class Dialog(DialogWidget):
                                        entry = self.parent
                                        class question(Webwidgets.HtmlWidget):
                                            html = 'Do you really want to delete %s' % self.parent.name
                                        def clicked(self, yes):
                                             DialogWidget.clicked(self, yes)
                                             if yes:
                                                 try:
                                                     result = self.entry.parent.session.__._getpath(
                                                         path=['delete', 'user'] + self.entry.parent.session.path + [self.entry.name])()
                                                 except Exception, result:
                                                     traceback.print_exc()
                                                 self.parent.children['message'].children['message'] = result and str(result)
                                                 self.entry.parent.session.changeGroup(self.entry.parent.session.path)
                                    self.parent.parent.parent.parent.parent.children['dialog'] = Dialog()
                                    
                        pre = "<table>"
                        sep = '\n'
                        post = "</table>"

                        def __init__(self, **attrs):
                            Webwidgets.ListWidget.__init__(self, **attrs)
                            self.update()

                        def update(self):
                            entries = set([path[0]
                                           for leaf, path in self.session.__._getpath(
                                               path=['introspection', 'dir', 'change', 'user'] + self.session.path)(1)
                                           if leaf and len(path) == 1])
                            self.children.clear()
                            self.children['pre'] = self.pre
                            self.children['sep'] = self.sep
                            self.children['post'] = self.post
                            self.children.update(
                                dict([(str(name), self.Entry(name=name))
                                      for name in entries]))
                            
                    def __init__(self, session, **attrs):
                        Webwidgets.HtmlWidget.__init__(
                            self,
                            listing = self.Listing(session = session),
                            **attrs)

                    def update(self):
                        self.children['listing'].update()
                
                def __init__(self, tree):
                    self._ = Grimoire.Performer.Logical(tree)
                    self.__ = Grimoire.Performer.Physical(tree)
                    self.path = []
                    Webwidgets.HtmlWidget.__init__(self,
                                                   groupListing = self.GroupListing(session=self),
                                                   userListing = self.UserListing(session=self),
                                                   curGroup = 'Home groups &gt;&gt; ' + ' &gt;&gt; '.join(self.path))

                def changeGroup(self, path):
                    self.path = path
                    self.children['curGroup'] = 'Home groups &gt;&gt; ' + ' &gt;&gt; '.join(self.path)
                    self.children['groupListing'].update()
                    self.children['userListing'].update()
                
    def newWindow(self, winId):
        return self.Main()
