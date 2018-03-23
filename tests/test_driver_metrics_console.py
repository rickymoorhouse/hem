
def test_check_init():
    import hemApp
    metrics = hemApp.initialise_metrics({"type":"console"})
    assert hemApp.drivers.metrics_console.instance is type(metrics)

def test_check_stage(capsys):
    import hemApp
    metrics = hemApp.initialise_metrics({"type":"console"})
    metrics.stage('hello',1)
    captured = capsys.readouterr()
    assert "hello" in captured.out
