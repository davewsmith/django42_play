# vi: set ft=ruby :

$provision = <<SCRIPT
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install python3.8-venv python3-pip sqlite3

cd /vagrant
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
SCRIPT



VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/focal64"  # Ubuntu 20.04
    config.vm.network "forwarded_port", guest: 8000, host: 8000

    config.vm.provider "virtualbox" do |vb|
        vb.name = "Django 4.2 Playground"
        vb.memory = 1024
        vb.cpus = 1
    end

    config.vm.provision :shell, inline: $provision, privileged: false
end
