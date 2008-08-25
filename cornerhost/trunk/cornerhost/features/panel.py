from platonic import Model

#@abstract
class ControlPanelFeature(object):
           
    def invoke(self):
        raise NotImplementedError
    
    def buildErrorMessage(self, e):
        if len(e.args)==1:
            return e[0]
        else:
            field, value = e[0], e[1]
            return "invalid %s: %s" % e #(field, value)


def extractNewPass(pass1, pass2):
    if pass1!=pass2:
        raise ValueError("passwords didn't match")
    if not pass1:
        raise ValueError("password must not be empty")
    return pass1

    

class EmptyModel(ControlPanelFeature):
    def invoke(self):
        return Model()
