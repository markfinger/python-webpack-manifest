import fs from 'fs';
import path from 'path';
import mkdirp from 'mkdirp';
import transform from 'lodash/object/transform';
import stripAnsi from 'strip-ansi';

/*
Webpack plugin that emits a manifest file in the following format

{
	status: "built" || "building" || "errors",
	errors: null || [
		"<error text>",
		...
	],
	files: null || {
		<entry>: [
			'rel/path/to/file.ext',
			...
		],
		...
	}
}
 */

function WebpackYAMPlugin({manifestPath, outputRoot}) {
	if (!manifestPath) throw new Error('WebpackYAMPlugin: no `manifestPath` option provided. It should be an absolute path to a file');
	if (!outputRoot) throw new Error('WebpackYAMPlugin: no `outputRoot` option provided. It should be an absolute path that your assets are served from');

	this.manifestPath = manifestPath;
	this.outputRoot = outputRoot;
}

WebpackYAMPlugin.prototype.apply = function(compiler) {
	const manifestPath = this.manifestPath;
	const outputRoot = this.outputRoot;

	if (!compiler.options.output.path) throw new Error('WebpackYAMPlugin: no `output.path` defined in config');
	const outputPath = compiler.options.output.path;

	compiler.plugin('compile', (compiler, callback) => {
		emitManifest({
			manifestPath,
			status: 'building'
		});
	});

	compiler.plugin('done', (stats) => {
		if (stats.hasErrors()) {
			emitManifest({
				manifestPath,
				status: 'errors',
				errors: stats.toJson().errors.map(err => stripAnsi(err))
			});
		} else {
			emitManifest({
				manifestPath,
				status: 'built',
				files: transform(stats.compilation.chunks, (files, chunk) => {
					files[chunk.name] = chunk.files.map(file => {
						const absPath = path.join(outputPath, file);
						const relPath = absPath.slice(outputRoot.length);
						if (relPath[0] == path.sep) {
							return relPath.slice(1);
						}
						return relPath;
					});
				}, {})
			});
		}
	});
};

function emitManifest({manifestPath, status, errors=null, files=null}) {
	if (!manifestPath) throw new Error('WebpackYAMPlugin: no `manifestPath` provided in call to emitManifest');
	if (!status) throw new Error('WebpackYAMPlugin: no `status` provided in call to emitManifest');

	const manifest = JSON.stringify({
		status,
		errors,
		files
	}, null, 2);

	mkdirp(path.dirname(manifestPath), function(err) {
		if (err) throw err;

		fs.writeFile(manifestPath, manifest, function(err) {
			if (err) throw err;
		});
	});
}

module.exports = WebpackYAMPlugin;