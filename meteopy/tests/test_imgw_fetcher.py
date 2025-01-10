import pytest
from meteopy.data_fetchers.imgw_fetcher import IMGWDataFetcher


def test_fetch(mocker):
    """Testuje metodę fetch."""
    mocker.patch("requests.get")
    requests.get.return_value.status_code = 200
    requests.get.return_value.text = "file1.csv\nfile2_2023.csv\nfile3.txt"

    fetcher = IMGWDataFetcher()
    result = fetcher.fetch("https://example.com/catalog", "2023")

    assert result == ["file2_2023.csv"]

def test_download_file(mocker, tmp_path):
    """Testuje metodę download_file."""
    mocker.patch("requests.get")
    requests.get.return_value.status_code = 200
    requests.get.return_value.iter_content = lambda chunk_size: [b"data"]

    fetcher = IMGWDataFetcher()
    fetcher.download_dir = tmp_path / "downloaded"
    fetcher.download_dir.mkdir()

    file_url = "https://example.com/file.zip"
    local_file = fetcher.download_dir / "file.zip"

    fetcher.download_file(file_url)

    assert local_file.exists()

def test_download_and_unzip(mocker, tmp_path):
    """Testuje pobieranie i wypakowywanie pliku ZIP."""
    mocker.patch("requests.get")
    mocker.patch("zipfile.ZipFile")
    requests.get.return_value.status_code = 200
    requests.get.return_value.iter_content = lambda chunk_size: [b"data"]

    fetcher = IMGWDataFetcher()
    fetcher.download_dir = tmp_path / "downloaded"
    fetcher.download_dir.mkdir()

    file_url = "https://example.com/file.zip"
    local_file = fetcher.download_dir / "file.zip"

    fetcher.download_file(file_url, unzip=True)

    assert local_file.exists()
    zipfile.ZipFile.assert_called_once_with(local_file, 'r')