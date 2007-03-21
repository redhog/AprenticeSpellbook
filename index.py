import Webwidgets, Grimoire, traceback
from Modules import LogIn, HomeGroup, Group, User, EmailAlias, VpnAccounts, AdslConfig, AdslAccountConfig, Me

class index(Webwidgets.Program):
    class Session(Webwidgets.Program.Session):
        def __init__(self, *args, **kws):
            Webwidgets.Program.Session.__init__(self, *args, **kws)
            self._ = None
            self.__ = None

        def newWindow(self, winId):
            print winId

            if winId[0] and winId[0][0] == 'log in':
                return LogIn.LogIn(self, winId)

            if self._ is None:
                self.redirectToWindow(['log in'], {})
                return None

            return self.Main(self, winId)

        class Main(Webwidgets.Window):
            headers={'Content-Type': 'text/html',
                     'Status': '200 Page loaded'}

            title = 'AprenticeSpellbook'

            class head(Webwidgets.StyleLink): style = 'Spellbook.css'

            class body(Webwidgets.HtmlWidget):
                html = """
                %(menu)s
                %(curWindow)s
                %(message)s
                %(dialog)s
                <div id="%(id)s-main">%(main)s</div>
                """

                def __init__(self, session, winId):
                    if winId[0][0] == 'Me':
                        main = Me.Me(session, winId)
                    elif winId[0][0] == 'Users':
                        if len(winId[0]) > 0 and winId[0][-1] == 'Group users':
                            session.redirectToWindow(winId[0][:-1], winId[1])
                            raise Webwidgets.OutputGiven
                        if len(winId[0]) > 1 and winId[0][-2] == 'Group users':
                            main = User.User(session, winId)
                        else:
                            main = HomeGroup.HomeGroup(session, winId)
                    elif winId[0][0] == 'Groups':
                        main = Group.Group(session, winId)
                    elif winId[0][0] == 'Email aliases':
                        main = EmailAlias.EmailAlias(session, winId)
                    elif winId[0][0] == 'VPN Accounts':
                        main = VpnAccounts.VpnAccounts(session, winId)
                    elif winId[0][0] == 'ADSL Config':
                        if len(winId[0]) == 1:
                            main = AdslConfig.AdslConfig(session, winId)
                        elif len(winId[0]) == 2:
                            main = AdslAccountConfig.AdslAccountConfig(session, winId)
                        else:
                            raise Webwidgets.OutputGiven
                    elif winId[0][0] == 'Log out':
                        program._ = None
                        session.redirectToWindow(['log in'], {})
                        raise Webwidgets.OutputGiven
                    else:
                        main = self.__class__.menu(session, winId)
                        #raise Webwidgets.OutputGiven
                    Webwidgets.HtmlWidget.__init__(self, session, winId, main = main)

                class curWindow(Webwidgets.WindowPathList): pass

                class menu(Webwidgets.ListWidget):
                    def __init__(self, session, winId):
                        menu = []
                        if len(session.__._getpath(path=['introspection', 'dir', 'change', 'own', 'password'])(1)) > 0:
                            menu.append('Me')
                        if len(session.__._getpath(path=['introspection', 'dir', 'create', 'user'])(1)) > 0:
                            menu.append('Users')
                        # FIXME: This should really check change.group.add\ member too!
                        if len(session.__._getpath(path=['introspection', 'dir', 'create', 'group'])(1)) > 0:
                            menu.append('Groups')
                        if len(session.__._getpath(path=['introspection', 'dir', 'create', 'emailalias'])(1)) > 0:
                            menu.append('Email aliases')
                        if len(session.__._getpath(path=['introspection', 'dir', 'create', 'emailalias'])(1)) > 0:
                            menu.append('Email aliases')
                        if len(session.__._getpath(path=['introspection', 'dir', 'create', 'vpn', 'account'])(1)) > 0:
                            menu.append('VPN Accounts')
                        if len(session.__._getpath(path=['introspection', 'dir', 'create', 'adsl', 'peer'])(1)) > 0:
                            menu.append('ADSL Config')
                        menu.append('Log out')
                        Webwidgets.ListWidget.__init__(
                            self, session, winId,
                            **dict([(name, self.Button(session, winId, title=name)) for name in menu]))
                        
                    class Button(Webwidgets.ButtonInputWidget):
                        __explicit_load__ = True
                        def clicked(self): self.session.redirectToWindow([self.title], {})

                class message(Webwidgets.Message): pass

                class dialog(Webwidgets.DialogWidget):
                    buttons = {}
                    body = head = ''
                    visible=False
