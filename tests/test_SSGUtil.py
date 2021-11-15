from ssg.SSGUtil import (
    get_accepted_files,
    output_to_file,
    get_config,
    create_output_dir,
    add_asset,
    OUTPUT_FOLDER,
)
import unittest.mock as mock
import os
import pytest


# Should return list of accepted files from directory
def test_get_accepted_files(tmp_path):
    path = tmp_path / "get_accepted_files"
    path.mkdir()

    (path / "md.md").write_text("1")
    (path / "txt.txt").write_text("1")
    (path / "html.html").write_text("1")
    (path / "jpg.jpg").write_text("1")

    assert get_accepted_files(path) == ["md.md", "txt.txt"]


# Should create output file
def test_output_to_file(tmp_path):
    FILE_NAME = "test.txt"
    HTML_CONTENT = "<html><p>Hello World</p></html>"
    OUT_FOLDER = tmp_path / OUTPUT_FOLDER
    OUT_FILE = str(OUT_FOLDER) + "/test/index.html"

    with mock.patch("ssg.SSGUtil.OUTPUT_FOLDER", str(OUT_FOLDER)):
        output_to_file(FILE_NAME, HTML_CONTENT)

    assert os.path.isfile(OUT_FILE)

    with open(OUT_FILE, "r") as f:
        assert HTML_CONTENT == f.read()


# Should return all values
def test_get_config(tmp_path):
    CONFIG_PATH = str(tmp_path) + "/config.json"
    CONFIG_CONTENT = """
    {
        "input": "../../Sherlock Holmes Selected Stories",
        "lang": "en-US",
        "stylesheet": "https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css"
    } """

    (tmp_path / "config.json").write_text(CONFIG_CONTENT)

    input, lang, stylesheet = get_config(CONFIG_PATH, None, None, None)

    assert input == "../../Sherlock Holmes Selected Stories"
    assert lang == "en-US"
    assert stylesheet == "https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css"


# Only input key should return input value
def test_get_config1(tmp_path):
    CONFIG_PATH = str(tmp_path) + "/config.json"
    CONFIG_CONTENT = """
    {
        "input": "../../Sherlock Holmes Selected Stories"
    } """

    (tmp_path / "config.json").write_text(CONFIG_CONTENT)

    input, lang, stylesheet = get_config(CONFIG_PATH, None, None, None)

    assert input == "../../Sherlock Holmes Selected Stories"
    assert lang is None
    assert stylesheet is None


# No input key should exit with code 1
def test_get_config2(tmp_path):
    CONFIG_PATH = str(tmp_path) + "/config.json"
    CONFIG_CONTENT = """
    {
        "stylesheet": "https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css"
    } """

    (tmp_path / "config.json").write_text(CONFIG_CONTENT)

    with pytest.raises(SystemExit) as e:
        get_config(CONFIG_PATH, None, None, None)

    assert e.type == SystemExit
    assert e.value.code == 1


# Only input and lang keys should be returned
def test_get_config3(tmp_path):
    CONFIG_PATH = str(tmp_path) + "/config.json"
    CONFIG_CONTENT = """
    {
        "input": "../../Sherlock Holmes Selected Stories",
        "lang": "en-US"
    } """

    (tmp_path / "config.json").write_text(CONFIG_CONTENT)

    input, lang, stylesheet = get_config(CONFIG_PATH, None, None, None)

    assert input == "../../Sherlock Holmes Selected Stories"
    assert lang is None
    assert stylesheet is None


# Should create output folder with assets folder inside
def test_create_output_dir(tmp_path):
    OUT_FOLDER = tmp_path / OUTPUT_FOLDER

    with mock.patch("ssg.SSGUtil.OUTPUT_FOLDER", str(OUT_FOLDER)):
        create_output_dir()

    assert os.path.isdir(str(OUT_FOLDER) + "/assets")


# Should create asset file in "type" folder contained in output folder
def test_add_asset(tmp_path):
    CSS_CONTENT = "h1 {}"
    OUT_FOLDER = tmp_path / OUTPUT_FOLDER
    OUT_FILE = str(OUT_FOLDER) + "/assets/css/test.css"

    with mock.patch("ssg.SSGUtil.OUTPUT_FOLDER", str(OUT_FOLDER)):
        add_asset("css", "test.css", CSS_CONTENT)

    assert os.path.isfile(OUT_FILE)

    with open(OUT_FILE, "r") as f:
        assert CSS_CONTENT == f.read()
