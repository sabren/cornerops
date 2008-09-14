import unittest
import personas
from platonic import Model
from cornerhost.features import panel

class ControlPanelFeatureTest(unittest.TestCase):

    def test_error(self):
        
        class ThrowFeature(panel.ControlPanelFeature):
            def invoke(self, _req):
                raise ValueError
            
        self.assertRaises(ValueError, ThrowFeature().invoke, _req={})


    def test_handle(self):
        class EmptyFeature(panel.ControlPanelFeature):
            def invoke(self, value, default='world!'):
                return Model(x=value, y=default)

        model = EmptyFeature().invoke(value='hello!')
        self.assertEquals(model["x"], "hello!")
        self.assertEquals(model["y"], "world!")

if __name__=="__main__":
    unittest.main()

