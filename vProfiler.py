#!/usr/bin/env python3
import yaml
import os
import argparse
import re
import sys

def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

LNX_DST = None
try:
    import distro
    LNX_DST = distro.linux_distribution()[0]
except ModuleNotFoundError:
    try:
        import platform
        LNX_DST = platform.linux_distribution()[0]
    except ModuleNotFoundError:
        print("Could not determine Linux Distribution", "Please pip install distro or platform")

parser = argparse.ArgumentParser()

with open("plugins.yaml", "r") as file:
    plugins = yaml.load(file)
    for name in plugins:
        if name == "default":
            continue
        plugin = plugins[name]
        if "params" in plugin:
            parser.add_argument("--"+name, nargs=len(plugin["params"]), help=plugin["description"], type=str, metavar=tuple(plugin["params"]))
        else:
            parser.add_argument("--"+name, help=plugin["description"], action="store_true")

args = vars(parser.parse_args())
if len(sys.argv) == 1:
    for name in plugins["default"]:
        args[name] = plugins["default"][name]

for name in args:
    if args[name] and "also_run" in plugins[name]:
        for plg in plugins[name]["also_run"]:
            args[plg] = plugins[name]["also_run"][plg]

for name in args:
    if name == "default":
        continue
    plugin = plugins[name]
    if "supported_distros" in plugin and not LNX_DST in plugin["supported_distros"]:
        continue
    if args[name] and "cmds" in plugin:
        if "params" in plugin:
            subs = {}
            for (var, val) in zip(plugin["params"], args[name]):
                subs[var] = val
            for cmd in plugin["cmds"]:
                os.system(replace(cmd, subs))
        else:
            for cmd in plugin["cmds"]:
                os.system(cmd)
