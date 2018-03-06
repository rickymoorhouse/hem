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
import time
import pike.discovery
from pike.manager import PikeManager
import threading


logging.captureWarnings(True)

def setup_logging(
        default_path='logging.yaml',
        default_level=logging.ERROR
        ):
    """Setup logging configuration

    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as config_file:
            config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def load_config():
    """
    Load configuration
    """
    path = '/etc/hem.yaml'
    path_list = ['hem.yaml', '/etc/hem.yaml']
    env_path = os.getenv('HEM_CONFIG', None)
    if env_path:
        path_list.insert(0, env_path)
    for path in path_list:
        if os.path.exists(path):
            with open(path, 'rt') as config_file:
                return yaml.safe_load(config_file.read())
    click.echo("No config found in "+', '.join(path_list))
    exit(2)

@six.add_metaclass(abc.ABCMeta)
class Metrics(object):
    """Base class for storing of metrics data
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

    def test(self, param, results):
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
        self.metrics.stage(
            "{}.{}.result".format(self.name, param.replace('.', '_')),
            status
            )
        self.metrics.stage(
            "{}.{}.time".format(self.name, param.replace('.', '_')),
            time.total_seconds()
            )
        results.append((status, time))

    def test_list(self, param_list):
        """ Run test over a list of parameters """
        results = []
        threads = []
        # Start a thread for each parameter
        for param in param_list:
            t = threading.Thread(target=self.test, args=(param, results))
            threads.append(t)
            t.start()
        for i in range(len(threads)):
            threads[i].join()
        self.logger.info(results)
        return results

    def report_failure(self, param, message):
        """ Display errors """
        click.echo(click.style("{} Failed with {}".format(param, message),fg='red'))


def discover_hosts(src):
    discovery_type = src['type']
    try:
        host_list = list()
        with PikeManager(['.', 'drivers']):
            discovery = pike.discovery.py.get_module_by_name('hemApp.drivers.discovery_' + discovery_type)
            host_list = discovery.hosts(**src)
            return host_list
    except ImportError as e:
        logging.exception(e)
        click.echo("Discovery method {} not found".format(discovery_type))
        return []

@click.command()
@click.option('-v', '--verbose', count=True)
def runApp(**kwargs):
    if kwargs['verbose'] > 1:
        setup_logging(default_level=logging.DEBUG)
    elif kwargs['verbose'] > 0:
        setup_logging(default_level=logging.INFO)
    else:
        setup_logging(default_level=logging.ERROR)
        
    config = load_config()
    logging.info(config)
    iteration = 1
    while True:
        start = time.time()
        logging.info("Iteration {} at {}".format(iteration, start))

        if 'discovery' in config:
            DEFAULT_DISCOVERY = config['discovery']
        else:
            DEFAULT_DISCOVERY = {}

        with PikeManager(['.', 'drivers']):
            metrics_driver = pike.discovery.py.get_module_by_name('hemApp.drivers.metrics_' + config['metrics']['type'])
        metrics = metrics_driver.instance(config['metrics'])
        
        
        for test_name in config['tests']:
            test = config['tests'][test_name]
            # Host list can be an array in the config or discovery
            if 'hosts' in test:
                hosts = test['hosts']
            elif 'discovery' in test:
                discovery = DEFAULT_DISCOVERY.copy()
                discovery.update(test['discovery']) # Python 3.5 move to context = {**defaults, **user}
                hosts = discover_hosts(discovery)
            else:
                hosts = []
            logging.info("Testing {0} across {1} hosts".format(test_name, len(hosts)))
            logging.debug("{} - {}".format(test,test.get('url')))
            CHECK = Check(
                test_name,
                test.get('path'), 
                test.get('secure',False), 
                test.get('verify',True), 
                metrics)
            results = CHECK.test_list(hosts)
            logging.debug(results)
        end = time.time()
        iteration += 1
        metrics.store()
        try:
            time.sleep(int(30 - (end - start)))
        except IOError:
            logging.info("Too quick!")

if __name__ == '__main__':
    runApp()
