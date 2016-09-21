# why82.lambda

This contains the AWS Lambda functions associated with the
[Why82?](http://why82.com) project.

## Development

To install dependencies:

    nvm install v4.5.0
    npm install -g serverless
    pushd node_modules/python-deps && npm install && popd
    pip install -r requirements.txt

To run tests run `invoke test`. You can call `nosetests` directly if you wish to provide more advanced options.

## TODO

- Get rid of that embarrassing, hackery `python-deps` package to get around how
`sls` builds the Lambda package.
