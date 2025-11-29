#!/bin/sh
export PYTHONUNBUFFERED=1
python llm_proxy/proxy.py &
python bot.py
