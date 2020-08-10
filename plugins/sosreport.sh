#!/bin/bash

sudo sosreport --batch --quiet --tmp-dir ../logs/
sudo chown `whoami` ../logs/sosreport*
