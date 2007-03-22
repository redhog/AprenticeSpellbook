import Webwidgets, Grimoire, traceback

class LogIn(Webwidgets.Window):
    headers={'Content-Type': 'text/html',
             'Status': '200 Page loaded'}

    title = 'AprenticeSpellbook - Log in'

    class head(Webwidgets.StyleLink): style = 'Spellbook.css'    

    class body(Webwidgets.HtmlWidget):
        html = """
        %(message)s
        %(dialog)s
        """

        class message(Webwidgets.Message): pass
        
        class dialog(Webwidgets.DialogWidget):
            buttons = {'Log in':'1'}
            head = "Log in to the aprentice' spellbook"

            class body(Webwidgets.HtmlWidget):
                html = """<div class="login">
                           <div>Username: %(username)s</div>
                           <div>Password: %(password)s</div>
                          </div>
                          """

                class username(Webwidgets.StringInputWidget): value = ''
                class password(Webwidgets.PasswordInputWidget): value = ''

            def clicked(self, path, value):
                try:
                    tree = Grimoire._.trees.local.ldap(self.children['body'].children['username'].value,
                                                       self.children['body'].children['password'].value)
                    self.parent.children['message'].children['message'] = Grimoire.Types.getComment(tree) and str(Grimoire.Types.getComment(tree))
                    self.session.__ = Grimoire.Performer.Physical(Grimoire.Types.getValue(tree))
                    self.session._ = Grimoire.Performer.Logical(self.session.__)
                    self.session.redirectToWindow(['Users'], {})
                except Exception, e:
                    traceback.print_exc()
                    self.parent.children['message'].children['message'] = e and str(e)
