import click
import logging
import yaml
import logging.config
import hemApp
import time
import os
import urllib3

@click.command()
@click.version_option()
@click.option('-v', '--verbose', 
                help="Verbose mode, multiple -v options increase verbosity.", 
                count=True)
@click.option('-c', '--config', required=False, 
                help="Specifies an alternative config file",
                type=click.Path())
@click.option('--curl/--no-curl', default=False,
                help="Only show example curl commands")
def main(**kwargs):
    if kwargs['verbose'] > 1:
        loglevel = logging.DEBUG
    elif kwargs['verbose'] > 0:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    path = 'logging.yaml'
    if os.path.exists(path):
        with open(path, 'rt') as config_file:
            config = yaml.safe_load(config_file.read())
            logging.config.dictConfig(config)

    # As hem supports per check verification settings, don't warn on these
    urllib3.disable_warnings()
    logging.getLogger().setLevel(level=loglevel)
    logger = logging.getLogger(__name__)
    config = hemApp.load_config(kwargs['config'])


    metrics = hemApp.initialise_metrics(config['metrics'])

    if not 'settings' in config:
        config['settings'] = {}
    frequency = config['settings'].get('frequency', 30)
    logger.info("Frequency is {}".format(frequency))
    logger.info(config)
    storage = hemApp.HemStore()
    if kwargs['curl']:
        hemApp.curl_commands(config)
        exit()
    
    while True:
        duration = hemApp.run_tests(config, metrics, storage)
        try:
            if int(frequency - duration) > 0:
                time.sleep(int(frequency - duration))
        except IOError:
            logger.info("Too quick!")


if __name__ == '__main__':
    main()
