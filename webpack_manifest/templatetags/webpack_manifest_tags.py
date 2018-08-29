from django import template
from django.conf import settings
from webpack_manifest import webpack_manifest

if not hasattr(settings, 'WEBPACK_MANIFEST'):
    raise webpack_manifest.WebpackManifestConfigError('`WEBPACK_MANIFEST` has not been defined in settings')

if 'manifests' not in settings.WEBPACK_MANIFEST:
    raise webpack_manifest.WebpackManifestConfigError(
        '`WEBPACK_MANIFEST[\'manifests\']` has not been defined in settings'
    )

register = template.Library()


@register.simple_tag
def load_webpack_manifest(name):
    if name not in settings.WEBPACK_MANIFEST['manifests']:
        raise webpack_manifest.WebpackManifestConfigError(
            '"%s" has not been defined in `WEBPACK_MANIFEST[\'manifests\']`' % name,
        )

    conf = settings.WEBPACK_MANIFEST['manifests'][name]

    for prop in ('path', 'static_url', 'static_root'):
        if prop not in conf:
            raise webpack_manifest.WebpackManifestConfigError(
                '"%s" has not been defined in `WEBPACK_MANIFEST[\'manifests\'][\'%s\']`' % (prop, name),
            )

    return webpack_manifest.load(**conf)
