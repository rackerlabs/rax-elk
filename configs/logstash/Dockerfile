FROM ubuntu:14.04
MAINTAINER "Phil Kates <me@philkates.com>"

ENV DEBIAN_FRONTEND noninteractive
ADD http://packages.elasticsearch.org/GPG-KEY-elasticsearch /tmp/GPG-KEY-elasticsearch
RUN apt-key add /tmp/GPG-KEY-elasticsearch
RUN echo deb http://packages.elasticsearch.org/logstash/1.4/debian stable main > /etc/apt/sources.list.d/logstash.list
RUN apt-get update \
    && apt-get upgrade -y -q \
    && apt-get -y -q install curl logstash logstash-contrib \
    && apt-get clean

ENV LOGSTASH_HOME /opt/logstash

ADD conf.d /etc/logstash/conf.d/

ENV ETCDCTL_VERSION v0.4.6
RUN curl -L -o etcdctl.tar.gz https://github.com/coreos/etcd/releases/download/$ETCDCTL_VERSION/etcd-$ETCDCTL_VERSION-linux-amd64.tar.gz \
    && tar zxvf etcdctl.tar.gz \
    && mv -v etcd-$ETCDCTL_VERSION-linux-amd64/etcdctl /usr/local/bin/ \
    && rm -rf etcdctl.tar.gz etcd-$ETCDCTL_VERSION-linux-amd64

ADD start.sh /
CMD ["agent", "-f", "/etc/logstash/conf.d/*.conf"]
ENTRYPOINT ["./start.sh"]
