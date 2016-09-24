'use strict';
const path = require('path');
var fs = require('fs-extra');
var exec = require('sync-exec');

class PythonDeps {
    constructor(serverless) {
        this.serverless = serverless;
        this.hooks = {
            'deploy:createDeploymentArtifacts': this.addPythonDependencies.bind(this)
        }
    }

    addPythonDependencies() {
        const zipFileName = `${this.serverless.service.service}.zip`;
        const artifactFilePath = path.join(this.serverless.config.servicePath, '.serverless', zipFileName);
        const distPath = path.join(this.serverless.config.servicePath, '.serverless', 'dist');
        const depTar = path.join(this.serverless.config.servicePath, 'why82.tar.gz');

        this.serverless.cli.log(`Creating ${distPath} dirs`);
        fs.removeSync(distPath);
        fs.mkdirsSync(distPath);
        this.exec(`tar -xf ${depTar}`, distPath);
        this.serverless.cli.log(`Adding python dependencies to service zip`);
        this.exec(`zip -9qr ${artifactFilePath} ./*`, distPath);
    }

    exec(cmd, cwd) {
        this.serverless.cli.log(cmd);
        var result = exec(cmd, {cwd: cwd});
        if (result.status!=0) {
          throw new Error(`Could not execute: ${cmd}`);
        }
    }
}

module.exports = PythonDeps;
