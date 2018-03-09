import click
import logging
import hemApp
import time

@click.command()
@click.version_option()
@click.option('-v', '--verbose', count=True)
def main(**kwargs):
    if kwargs['verbose'] > 1:
        hemApp.setup_logging(default_level=logging.DEBUG)
    elif kwargs['verbose'] > 0:
        hemApp.setup_logging(default_level=logging.INFO)
    else:
        hemApp.setup_logging(default_level=logging.ERROR)
        
    config = hemApp.load_config()


    metrics = hemApp.initialise_metrics(config['metrics'])

    if not 'settings' in config:
        config['settings'] = {}
    frequency = config['settings'].get('frequency', 30)
    logging.info("Frequency is {}".format(frequency))
    logging.info(config)
    while True:
        duration = hemApp.run_tests(config, metrics)
        try:
            time.sleep(int(frequency - duration))
        except IOError:
            logging.info("Too quick!")


if __name__ == '__main__':
    main()
