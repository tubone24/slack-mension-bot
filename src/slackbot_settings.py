# coding: utf-8
import yaml


def load_config():
    with open("config.yaml") as f:
        config = yaml.load(f)
        return config


config = load_config()

API_TOKEN = config["slack"]["token"]

DEFAULT_REPLY = "あああああああああ"

PLUGINS = ["plugins.mention_watcher"]
