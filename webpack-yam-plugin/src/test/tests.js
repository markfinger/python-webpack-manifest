import fs from 'fs';
import path from 'path';
import sourceMapSupport from 'source-map-support';
import chai from 'chai';
import rimraf from 'rimraf';
import webpack from 'webpack';
import WebpackYAMPlugin from '../webpack-yam-plugin';

sourceMapSupport.install({
	handleUncaughtExceptions: false
});

chai.config.includeStack = true;

const assert = chai.assert;
const OUTPUT_DIR = path.join(__dirname, 'test_output');
const TEST_MANIFEST_FILE = path.join(OUTPUT_DIR, 'test_manifest.json');

// Ensure we have a clean slate before and after each test
function clearFiles() {
    rimraf.sync(OUTPUT_DIR);
}
beforeEach(clearFiles);
afterEach(clearFiles);

describe('webpack-yam-plugin', () => {
	it('should emit a manifest with relative paths', (done) => {
		webpack({
            context: __dirname,
            entry: './test_file_1.js',
            output: {
                path: OUTPUT_DIR,
                filename: 'test.js'
            },
			plugins: [
                new WebpackYAMPlugin({
                    manifestPath: TEST_MANIFEST_FILE,
                    outputRoot: path.join(__dirname, '..')
                })
			]
		}, function() {
            setTimeout(() => {
                const manifest = JSON.parse(
                    fs.readFileSync(TEST_MANIFEST_FILE).toString()
                );
                assert.deepEqual(manifest, {
                    status: 'built',
                    errors: null,
                    files: {
                        main: [
                            path.join(path.basename(__dirname), path.basename(OUTPUT_DIR), 'test.js')
                        ]
                    }
                });
                done();
            }, 10);
        });
	});
    it('should emit a manifest indicating any errors encountered', (done) => {
		webpack({
            context: __dirname,
            entry: './test_file_2.js',
            output: {
                path: OUTPUT_DIR,
                filename: 'test.js'
            },
			plugins: [
                new WebpackYAMPlugin({
                    manifestPath: TEST_MANIFEST_FILE,
                    outputRoot: path.join(__dirname, '..')
                })
			]
		}, function() {
            setTimeout(() => {
                const manifest = JSON.parse(
                    fs.readFileSync(TEST_MANIFEST_FILE).toString()
                );
                assert.equal(manifest.status, 'errors');
                assert.isArray(manifest.errors);
                assert.equal(manifest.errors.length, 1);
                assert.include(manifest.errors[0], 'test_file_3.js');
                assert.include(manifest.errors[0], './package_that_does_not_exist');
                assert.isNull(manifest.files);
                done();
            }, 10);
        });
	});
    it('should emit a manifest that groups entries', (done) => {
		webpack({
            context: __dirname,
            entry: {
                foo: './test_file_1.js',
                bar: './test_file_5.js'
            },
            output: {
                path: OUTPUT_DIR,
                filename: '[name].js'
            },
			plugins: [
                new WebpackYAMPlugin({
                    manifestPath: TEST_MANIFEST_FILE,
                    outputRoot: path.join(__dirname, '..')
                })
			]
		}, function() {
            setTimeout(() => {
                const manifest = JSON.parse(
                    fs.readFileSync(TEST_MANIFEST_FILE).toString()
                );
                assert.deepEqual(manifest, {
                    status: 'built',
                    errors: null,
                    files: {
                        foo: [
                            path.join(path.basename(__dirname), path.basename(OUTPUT_DIR), 'foo.js')
                        ],
                        bar: [
                            path.join(path.basename(__dirname), path.basename(OUTPUT_DIR), 'bar.js')
                        ]
                    }
                });
                done();
            }, 10);
        });
	});
});