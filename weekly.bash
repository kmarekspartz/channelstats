#! /usr/bin/env bash

BASEDIR=$(dirname "$0")
cd $BASEDIR
git pull

set -x
./user_downloader.py
./channel_downloader.py
./message_downloader.py
./user_and_channel_report
./slack_report.py --destination \#zmeta-statistics
set +x
