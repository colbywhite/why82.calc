'use strict';
const path = require('path');
var fs = require('fs-extra');
var exec = require('sync-exec');

class PythonDeps {
    constructor(serverless) {
        this.serverless = serverless;
        this.hooks = {
            'after:deploy:createDeploymentArtifacts': this.afterArtifacts.bind(this)
        }
    }

    afterArtifacts() {
        console.log('after:deploy:createDeploymentArtifacts');
        const zipFileName = `${this.serverless.service.service}.zip`;
        const artifactFilePath = path.join(this.serverless.config.servicePath, '.serverless', zipFileName);
        const distPath = path.join(this.serverless.config.servicePath, '.serverless', 'dist');
        const why82Path = path.join(this.serverless.config.servicePath, '.serverless', 'dist', 'why82');
        const srcDir = path.join(this.serverless.config.servicePath, 'why82');
        const calc_schedule_src = path.join(this.serverless.config.servicePath, 'calc_schedule.py');
        const calc_tiers_src = path.join(this.serverless.config.servicePath, 'calc_tiers.py');
        const calc_schedule_dist = path.join(distPath, 'calc_schedule.py');
        const calc_tiers_dist = path.join(distPath, 'calc_tiers.py');
        const depTar = path.join(this.serverless.config.servicePath, 'why82.tar.gz');

        console.log(`Removing ${artifactFilePath}`);
        fs.removeSync(artifactFilePath);

        console.log(`Removing ${distPath}`);
        fs.removeSync(distPath);

        console.log(`Creating ${distPath}`);
        fs.mkdirsSync(distPath);

        console.log(`Creating ${why82Path}`);
        fs.mkdirsSync(why82Path);

        console.log(`Un-tarring ${depTar} into ${distPath}`);
        console.log(`tar -xf ${depTar}`);
        console.log(exec(`tar -xf ${depTar}`, {cwd: distPath}));
        console.log(`Copying ${srcDir} into ${why82Path}`);
        fs.copySync(srcDir, why82Path);
        console.log(`Copying ${calc_schedule_src} into ${calc_schedule_dist}`);
        fs.copySync(calc_schedule_src, calc_schedule_dist);
        console.log(`Copying ${calc_tiers_src} into ${calc_tiers_dist}`);
        fs.copySync(calc_tiers_src, calc_tiers_dist);
        console.log(`Creating ${artifactFilePath}`);
        console.log(`zip -9qr ${artifactFilePath} ./*`);
        console.log(exec(`zip -9qr ${artifactFilePath} ./*`, {cwd: distPath}));
    }
}

module.exports = PythonDeps;
