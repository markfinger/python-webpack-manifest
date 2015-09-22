import os
import unittest
from webpack_manifest import webpack_manifest

TEST_ROOT = os.path.dirname(__file__)


class TestBundles(unittest.TestCase):
    def test_raises_exception_for_missing_manifest(self):
        self.assertRaises(
            webpack_manifest.WebpackManifestFileError,
            webpack_manifest.read_file,
            '/path/that/does/not/exist',
        )

    def test_manifest_provide_rendered_elements(self):
        manifest = webpack_manifest.load(
            os.path.join(TEST_ROOT, 'test_manifest_1.json'),
            static_url='/static/',
        )
        self.assertEqual(manifest.main.js, '<script src="/static/foo/bar.js"></script>')
        self.assertEqual(manifest.main.css, '<link rel="stylesheet" href="/static/woz/bar.css">')

        self.assertEqual(
            manifest.foo.js,
            (
                '<script src="/static/foo/bar.js"></script>'
                '<script src="/static/woz/bar.js"></script>'
                '<script src="/static/bar/woz.js"></script>'
            )
        )
        self.assertEqual(manifest.foo.css, '')

        self.assertEqual(manifest.bar.js, '<script src="/static/bar/woz.js"></script>')
        self.assertEqual(
            manifest.bar.css,
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
        self.assertEqual(manifest.main.js, '<script src="/static/foo/bar.js"></script>')
        self.assertEqual(manifest.main.css, '<link rel="stylesheet" href="/static/woz/bar.css">')

    def test_errors_handled(self):
        try:
            webpack_manifest.load(
                os.path.join(TEST_ROOT, 'test_manifest_2.json'),
                static_url='/static',
            )
            self.assertFalse('should not reach this')
        except webpack_manifest.WebpackError as e:
            self.assertEqual(
                e.message,
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
                e.message,
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
                e.message,
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
                e.message,
                'Unknown webpack manifest status: "unknown status"',
            )
