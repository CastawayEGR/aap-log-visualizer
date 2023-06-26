""" Python tests for main.py """
# pylint: disable=duplicate-code
from unittest.mock import mock_open, patch
import pytest
from main import (
    update_promtail_config,
    start_grafana_server,
    start_loki_server,
    start_promtail,
    check_ready,
    sigterm_handler,
)


@pytest.fixture
def mock_response():
    """ Mock the response from the requests.get function """
    class MockResponse:
        """ Class to handle response.text """
        def __init__(self, text):
            self.text = text
            self.status_code = 200

    return MockResponse("ready")


def test_update_promtail_config(mock_template_file="Timezone: America/New_York"):
    """ Test the update_promtail_config function """
    # Set up template_content
    template_content = "Timezone: $timezone"
    # Set up the necessary mocks
    with patch("builtins.open", mock_open(read_data=mock_template_file), create=True) as mock_file:
        # Mock the glob.glob function
        with patch("glob.glob") as mock_glob:
            # Mock the os.path.isdir function
            with patch("os.path.isdir") as mock_isdir:
                # Set the expected values for the mocks
                mock_isdir.return_value = True
                mock_glob.return_value = ["/logs/usr/share/zoneinfo/America/New_York"]

                # Call the function to update the promtail config
                update_promtail_config()

                # Verify that the necessary functions were called
                mock_isdir.assert_called_with("/logs/usr/share/zoneinfo")
                mock_glob.assert_called_with("/logs/usr/share/zoneinfo/*/*")
                mock_file.assert_called_with("/opt/promtail/promtail-config.yaml", "w",
                                             encoding="utf8")

    # Verify that the config file was written with the correct content
    with patch("builtins.open", mock_open(read_data=mock_template_file), create=True) as mock_file:
        with open(mock_file, "r", encoding="utf8") as file:
            config_content = file.read()

            # Define the expected content based on the conditions
            expected_content = template_content.replace("$timezone", "America/New_York")

        assert config_content == expected_content


def test_start_grafana_server():
    """ Test the start_grafana_server function """
    # Call the function to start Grafana server
    with patch("subprocess.Popen") as mock_popen:
        process_mock = mock_popen.return_value
        process_mock.wait.return_value = 0

        grafana_process = start_grafana_server()

        # Verify that the appropriate arguments were passed to subprocess.Popen
        mock_popen.assert_called_with([
            "/opt/grafana/bin/grafana-server",
            "-homepath",
            "/opt/grafana",
            "-config",
            "/opt/grafana/conf/grafana.ini",
            "$@",
            "cfg:default.log.mode=console",
        ])

        # Verify that the process was started and returned
        assert grafana_process == process_mock


def test_check_ready(mock_response):
    # pylint: disable=redefined-outer-name
    """ Test the loki api check_ready function """
    # Mock the requests.get function to return the desired response
    with patch("requests.get") as mock_get:
        # Configure the mock to return the mock response
        mock_get.return_value = mock_response

        # Call the function and assert that it breaks out of the loop when "ready" is received
        check_ready()

        # Verify that requests.get was called with the expected URL
        mock_get.assert_called_with("http://localhost:3100/ready", timeout=5)


def test_start_loki_server():
    """ Test the start_loki_server function """
    # Call the function to start Loki server
    with patch("subprocess.Popen") as mock_popen:
        process_mock = mock_popen.return_value
        process_mock.wait.return_value = 0

        loki_process = start_loki_server()

        # Verify that the appropriate arguments were passed to subprocess.Popen
        mock_popen.assert_called_with([
            "/opt/loki/loki-server",
            "--config.file",
            "/opt/loki/loki-local-config.yaml",
        ])

        # Verify that the process was started and returned
        assert loki_process == process_mock


def test_start_promtail():
    """ Test the start_promtail function """
    # Call the function to start Promtail
    promtail_config = "/opt/promtail/promtail-config.yaml"
    with patch("subprocess.Popen") as mock_popen:
        process_mock = mock_popen.return_value
        process_mock.wait.return_value = 0

        promtail_process = start_promtail(promtail_config)

        # Verify that the appropriate arguments were passed to subprocess.Popen
        mock_popen.assert_called_with([
            "/opt/promtail/promtail-agent",
            "-config.file",
            promtail_config,
        ])

        # Verify that the process was started and returned
        assert promtail_process == process_mock


def test_sigterm_handler(capsys):
    """ Test the sigterm_handler function """
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sigterm_handler()
    captured = capsys.readouterr()
    # Verify stdout message
    assert "AAP log visualizer is shutting down!" in captured.out

    # Verify sys.exit code is 0
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


# Run the tests
if __name__ == "__main__":
    pytest.main()
