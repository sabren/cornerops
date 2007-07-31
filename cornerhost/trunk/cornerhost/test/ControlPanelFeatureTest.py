import unittest
import personas
from platonic import Model
from cornerhost.features import panel

class ControlPanelFeatureTest(unittest.TestCase):

    def test_error(self):
        
        class ThrowFeature(panel.ControlPanelFeature):
            def invoke(self, _req):
                raise ValueError
            
        uclerk = personas.fredClerk()
        self.assertRaises(ValueError,
            ThrowFeature(uclerk).handle, req={}, res=None, sess=None)


    def test_handle(self):
        class EmptyFeature(panel.ControlPanelFeature):
            def invoke(self, value, default='world!'):
                return Model(x=value, y=default)

        uclerk = personas.fredClerk()
        model = EmptyFeature(uclerk).handle({"value":"hello!"}, None, None) 
        self.assertEquals(model["x"], "hello!")
        self.assertEquals(model["y"], "world!")

if __name__=="__main__":
    unittest.main()

