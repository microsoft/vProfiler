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

# Used to do plugin paramenter / argument replacement in a single pass
def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

# Get the Linux Distribution for support checking
#  - platform.linux_distribution() is technically depricated but distro.linux_distribution()
#    is not yet supported on many LTS distros 
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

# ARGUMENT PARSING
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--config", help="Sets the YAML file to use as list of plugins",
                    metavar="FILE", default="plugins.yaml")
parser.add_argument("--quiet", help="Suppress output messages", action="store_true")

args = parser.parse_known_args()[0]

# Open the pligin list and populate the argparser
with open(args.config, "r") as file:
    plugins = yaml.safe_load(file)

parser = argparse.ArgumentParser(parents=[parser],
                                 description="A tool to collect, analyze, and export system information from a Linux machine running on HyperV. Many of vProfiler's actions require superuser permissions, but vProfiler will not modify your system.",
                                 epilog="Default behavior: --" + " --".join(plugins["default"]))
for name in plugins:
    if name == "default":
        continue
    plugin = plugins[name]
    if not "description" in plugin:
        plugin["description"] = ""
    if "params" in plugin:
        parser.add_argument("--"+name, nargs=len(plugin["params"]), help=plugin["description"], type=str, metavar=tuple(plugin["params"]))
    else:
        parser.add_argument("--"+name, help=plugin["description"], action="store_true")

args = vars(parser.parse_args())

# Run default behavior if no plugins are activated by options
if all((x == "default" or not args[x]) for x in plugins):
    for name in plugins["default"]:
        if name not in args:
            print("Warning: Default flag " + name + " is not a defined plugin", file=sys.stderr)
        args[name] = plugins["default"][name]

# Activate any plugins listed in the "also_run" sections of activated plugins
for name in reversed(plugins):
    if name == "default":
        continue
    if args[name] and "also_run" in plugins[name]:
        for plg in plugins[name]["also_run"]:
            args[plg] = plugins[name]["also_run"][plg]

print("Many of vProfiler's actions require superuser permissions, but vProfiler will not modify your system.", flush=True)
if not os.path.exists('logs'):
    os.makedirs('logs')
            
# Run the plugins
for name in plugins:
    if name == "default":
        continue
    plugin = plugins[name]
    if "supported_distros" in plugin and not LNX_DST in plugin["supported_distros"]:
        continue
    if args[name] and "cmds" in plugin:
        if "message" in plugin and not args["quiet"]:
           print(plugin["message"], flush=True)
        if "params" in plugin:
            # ArgParse enforces the parameter number so this error only happens
            #  if there is a mistake in plugins.yaml
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
