#!/bin/bash

export ETCDCTL_PEERS="http://$(route |grep default | awk '{print $2}'):4001"

cd $LOGSTASH_HOME
exec 2>&1

ES_UNICAST_HOSTS=$(etcdctl ls /rax_elk/es_hosts | xargs -n1 etcdctl get | paste -sd ",")

# Need to override some Elasticsearch options inside the container
export JAVA_OPTS="-Des.network.publish_host=$ES_PUBLISH_HOST \
-Des.discovery.zen.ping.multicast.enabled=false \
-Des.discovery.zen.ping.unicast.hosts=$ES_UNICAST_HOSTS"

$LOGSTASH_HOME/bin/logstash $@
