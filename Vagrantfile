# -*- mode: ruby -*-
# # vi: set ft=ruby :

require 'fileutils'

Vagrant.require_version ">= 1.6.0"

CLOUD_CONFIG_PATH = File.join(File.dirname(__FILE__), "configs", "vagrant", "user-data")
CONFIG = File.join(File.dirname(__FILE__), "configs", "vagrant", "config.rb")

# Defaults for config options defined in CONFIG
$num_instances = 1
$update_channel = "alpha"
$enable_serial_logging = false
$vb_gui = false
$vb_memory = 1024
$vb_cpus = 1

# Attempt to apply the deprecated environment variable NUM_INSTANCES to
# $num_instances while allowing config.rb to override it
if ENV["NUM_INSTANCES"].to_i > 0 && ENV["NUM_INSTANCES"]
  $num_instances = ENV["NUM_INSTANCES"].to_i
end

if File.exist?(CONFIG)
  require CONFIG
end

file_provisioner = lambda do |fp|
  return unless File.exist?(CLOUD_CONFIG_PATH)
  fp.vm.provision :file, :source => "#{CLOUD_CONFIG_PATH}", :destination => "/tmp/vagrantfile-user-data"
  fp.vm.provision :shell, :inline => "mv /tmp/vagrantfile-user-data /var/lib/coreos-vagrant/", :privileged => true
end

Vagrant.configure("2") do |config|
  config.vm.box = "coreos-%s" % $update_channel
  config.vm.box_version = ">= 308.0.1"
  config.vm.box_url = "http://%s.release.core-os.net/amd64-usr/current/coreos_production_vagrant.json" % $update_channel

  config.vm.provider :vmware_fusion do |vb, override|
    override.vm.box_url = "http://%s.release.core-os.net/amd64-usr/current/coreos_production_vagrant_vmware_fusion.json" % $update_channel
  end

  config.vm.provider :virtualbox do |v|
    # On VirtualBox, we don't have guest additions or a functional vboxsf
    # in CoreOS, so tell Vagrant that so it can be smarter.
    v.check_guest_additions = false
    v.functional_vboxsf     = false
  end

  config.vm.provider :rackspace do |v, override|
    # v.username = get_env!('OS_USERNAME')
    # v.api_key  = get_env!('OS_PASSWORD')
    v.username = ENV['OS_USERNAME']
    v.api_key  = ENV['OS_PASSWORD']
    v.flavor   = /2 GB Performance/
    v.image    = /CoreOS.*#{$update_channel}/i
    v.key_name = "philk-key" # TODO: Replace this with a config option
    v.rackspace_region = :iad
    v.user_data = CLOUD_CONFIG_PATH
    override.ssh.username = "core"
    override.ssh.private_key_path = File.join("#{ENV['HOME']}", ".ssh", "id_rsa")

    # Turns out just putting this in a provider block doesn't really isolate it
    # if on_rackspace?
    #   config.ssh.username = "core"
    #   config.ssh.private_key_path = File.join("#{ENV['HOME']}", ".ssh", "id_rsa")
    # end
  end

  # plugin conflict
  if Vagrant.has_plugin?("vagrant-vbguest") then
    config.vbguest.auto_update = false
  end

  (1..$num_instances).each do |i|
    config.vm.define vm_name = "#{ENV['USER']}-core-%02d" % i do |vmcfg|
      vmcfg.vm.hostname = vm_name

      if $enable_serial_logging
        logdir = File.join(File.dirname(__FILE__), "log")
        FileUtils.mkdir_p(logdir)

        serialFile = File.join(logdir, "%s-serial.txt" % vm_name)
        FileUtils.touch(serialFile)

        vmcfg.vm.provider :vmware_fusion do |v, override|
          v.vmx["serial0.present"] = "TRUE"
          v.vmx["serial0.fileType"] = "file"
          v.vmx["serial0.fileName"] = serialFile
          v.vmx["serial0.tryNoRxLoss"] = "FALSE"
        end

        vmcfg.vm.provider :virtualbox do |vb, override|
          vb.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
          vb.customize ["modifyvm", :id, "--uartmode1", serialFile]
        end
      end

      if $expose_docker_tcp
        vmcfg.vm.network "forwarded_port", guest: 2375, host: ($expose_docker_tcp + i - 1), auto_correct: true
      end

      vmcfg.vm.provider :vmware_fusion do |vb, override|
        vb.gui = $vb_gui
        file_provisioner.call(override)
      end

      vmcfg.vm.provider :virtualbox do |vb, override|
        vb.gui = $vb_gui
        vb.memory = $vb_memory
        vb.cpus = $vb_cpus
        file_provisioner.call(override)
      end

      ip = "172.17.8.#{i+100}"
      vmcfg.vm.network :private_network, ip: ip

      # Uncomment below to enable NFS for sharing the host machine into the coreos-vagrant VM.
      #config.vm.synced_folder ".", "/home/core/share", id: "core", :nfs => true, :mount_options => ['nolock,vers=3,udp']
      config.vm.synced_folder ".", "/vagrant", :type => "rsync", :rsync__exclude => [".git/", ".vagrant/"]

      vmcfg.vm.provision "docker" do |d|
        d.pull_images "ubuntu:14.04"
        # d.build_image "/vagrant/configs/logstash", :args => "-t logstash"
      end

    end
  end
end
