# Standard Library
import unittest
from unittest import mock

# Dependencies
import pytest
from bs4 import BeautifulSoup


# From apps
from logic.app import Manganato


@mock.patch.object(Manganato, "get_directory_name")
@mock.patch("os.path.join")
@mock.patch("os.path.isdir")
def test_create_directory_success(
    m_os_path_isdir: mock.Mock,
    m_os_path_join: mock.Mock,
    m_get_directory_name: mock.Mock,
    web_data_main_page: BeautifulSoup,
):
    downloader = Manganato(web_data=web_data_main_page, directory_path=".")
    m_get_directory_name.return_value = "Fullmetal Alchemist"
    m_os_path_join.return_value = f"{downloader.directory_path}/{m_get_directory_name.return_value}"
    m_os_path_isdir.return_value = True
    response = downloader.create_directory()
    expected_response = m_os_path_join.return_value
    assert response == expected_response
    assert m_get_directory_name.call_count == 1
    assert m_os_path_join.call_count == 1
    assert m_os_path_isdir.call_count == 1


@unittest.skip("TO DO!")
@mock.patch.object(Manganato, "get_directory_name")
@mock.patch("os.path.join")
def test_create_directory_failure(
    m_os_path_join: mock.Mock,
    m_get_directory_name: mock.Mock,
    web_data_main_page: BeautifulSoup,
):
    pass
