from zoidboard import plugins

class TestPlugins:
    def test_import_builtin_plugin(self):
        assert plugins.get('ip') is not None, \
               'Should have imported builtin plugin'

    def test_import_builtin_plugin_that_does_not_exist(self):
        assert plugins.get('qwerty') is None, \
               'Should have not have imported non existant builtin plugin'

    # def test_import_custom_plugin and non existant custom plugins
    # use pytest's temp directory to create custom plugin directory
    # monkey patch plugins.CUSTOM_PLUGIN_LOCATION
    ## better way of doing this without monkey patching?
