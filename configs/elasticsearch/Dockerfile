FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive
# Java 8 webupd8team key
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
RUN echo deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main > /etc/apt/sources.list.d/webupd8team.list
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
ADD http://packages.elasticsearch.org/GPG-KEY-elasticsearch /tmp/GPG-KEY-elasticsearch
RUN apt-key add /tmp/GPG-KEY-elasticsearch
RUN echo deb http://packages.elasticsearch.org/elasticsearch/1.1/debian stable main > /etc/apt/sources.list.d/elasticsearch.list
RUN apt-get update \
  && apt-get upgrade -y -q \
  && apt-get -y -q install oracle-java8-installer oracle-java8-set-default elasticsearch \
  && apt-get clean

ADD elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
ADD logging.yml /etc/elasticsearch/logging.yml
ADD start.sh /
EXPOSE 9200
EXPOSE 9300
VOLUME ["/var/lib/elasticsearch"]

ENTRYPOINT ["/start.sh"]
