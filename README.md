rax-elk
=======

## Description

The purpose of this repository is to allow a quick push-button setup of a minimum viable logstash cluster.

Join the discussion on #elk-dev on Freenode.

## Dev Environment

The Vagrantfile will handle configuring CoreOS instance(s) for testing containers and configurations on. Look in [configs/vagrant](configs/vagrant) for sample configurations. These should be safe to use out of the box by removing `.sample` from the filenames.

Virtualbox:  
`vagrant up`

Rackspace Cloud (requires OS\_USERNAME and OS\_PASSWORD to be set):  
`vagrant up --provider=rackspace`

The synced folder configuration uses Vagrant's rsync method so run `vagrant rsync` to update the files on the VM. Alternately just leave `vagrant rsync-auto` running in the background.

Watch the initial Vagrant bootstrapping for messages about the box file being out of date. If it is just run `vagrant box update` like the warning says then you'll be good to go next time you bring up a clean box.

To connect to the docker instance directly (if you have Docker installed on you host system) make sure you `export DOCKER_HOST=127.0.0.1:2375` then docker commands should work as expected.

## Cluster Configuration

The initial cluster will be started using a bootstrap script and a config.yaml file. The config allows you to set things such as the Elasticsearch cluster size and flavors used for the nodes.

### cloud-config.yaml

Rename cloud-config.yaml.sample and add settings that should exist on all nodes. One good example would be ssh_authorized_keys.

[CoreOS Cloudinit docs](http://coreos.com/docs/cluster-management/setup/cloudinit-cloud-config/)

```yaml
# Example only
users:
  - name: philkates
  groups:
    - sudo
    - docker
  coreos-ssh-import-github: philk

coreos:
  update:
    reboot-strategy: etcd-lock

```
...etc

### config.yaml

Rename [config.yaml.sample](config.yaml.sample) to config.yaml and update the settings you wish to change.
