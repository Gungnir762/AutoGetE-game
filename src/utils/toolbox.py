# -*- coding: utf-8 -*-
# Time       : 2022/1/16 0:27
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from __future__ import annotations

import inspect
import sys
from typing import Dict, Any

from loguru import logger


def init_log(**sink_channel):
    event_logger_format = "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | <lvl>{level}</lvl> - {message}"
    serialize_format = event_logger_format + "- {extra}"
    logger.remove()
    logger.add(
        sink=sys.stdout, colorize=True, level="DEBUG", format=serialize_format, diagnose=False
    )
    if sink_channel.get("error"):
        logger.add(
            sink=sink_channel.get("error"),
            level="ERROR",
            rotation="1 week",
            encoding="utf8",
            diagnose=False,
            format=serialize_format,
        )
    if sink_channel.get("runtime"):
        logger.add(
            sink=sink_channel.get("runtime"),
            level="DEBUG",
            rotation="20 MB",
            retention="20 days",
            encoding="utf8",
            diagnose=False,
            format=serialize_format,
        )
    if sink_channel.get("serialize"):
        logger.add(
            sink=sink_channel.get("serialize"),
            level="DEBUG",
            format=serialize_format,
            encoding="utf8",
            diagnose=False,
            serialize=True,
        )
    return logger


def from_dict_to_model(cls, data: Dict[str, Any]):
    return cls(
        **{
            key: (data[key] if val.default == val.empty else data.get(key, val.default))
            for key, val in inspect.signature(cls).parameters.items()
        }
    )
