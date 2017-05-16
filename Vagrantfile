# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "boxcutter/ubuntu1604-desktop"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
    config.vm.network "public_network", ip: "192.168.0.200"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
  
  # The below setting resolves a error 
  # "Permissions 0777 for '/vagrant/.vagrant/machines/web1/virtualbox/private_key' are too open."
  # This is caused by a difference of permission rules between Windows and Linux, 
  # which results in permissions in Linux that unprotects the ssh key.
    config.vm.synced_folder "./", "/vagrant",
        owner: "vagrant", mount_options: ["dmode=775,fmode=600"]

    config.vm.define 'debian_basebuild' do |machine|
        machine.vm.network "public_network", ip: "192.168.0.200"
		machine.vm.provision :shell, inline: "sudo /sbin/ifdown enp0s8 && sudo /sbin/ifup enp0s8"
		machine.vm.provider "virtualbox" do |vb|
            # Customize the amount of memory on the VM:
		    vb.memory = "824" 
			# enable USB
			vb.customize ["modifyvm", :id, "--usb", "on"]
			vb.customize ["modifyvm", :id, "--usbehci", "on"]
			vb.customize ["usbfilter", "add", "0", 
              "--target", :id, 
              "--name", "Generic USB Storage [0220]",
              "--manufacturer", "Generic",
              "--product", "USB Storage"]
		end
		# Reads the inventory file to locate the sshkey for the debian_basebuild file,
		# then activates the yml file to provision the python sandbox
		machine.vm.provision :ansible_local do |ansible|
            ansible.playbook       = "debian_basebuild.yml"
            ansible.verbose        = true
            ansible.install        = true
            ansible.limit          = "debian_basebuild" # or only "nodes" group, etc.
            ansible.inventory_path = "inventory"
        end

    end
		

end
