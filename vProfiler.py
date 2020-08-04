#!/usr/bin/env python3
import argparse
import os


parser = argparse.ArgumentParser()
metavars = {}

with open("plugins.csv", "r") as plugins:
    for line in plugins:
        if(line == "===\n"):
            break
        argument = [item.strip() for item in line.split(',')]
        if(len(argument) < 2):
            continue
        elif(len(argument) == 2):
            parser.add_argument("--"+argument[0], action="store_true")
        else:
            metavars[argument[0]] = argument[2:]
            parser.add_argument("--"+argument[0], nargs=len(argument[2:]), help=argument[1], type=str, metavar=tuple(argument[2:]))
    args = vars(parser.parse_args())

    for line in plugins:
        plugin = [item.strip() for item in line.split(',')]
        if(len(plugin) < 2):
            continue
        elif(plugin[0] == ''):
            print(plugin[1])
            os.system(plugin[1])
        elif(args[plugin[0]]):
            command = plugin[1]
            try:
                for (key, value) in zip(metavars[plugin[0]], args[plugin[0]]):
                    command = command.replace(key,value)
            except KeyError:
                pass
            print(command)
            os.system(command)

    

    
