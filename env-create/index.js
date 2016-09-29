'use strict';
var EnvVarsPlugin = require('serverless-plugin-write-env-vars')

class EnvCreate {
    constructor(serverless, opts) {
        this.serverless = serverless;
        this._opts = opts;
        this.commands = {
          env:{
            usage: 'Creates a .env file based on SLS config.',
            lifecycleEvents:[
              'create'
            ]
          }
        };
        this.hooks = {
          'env:create': this.writeEnvironmentFile.bind(this)
        };
    }

    writeEnvironmentFile(){
      var env_vars = new EnvVarsPlugin(this.serverless, this.opts);
      env_vars.writeEnvironmentFile();
    }
}

module.exports = EnvCreate;
