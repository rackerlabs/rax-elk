rax-elk
=======

## Description

The purpose of this repository is to allow a quick push-button setup of a minimum viable logstash cluster.

Join the discussion on #elk-dev on Freenode.

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

## Docker Containers

### Logstash

Inside of `configs/logstash` you'll see a conf.d directory. This directory gets added to the container during the build. In the [Dockerfile](configs/logstash/Dockerfile) you'll see that the default command tells logstash to load all *.conf files in that directory. We've included a couple of conf.sample files that can just be renamed or you can add as many custom conf files as you want. (Note: *.conf files in that path are .gitignored)

If you're using elasticsearch you'll want to set a couple of keys in etcd for the [start.sh](configs/logstash/start.sh) script. In the future these will be set automatically by the systemd units.

Set the host for Elasticsearch to publish itself as to the rest of the cluster (may need to specify a different interface):

`etcdctl set /rax_elk/es_publish_host $(ifconfig eth2 |grep 'inet ' |awk '{print $2}')`

Set list of other hosts to connect to:

`etcdctl set /rax_elk/es_hosts/node0 192.168.2.5:9200`

The Logstash heap size can be customized by setting the `LS_HEAP_SIZE` environment variable in docker run.
