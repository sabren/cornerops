from platonic import Model, Intercept
import inspect

def signature(callable):
    """
    returns a list of arguments and a dict of default values
    """
    spec = inspect.getargspec(callable)
    need = spec[0]
    vals = spec[3]
    defaults = {}
    if vals:
        for k,v in zip(need[-len(vals):], vals):
            # this is important for fastCGI/etc:
            # (because default values are evaluated only once)
            assert type(v)!=list, "default lists are mutable! use tuples!"
            defaults[k]=v
    return need, defaults

def first_match(arg, *dicts):
    for d in dicts:
        if d.has_key(arg):
            return d[arg]
    raise TypeError("missing parameter: %s" % arg)


#@abstract
class ControlPanelFeature(object):
   
    def __init__(self, uclerk):
        self.clerk = uclerk.clerk
        self.user = uclerk.user

    def handle(self, req, res, sess):

        special = {
            "_req" : req ,
            "_res" : res ,
            "_sess": sess,
            "_user": self.user,
            "_clerk": self.clerk,
        }
        
        need, defaults = signature(self.invoke)
        if need[0]=="self":
            need.remove("self") # @TODO: work even without convention

        return self.invoke(*[first_match(arg, special, req, defaults)
                             for arg in need])

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
