#!/bin/bash
fission spec init
fission env create --spec --name user-update-env --image nexus.sigame.com.br/fission-async-cx:0.0.1 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name user-update-fn --env user-update-env --src "./func/*" --entrypoint main.update_user_data --executortype newdeploy --maxscale 1
fission route create --spec --name user-update-rt --method PUT --url /onboarding/update_user --function user-update-fn
