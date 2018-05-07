from unittest.mock import patch
from pykafka import KafkaClient
@patch('pykafka.KafkaClient')
def test_check_init(MockKafka):
    import hemApp
    metrics = hemApp.initialise_metrics({"type":"kafka"})
    assert hemApp.drivers.metrics_kafka.instance is type(metrics)
    assert MockKafka.called_once_with('localhost','9092')
    metrics.stage('test_metric', 100)
    assert MockKafka.called
