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
        logging.getLogger().setLevel(level=default_level)
    else:
        logging.basicConfig(level=default_level)

def load_config(path = 'hem.yaml'):
    """
    Load configuration
    """
    path_list = [path, '/etc/hem.yaml']
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
    headers = {}
    expected = None
    timeout = 10
    metrics = None
    certificate = None

    def __init__(self, name, test, metrics=None):
        #path, secure=False, verify=True, metrics=None):
        self.logger = logging.getLogger(__name__)
        self.name = name

        self.verify = test.get('verify', True)
        if test.get('secure', False):
            self.url = "https://{}" + test.get('path', '')
        else:
            self.url = "http://{}" + test.get('path', '')
        self.method = test.get('method', "get")
        if 'expected' in test:
            self.expected = test['expected']
        if 'certificate' in test:
            self.logger.info("Setting certificate to %s", test['certificate'])
            self.certificate = test['certificate']
        if 'headers' in test:
            self.headers = test['headers']

        self.metrics = metrics

    def test(self, param, results):
        """
        The core testing -
        takes in the parameter to test the check with and returns status and time
        """
        elapsed_time = timedelta(seconds=0)

        try:
            http_call=getattr(requests,self.method) 
            start = time.time()
            result = http_call(
                self.url.format(param), 
                headers=self.headers,
                timeout=self.timeout, 
                verify=self.verify,
                cert=self.certificate
                )
            self.logger.debug("Response text: %s", result.text)
            elapsed_time = result.elapsed
            result.raise_for_status()
            status = result.status_code
        except requests.exceptions.HTTPError as he:
            self.logger.debug(he)
            self.report_failure(param, result.text)
            elapsed_time = result.elapsed
            status = result.status_code
        except requests.exceptions.SSLError as ssl_error:
            self.logger.debug(ssl_error)
            self.report_failure(param, ssl_error.strerror)
            status = 526
        except requests.exceptions.ConnectTimeout as timeout:
            self.logger.debug(timeout)
            self.report_failure(param, timeout.strerror)
            status = 522
            elapsed_time = timedelta(seconds=self.timeout)
        except requests.exceptions.ConnectionError as connection:
            self.logger.debug(connection)
            self.report_failure(param, connection.strerror)
            status = 0000
        roundtrip_time = time.time() - start
        success = 0
        if self.expected:
            self.logger.debug("Testing status of {} against {}".format(status, self.expected))
            if status == self.expected:
                success = 1
        elif status == requests.codes.ok:
            success = 1

        if self.metrics:
            self.metrics.stage(
                "{}.{}.result".format(self.name, param.replace('.', '_')),
                status
                )
            self.metrics.stage(
                "{}.{}.success".format(self.name, param.replace('.', '_')),
                success
                )
            self.metrics.stage(
                "{}.{}.time".format(self.name, param.replace('.', '_')),
                elapsed_time.total_seconds()
                )
            self.metrics.stage(
                "{}.{}.roundtrip".format(self.name, param.replace('.', '_')),
                roundtrip_time
                )
        results.append((status, elapsed_time))

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
        click.echo(click.style("{} Failed with {}".format(param, message.split('\n')[0]),fg='red'))


def discover_hosts(src, metrics=None):
    discovery_type = src['type']
    try:
        host_list = list()
        with PikeManager(['.', 'drivers']):
            discovery = pike.discovery.py.get_module_by_name('hemApp.drivers.discovery_' + discovery_type)
            if None != metrics:
                src['metrics'] = metrics
            try:
                host_list = discovery.hosts(**src)
            except Exception as e:
                logging.error("{} discovery of failed with exception".format(discovery_type))
                logging.exception(e)
                host_list = []
            return host_list
    except ImportError as e:
        logging.exception(e)
        click.echo("Discovery method {} not found".format(discovery_type))
        return []

def initialise_metrics(metricConfig):
    with PikeManager(['.', 'drivers']):
        metrics_driver = pike.discovery.py.get_module_by_name(
            'hemApp.drivers.metrics_' + metricConfig.get('type','console')
        )
    return metrics_driver.instance(metricConfig)

def run_tests(config, metrics=None):        
    start = time.time()
    logging.info("Started tests at {}".format(start))

    if 'discovery' in config:
        DEFAULT_DISCOVERY = config['discovery']
    else:
        DEFAULT_DISCOVERY = {}
    
    for test_name in config['tests']:
        test = config['tests'][test_name]

        # Host list can be an array in the config or discovery
        if 'hosts' in test:
            hosts = test['hosts']
        elif 'discovery' in test:
            # Local discovery section inherits defaults but overrides defaults
            discovery = DEFAULT_DISCOVERY.copy()
            discovery.update(test['discovery']) # Python 3.5 move to context = {**defaults, **user}
            hosts = discover_hosts(discovery, metrics)
        else:
            hosts = []
        logging.info("Testing {0} across {1} hosts".format(test_name, len(hosts)))
        logging.debug(test)
        CHECK = Check(
            test_name,
            test,
            metrics)
#            test.get('secure',False), 
#            test.get('verify',True), 
        results = CHECK.test_list(hosts)
        logging.debug(results)
    end = time.time()
    metrics.store()
    return (end - start)

