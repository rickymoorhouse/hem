""" HEM - HTTP(s) Endpoint Monitor """
from multiprocessing import Pool
from datetime import timedelta
import abc
import logging
import os
import requests
import click
import yaml
import six
import pike.discovery
from pike.manager import PikeManager

logging.captureWarnings(True)

def setup_logging(
        default_path='logging.yaml',
        default_level=logging.ERROR,
        env_key='LOG_CFG'
    ):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as config_file:
            config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

@six.add_metaclass(abc.ABCMeta)
class StoreBase(object):
    """Base class for storing of check data
    """
    @abc.abstractmethod
    def __init__(self):
        """ Abstract init method """

    @abc.abstractmethod
    def stage(self, data):
        """Gather the data for storing

        :param data: object containing data points
        :returns: True or False
        """

    @abc.abstractmethod
    def store(self):
        """ Saves current buffer """

class Check(object):
    """ A check and it's testing  """
    url = ""
    method = "get"
    name = ""
    timeout = 10
    metrics = None

    def __init__(self, name, path, secure=False, verify=True, metrics=None):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.verify = verify
        if secure:
            self.url = "https://{}" + path
        else:
            self.url = "http://{}" + path
        self.metrics = metrics

    def test(self, param):
        """
        The core testing -
        takes in the parameter to test the check with and returns status and time
        """
        time = timedelta(seconds=0)

        try:
            http_call=getattr(requests,self.method) 
            result = http_call(self.url.format(param), timeout=self.timeout, verify=self.verify)
            self.logger.debug("Response text: %s", result.text)
            time = result.elapsed
            result.raise_for_status()
            status = result.status_code
        except requests.exceptions.HTTPError as he:
            self.logger.debug(he)
            self.report_failure(param, he.message)
            time = result.elapsed
            status = result.status_code
        except requests.exceptions.SSLError as ssl_error:
            self.logger.debug(ssl_error)
            self.report_failure(param, ssl_error.message)
            status = 000
        except requests.exceptions.ConnectTimeout as timeout:
            self.logger.debug(timeout)
            self.report_failure(param, timeout.message)
            status = 000
            time = timedelta(seconds=self.timeout)
        except requests.exceptions.ConnectionError as connection:
            self.logger.debug(connection)
            self.report_failure(param, connection.message)
            status = 0000
        self.metrics.store(
            "{}.{}.result".format(self.name, param.replace('.', '_')),
            status
            )
        self.metrics.store(
            "{}.{}.time".format(self.name, param.replace('.', '_')),
            time.total_seconds()
            )
        return (status, time)

    def test_list(self, param_list):
        """ Run test over a list of parameters """
        results = []
        for param in param_list:
            results.append(self.test(param))
        self.logger.info(results)
        return results

    def report_failure(self, param, message):
        """ Display errors """
        click.echo(click.style("{} Failed with {}".format(param, message),fg='red'))


def summarise_results(results):
    #[(200, datetime.timedelta(0, 0, 138273)), (200, datetime.timedelta(0, 0, 142190))]
    success_count = 0
    for result in results:
        if result[0] == 200:
            success_count += 1
    print success_count

def discover_hosts(src):
    discovery_type = src['type']
    try:
        host_list = list()
        with PikeManager(['drivers']) as mgr:
            discovery = pike.discovery.py.get_module_by_name('discovery_' + discovery_type)
            host_list = discovery.hosts(**src)
            return host_list
    except ImportError:
        print "Discovery method {} not found".format(discovery_type)
        return []

@click.command()
@click.option('--count', default=1)
def runApp(**kwargs):
    for x in range(kwargs['count']):
        logging.basicConfig(level=logging.ERROR)
        with open('config.yaml') as config_file:
            config = yaml.load(config_file)
        if 'discovery' in config:
            DEFAULT_DISCOVERY = config['discovery']
        else:
            DEFAULT_DISCOVERY = {}

        with PikeManager(['drivers']) as mgr:
            metrics_driver = pike.discovery.py.get_module_by_name('metrics_' + config['metrics']['type'])
        metrics = metrics_driver.instance(config['metrics'])
        
        
        for test_name in config['tests']:
            test = config['tests'][test_name]
            if 'hosts' in test:
                hosts = test['hosts']
            elif 'discovery' in test:
                discovery = DEFAULT_DISCOVERY.copy()
                discovery.update(test['discovery']) # Python 3.5 move to context = {**defaults, **user}
                hosts = discover_hosts(discovery)
            else:
                hosts = ["api.eu.apiconnect.ibmcloud.com", "rickymoorhouse.uk"]
            click.echo("Testing {0} across {1} hosts".format(test_name, len(hosts)))
            logging.debug("{} - {}".format(test,test.get('url')))
            CHECK = Check(
                test_name,
                test.get('path'), 
                test.get('secure',False), 
                test.get('verify',True), 
                metrics)
            results = CHECK.test_list(hosts)
            summarise_results(results)

if __name__ == '__main__':
    runApp()
