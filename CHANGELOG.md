Changelog
=========

### 2.1.1 (29/08/2018)

- Fixed a bug preventing `debug` flag from being passed to the Django template tag.


### 2.1.0 (26/07/2018)

- Added Django template tag to load manifests during template runtime.


### 2.0.0 (25/07/2018)

- Exceptions will now be raised if an unknown entry is accessed. See [https://github.com/markfinger/python-webpack-manifest/issues/1]
- Improved ability to debug `WebpackManifestTypeEntry` instances as they can now access their parent manifest via `self.manifest`.

### 1.2.0 (13/02/2017)

- Support inline rendering via @IlyaSemenov [https://github.com/markfinger/python-webpack-manifest/pull/5]

### 1.1.0 (19/12/2016)

- Python 3 compatibility fixes from @IlyaSemenov [https://github.com/markfinger/python-webpack-manifest/pull/3]

### 1.0.0 (21/4/2016)

- Improving handling of write-buffer race conditions.

### 0.3.0 (22/9/2015)

- Fixed an issue where a write-buffer race condition emerges between the node and python processes

### 0.2.0 (1/9/2015)

- Initial Release