from django.test import TestCase

from turbion.core.utils import spot

class BasePlugin(object):
    def hello(self):
        return 'Hello from %s' % self.name

class PluginManager(spot.Manager):
    def load(self):
        pass

Plugin = spot.create(BasePlugin, manager=PluginManager, cache=False)

class PlugA(Plugin):
    name = 'plug_a'

class PlugB(Plugin):
    pass

class SpotTest(TestCase):
    def setUp(self):
        pass

    def test_all_plugins(self):
        self.assertEqual(
            sorted([name for name, obj in Plugin.manager.all()]),
            ['plug_a', 'plug_b']
        )

    def test_get_plugin(self):
        plug = Plugin.manager.get('plug_a')

        self.assert_(isinstance(plug, Plugin))
        self.assertEqual(plug.hello(), 'Hello from plug_a')

    def test_fresh(self):
        plug1 = Plugin.manager.get('plug_a')
        plug2 = Plugin.manager.get('plug_a')

        self.assert_(plug1 != plug2)

    def test_is_loaded(self):
        Plugin.manager.get('plug_a')
        self.assert_(Plugin.manager.is_loaded())
