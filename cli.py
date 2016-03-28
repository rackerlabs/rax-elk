import sys

from twisted.task import react

import yaml


class Elk(object):
    """
    Elastic search cluster spinup tool
    """
    def __init__(self, cli_args=None):
        self.conf_fname = cli_args.config
        self.discovery = cli_args.discovery

    def bootstrap(self):
        # Replace certain conf parts/ add if any
        conf = yaml.load(open(self.conf_fname).read())
        conf['coreos']['etcd']['discovery'] = get_discovery_url(self.discovery)

    def update(self):
        pass


def get_discovery_url(discovery_id=None):
    if discovery_id is None:
        return requests.get('http://discovery.etcd.io/new').text
    return 'http://discovery.etcd.io/{}'.format(discovery_id)


def bootstrap(args):
    elk = ELk(cli_args=args)
    elk.bootstrap()


def update(args):
    pass


def setup_parser():
    parser = argparse.ArgumentParser('elk', description='Spin up elasticsearch/logstash cluster')
    subparsers = parser.add_subparsers('commands')
    bootstrap = subparsers.add_parser('bootstrap')
    bootstrap.add_argument('-c', '--config', help='CoreOS cloud config yaml file',
                           default='config.yaml')
    bootstrap.add_argument('-d', '--discovery', help='Discovery ID')
    bootstrap.set_defaults(func=bootstrap)
    update = subparsers.add_parser('update')
    update.set_defaults(func=update)
    return parser


def main(args):
    parsed = setup_parser().parse_args(args)
    parsed.func(parsed)


if __name__ == '__main__':
    main(sys.argv)

#task.react(main, sys.argv)
