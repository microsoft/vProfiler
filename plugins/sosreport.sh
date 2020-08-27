#!/bin/bash
sudo sosreport --batch --build --tmp-dir ../logs/
sudo chown -R `whoami` ../logs/sosreport*
