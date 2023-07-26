#!/bin/sh
docker build -t fission-account-update-user-data --secret id=pipconfig,src=$HOME/.pip.conf .
