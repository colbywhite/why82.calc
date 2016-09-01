requirements = File.read('requirements.txt').split("\n").join ' '

pip_install = <<SCRIPT
#!/bin/bash
set -e
set -x

virtualenv /why82
source /why82/bin/activate
pip install --upgrade pip
pip install #{requirements}
SCRIPT
Vagrant.configure('2') do |config|
  config.vm.box = 'dummy'

  config.vm.provider :aws do |aws, override|
    aws.keypair_name = 'lambda_deps'
    aws.instance_type = 't2.micro'

    # allows SSH from colby's network
    aws.security_groups = ['ssh from colby']

    # See: https://aws.amazon.com/amazon-linux-ami
    aws.region_config 'us-west-2', :ami => 'ami-7172b611'

    override.ssh.username = 'ec2-user'
    override.ssh.private_key_path = File.expand_path '~/.ssh/lambda_deps.pem'

    config.vm.provision 'shell', path: 'deps_setup.sh'
    config.vm.provision 'shell', inline: pip_install
    config.vm.provision 'shell', path: 'deps_package.sh'
  end
end
