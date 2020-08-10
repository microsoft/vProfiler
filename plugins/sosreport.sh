#!/bin/bash
echo "Now running sosreport (this may take a while)"
sudo sosreport --batch --quiet --tmp-dir ../logs/
sudo chown `whoami` ../logs/sosreport*
