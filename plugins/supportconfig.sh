#!/bin/bash
echo "Now running supportconfig (this may take a while)"
sudo supportconfig -QR ../logs
sudo chown `whoami` ../logs/scc_*
