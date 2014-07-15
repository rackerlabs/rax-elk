rax-elk
=======

## Description

The purpose of this repository is to allow a quick push-button setup of a minimum viable logstash cluster.

## Cluster Configuration

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
