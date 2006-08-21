import Webwidgets, Grimoire, traceback
import LogIn, HomeGroup, Group, User

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
                if winId[0][0] == 'Users':
                    if len(winId[0]) > 0 and winId[0][-1] == 'Group users':
                        program.redirectToWindow(winId[0][:-1], winId[1])
                        raise Webwidgets.OutputGiven
                    if len(winId[0]) > 1 and winId[0][-2] == 'Group users':
                        main = User.User(program, winId)
                    else:
                        main = HomeGroup.HomeGroup(program, winId)
                elif winId[0][0] == 'Groups':
                    main = Group.Group(program, winId)
                else:
                    main = ''
                    #raise Webwidgets.OutputGiven
                Webwidgets.HtmlWidget.__init__(self, program, winId, main = main)

            class curWindow(Webwidgets.WindowPathList): pass

            class menu(Webwidgets.HtmlWidget):
                __children__ = Webwidgets.HtmlWidget.__children__ + ('HomeGroup', 'Group', 'LogOut')
                html = """<div id="%(id)s-main">
                           %(HomeGroup)s
                           %(Group)s
                           %(LogOut)s
                          </div>
                          """

                class HomeGroup(Webwidgets.ButtonInputWidget):
                    title = 'Users'
                    def clicked(self): self.program.redirectToWindow(['Users'], {})

                class Group(Webwidgets.ButtonInputWidget):
                    title = 'Groups'
                    def clicked(self): self.program.redirectToWindow(['Groups'], {})

                class LogOut(Webwidgets.ButtonInputWidget):
                    title = 'Log out'
                    def clicked(self): self.program.redirectToWindow(['log out'], {})
                
            class message(Webwidgets.Message): pass

            class dialog(Webwidgets.DialogWidget):
                buttons = {}
                body = head = ''
                visible=False
