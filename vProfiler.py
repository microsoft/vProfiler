#!/usr/bin/env python3
import argparse

import upload
import generate

parser = argparse.ArgumentParser()

parser.add_argument("--upload", nargs=2, help="upload a file to blob storage", type=str, metavar=('FILE', 'URL'))

args = parser.parse_args()


if(args.upload):
    FILE_NAME = args.upload[0]
    CONTAINER_URL = args.upload[1]
    upload.uploadFile(CONTAINER_URL, FILE_NAME)
else:
    generate.generate_sosreport()
