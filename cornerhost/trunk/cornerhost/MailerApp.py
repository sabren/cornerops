from sixthday import App
from strongbox import BoxView
from duckbill import *
from cornerhost import *
import zebra
from handy import sendmail

class MailerApp(App):

    def __init__(self, req, clerk):
        super(MailerApp, self).__init__(req)
        self.clerk = clerk

    def fetchUserAndAccount(self):
        try:
            u = self.clerk.match(User, username=self.input["who"])[0]
            a = u.account
        except Exception, e:
            if self.input.get("who"):
                err = "couldn't load user %s: %s" % (self.input["who"], e)
            else:
                err = "no username given"
            print >> self, "ERROR:", err
            raise Exception, err
        return a, u

    def act_welcome(self):
        try:
            a,u = self.fetchUserAndAccount()
        except:
            return

        self.model.update(BoxView(a))
        self.model.update(BoxView(u))
        self.model["shortname"] = u.server.shortname
        self.model["message"] = zebra.fetch("eml_welcome", self.model) 
        self.model["subject"] = "Welcome to Cornerhost!"
        self.model["bcc"] = "michal@sabren.com"
        print >> self, zebra.fetch("frm_mailer", self.model)

    def act_send(self):
        msg_from = self.input["from"]
        msg_to = self.input["to"]
        msg = self.input["message"]
        cc = self.input["cc"]
        bcc = self.input["bcc"]
        subject = self.input["subject"]

        sendmail("From: %s\nTo: %s\nCC: %s\nBCC: %s\nSubject: %s\n%s" \
                 % (msg_from, msg_to, cc, bcc, subject, msg))

        print >> self, zebra.fetch("../skin/header.zb", self.model)
        print >> self, "message sent!"
        print >> self, zebra.fetch("../skin/footer.zb", self.model)
        
