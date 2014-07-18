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

* logstash.configurations - Specify a list of files in the `logstash_configurations` directory that you want added into the logstash docker container on build

```yaml
coreos:
  # Optional: Specify the full URL or leave empty. Will generate a new discovery id for the cluster if empty
  discovery: https://discovery.etcd.io/8ba477fa9ddf749616eb98812269a726
logstash:
  # Size of the elasticsearch data nodes
  flavor: performance1-8
  configurations:
    inputs:
      - syslog
    outputs:
      - elasticsearch
      - redis_pub_sub
elasticsearch:
  # Size of the elasticsearch data nodes
  flavor: performance2-15
  # Optional
  name: corestash
  # How many data nodes to create
  cluster_size: 3
```
