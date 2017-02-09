import os
import unittest
from webpack_manifest import webpack_manifest

TEST_ROOT = os.path.dirname(__file__)


class TestBundles(unittest.TestCase):
    def test_raises_exception_for_missing_manifest(self):
        self.assertRaises(
            webpack_manifest.WebpackManifestFileError,
            webpack_manifest.read,
            '/path/that/does/not/exist',
            None,
        )

    def test_manifest_entry_object_string_conversion(self):
        manifest = webpack_manifest.load(
            os.path.join(TEST_ROOT, 'test_manifest_1.json'),
            static_url='/static/',
        )
        self.assertEqual(str(manifest.main.js), manifest.main.js.output)
        self.assertEqual(str(manifest.main.css), manifest.main.css.output)

    def test_manifest_provide_rendered_elements(self):
        manifest = webpack_manifest.load(
            os.path.join(TEST_ROOT, 'test_manifest_1.json'),
            static_url='/static/',
        )
        self.assertEqual(manifest.main.js.output, '<script src="/static/foo/bar.js"></script>')
        self.assertEqual(manifest.main.css.output, '<link rel="stylesheet" href="/static/woz/bar.css">')

        self.assertEqual(
            manifest.foo.js.output,
            (
                '<script src="/static/foo/bar.js"></script>'
                '<script src="/static/woz/bar.js"></script>'
                '<script src="/static/bar/woz.js"></script>'
            )
        )
        self.assertEqual(manifest.foo.css.output, '')

        self.assertEqual(manifest.bar.js.output, '<script src="/static/bar/woz.js"></script>')
        self.assertEqual(
            manifest.bar.css.output,
            (
                '<link rel="stylesheet" href="/static/foo/bar.css">'
                '<link rel="stylesheet" href="/static/woz/bar.css">'
            )
        )

    def test_non_trailing_slash_static_url_handled(self):
        manifest = webpack_manifest.load(
            os.path.join(TEST_ROOT, 'test_manifest_1.json'),
            static_url='/static',
        )
        self.assertEqual(manifest.main.js.output, '<script src="/static/foo/bar.js"></script>')
        self.assertEqual(manifest.main.css.output, '<link rel="stylesheet" href="/static/woz/bar.css">')

    def test_rel_urls(self):
        manifest = webpack_manifest.load(
            os.path.join(TEST_ROOT, 'test_manifest_1.json'),
            static_url='/static/',
            static_root=os.path.dirname(__file__),
        )
        self.assertEqual(manifest.foo.js.rel_urls, ['foo/bar.js', 'woz/bar.js', 'bar/woz.js'])
        self.assertEqual(manifest.foo.css.rel_urls, [])
        self.assertEqual(manifest.bar.css.rel_urls, ['foo/bar.css', 'woz/bar.css'])

    def test_legacy_rel_urls(self):
        manifest = webpack_manifest.load(
            os.path.join(TEST_ROOT, 'test_manifest_1.json'),
            static_url='/static/',
            static_root=os.path.dirname(__file__),
        )
        self.assertEqual(manifest.foo.rel_js, ['foo/bar.js', 'woz/bar.js', 'bar/woz.js'])
        self.assertEqual(manifest.bar.rel_css, ['foo/bar.css', 'woz/bar.css'])
 
    def test_missing_static_root_handled(self):
        try:
            manifest = webpack_manifest.load(
                os.path.join(TEST_ROOT, 'test_manifest_1.json'),
                static_url='/static/',
                debug=True,
            )
            manifest.main.js.content
            self.assertFalse('should not reach this')
        except webpack_manifest.WebpackManifestConfigError as e:
            self.assertEqual(
                e.args[0],
                'Provide static_root to access webpack entry content.',
            )

    def test_content_output(self):
        manifest = webpack_manifest.load(
            os.path.join(TEST_ROOT, 'test_manifest_1.json'),
            static_url='/static/',
            static_root=os.path.dirname(__file__),
            debug=True,
        )
        self.assertEqual(manifest.foo.js.content, 'foo_bar=1\n\nwoz_bar=1\n\nbar_woz=1\n')
        self.assertEqual(manifest.foo.css.content, '')
        self.assertEqual(manifest.bar.css.content, '.foo_bar {}\n\n.woz_bar {}\n')

    def test_content_inline(self):
        manifest = webpack_manifest.load(
            os.path.join(TEST_ROOT, 'test_manifest_1.json'),
            static_url='/static/',
            static_root=os.path.dirname(__file__),
            debug=True,
        )
        self.assertEqual(manifest.foo.js.inline, '<script>foo_bar=1\n\nwoz_bar=1\n\nbar_woz=1\n</script>')
        self.assertEqual(manifest.foo.css.inline, '')
        self.assertEqual(manifest.bar.css.inline, '<style>.foo_bar {}\n\n.woz_bar {}\n</style>')

    def test_errors_handled(self):
        try:
            webpack_manifest.load(
                os.path.join(TEST_ROOT, 'test_manifest_2.json'),
                static_url='/static',
            )
            self.assertFalse('should not reach this')
        except webpack_manifest.WebpackError as e:
            self.assertEqual(
                e.args[0],
                'Webpack errors: \n\nerror 1\n\nerror 2',
            )

    def test_status_handled(self):
        try:
            webpack_manifest.load(
                os.path.join(TEST_ROOT, 'test_manifest_2.json'),
                static_url='/static',
            )
            self.assertFalse('should not reach this')
        except webpack_manifest.WebpackError as e:
            self.assertEqual(
                e.args[0],
                'Webpack errors: \n\nerror 1\n\nerror 2',
            )

    def test_handles_timeouts_in_debug(self):
        path = os.path.join(TEST_ROOT, 'test_manifest_3.json')
        try:
            webpack_manifest.load(
                path,
                static_url='/static',
                debug=True,
                timeout=1,
            )
            self.assertFalse('should not reach this')
        except webpack_manifest.WebpackManifestBuildingStatusTimeout as e:
            self.assertEqual(
                e.args[0],
                'Timed out reading the webpack manifest at "{}"'.format(path),
            )

    def test_handles_unknown_statuses(self):
        path = os.path.join(TEST_ROOT, 'test_manifest_4.json')
        try:
            webpack_manifest.load(
                path,
                static_url='/static',
            )
            self.assertFalse('should not reach this')
        except webpack_manifest.WebpackManifestStatusError as e:
            self.assertEqual(
                e.args[0],
                'Unknown webpack manifest status: "unknown status"',
            )
