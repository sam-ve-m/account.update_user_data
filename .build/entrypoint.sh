#!/bin/sh
set -e

# Input envs for application
source /opt/app/.env/config

rm -rf /opt/app/.env/config

# Start apps

python server.py
