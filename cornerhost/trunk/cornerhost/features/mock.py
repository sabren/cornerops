
"""
>>> class Original(object):
...    def doSomething():
...         return 0
...
>>> maker = MockMaker(Original)
>>> maker.expects.doSomething()
>>> maker.returns(None)
>>> maker.expects.doSomethingElse()
TypeError
>>> mock = make.getMock()
"""

class MockMethod(object):
    def __call__(self, *args, **kw):
        pass

class MockMethodMaker(objet):
    def __getattr_(self, name):
        return Mock

class Mock:
    def __getattr__(self, name):
        self.mock._record(name, MockMethod())

class MockMaker:
    def __init__(self, klass):
        self.klass = klass
        self.mock = Mock()
        self.mock.script = []
        self.expects = MockMethodMaker()
        
    def returns(self, result):
        self.mock(result) == 5



if __name__=="__main__":
    import doctest, mock
    doctest.testmod(mock)
