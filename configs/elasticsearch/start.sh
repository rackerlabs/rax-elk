#!/bin/bash

ulimit -l unlimited
ulimit -n 128000
export ES_HEAP_SIZE=${ES_HEAP_SIZE:-512M}
export ES_NODE_NAME=${ES_NODE_NAME:-$(hostname)}
export ES_PUBLISH_HOST=${ES_PUBLISH_HOST:-"0.0.0.0"}

/usr/share/elasticsearch/bin/elasticsearch \
  -Des.path.conf=/etc/elasticsearch \
  -Des.max-open-files=true \
  "${@}"
