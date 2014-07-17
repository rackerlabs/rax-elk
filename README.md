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

```yaml
coreos:
    system_names:
        - log0
        - es0
        - es1
        - es2
logstash:
    flavor: performance1-8
elasticsearch:
    flavor: performance2-15
    name: corestash
    cluster_size: 3
```
