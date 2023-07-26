#!/bin/bash
fission spec init
fission env create --spec --name acc-data-update-env --image nexus.sigame.com.br/fission-account-update-user-data:0.1.2 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name acc-data-update-fn --env acc-data-update-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name acc-data-update-rt --method PUT --url /account/update_user --function acc-data-update-fn
