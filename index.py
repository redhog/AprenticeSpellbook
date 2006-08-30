import Webwidgets, Grimoire, traceback
from Modules import LogIn, HomeGroup, Group, User, EmailAlias, VpnAccounts, AdslConfig, AdslAccountConfig, Self

class index(Webwidgets.Program):
    def __init__(self, *args, **kws):
        Webwidgets.Program.__init__(self, *args, **kws)
        self._ = None
        self.__ = None
        
    def newWindow(self, winId):
        print winId
        if winId[0][0] == 'log in':
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

            def __init__(self, program, winId):
                if winId[0][0] == 'Self':
                    main = Self.Self(program, winId)
                elif winId[0][0] == 'Users':
                    if len(winId[0]) > 0 and winId[0][-1] == 'Group users':
                        program.redirectToWindow(winId[0][:-1], winId[1])
                        raise Webwidgets.OutputGiven
                    if len(winId[0]) > 1 and winId[0][-2] == 'Group users':
                        main = User.User(program, winId)
                    else:
                        main = HomeGroup.HomeGroup(program, winId)
                elif winId[0][0] == 'Groups':
                    main = Group.Group(program, winId)
                elif winId[0][0] == 'Email aliases':
                    main = EmailAlias.EmailAlias(program, winId)
                elif winId[0][0] == 'VPN Accounts':
                    main = VpnAccounts.VpnAccounts(program, winId)
                elif winId[0][0] == 'ADSL Config':
                    if len(winId[0]) == 1:
                        main = AdslConfig.AdslConfig(program, winId)
                    elif len(winId[0]) == 2:
                        main = AdslAccountConfig.AdslAccountConfig(program, winId)
                    else:
                        raise Webwidgets.OutputGiven
                elif winId[0][0] == 'Log out':
                    program._ = None
                    program.redirectToWindow(['log in'], {})
                    raise Webwidgets.OutputGiven
                else:
                    main = self.__class__.menu(program, winId)
                    #raise Webwidgets.OutputGiven
                Webwidgets.HtmlWidget.__init__(self, program, winId, main = main)

            class curWindow(Webwidgets.WindowPathList): pass

            class menu(Webwidgets.HtmlWidget):
                __children__ = Webwidgets.HtmlWidget.__children__ + ('Users', 'Groups', 'EmailAliases', 'LogOut')
                html = """<div id="%(id)s-main">
                           %(Me)s
                           %(Users)s
                           %(Groups)s
                           %(EmailAliases)s
                           %(VpnAccounts)s
                           %(AdslConfig)s
                           %(LogOut)s
                          </div>
                          """

                class Me(Webwidgets.ButtonInputWidget):
                    title = 'Me'
                    def clicked(self): self.program.redirectToWindow(['Self'], {})

                class Users(Webwidgets.ButtonInputWidget):
                    title = 'Users'
                    def clicked(self): self.program.redirectToWindow(['Users'], {})

                class Groups(Webwidgets.ButtonInputWidget):
                    title = 'Groups'
                    def clicked(self): self.program.redirectToWindow(['Groups'], {})

                class EmailAliases(Webwidgets.ButtonInputWidget):
                    title = 'Email aliases'
                    def clicked(self): self.program.redirectToWindow(['Email aliases'], {})

                class VpnAccounts(Webwidgets.ButtonInputWidget):
                    title = 'VPN Accounts'
                    def clicked(self): self.program.redirectToWindow(['VPN Accounts'], {})

                class AdslConfig(Webwidgets.ButtonInputWidget):
                    title = 'ADSL Config'
                    def clicked(self): self.program.redirectToWindow(['ADSL Config'], {})

                class LogOut(Webwidgets.ButtonInputWidget):
                    title = 'Log out'
                    def clicked(self): self.program.redirectToWindow(['Log out'], {})
                
            class message(Webwidgets.Message): pass

            class dialog(Webwidgets.DialogWidget):
                buttons = {}
                body = head = ''
                visible=False
