#!/usr/bin/env python3
import os
import argparse
import re
import sys

try:
    import yaml
except ModuleNotFoundError:
    print("The python package yaml is required for this tool.", file=sys.stderr)
    print("Please try pip install pyyaml", file=sys.stderr)
    quit()

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
        print("Could not determine Linux Distribution", "Please pip install distro or platform", file=sys.stderr)

parser = argparse.ArgumentParser()

with open("plugins.yaml", "r") as file:
    plugins = yaml.safe_load(file)
for name in plugins:
    if name == "default":
        continue
    plugin = plugins[name]
    if not "description" in plugin:
        print(name + " Error: decription field is required", file=sys.stderr)
        print("This will cause a runtime error if the plugin is activated in default behavior.\n", file=sys.stderr)
        continue
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
            if len(plugin["params"]) != len(args[name]):
                print(name + " Error: incorrect number of parameters", file=sys.stderr)
                continue
            subs = {}
            for (var, val) in zip(plugin["params"], args[name]):
                subs[var] = val
            for cmd in plugin["cmds"]:
                os.system("cd plugins;" + replace(cmd, subs))
        else:
            for cmd in plugin["cmds"]:
                os.system("cd plugins;" + cmd)
