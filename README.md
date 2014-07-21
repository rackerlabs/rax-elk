rax-elk
=======

## Description

The purpose of this repository is to allow a quick push-button setup of a minimum viable logstash cluster.

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
