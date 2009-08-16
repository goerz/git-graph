#!/usr/bin/python
import os
import re
import sys

pref = re.compile(r'^(?P<hash>[0-9a-f]+) refs/(?P<name>.*)')
pgraph = re.compile(r'^(?P<graph>[\s\\/\*|]+)(?P<longhash>[0-9a-f]+) (?P<hash>[0-9a-f]+) : (?P<message>.*)')
pgraph_join = re.compile(r'^(?P<graph>[\s\\/\*|]+)')

BOLD = '\033[1m'
BLUE = '\033[94m'
ENDC = '\033[0m'


hashes = {}

refs = os.popen('git show-ref', 'r', 0)
for line in refs:
    refmatch = pref.match(line)
    if refmatch:
        hashes[refmatch.group('hash')] = refmatch.group('name')
    else:
        print "Unexpected ref format"
        print line
        sys.exit()

graph = os.popen(
'git log --all --pretty=format:\'%H %h : %s\' --date-order --graph', 'r', 0)
for line in graph:
    graphmatch = pgraph.match(line)
    if graphmatch:
        has_ref = False
        for hash in hashes.keys():
            if hash.startswith(graphmatch.group('hash')):
                print "%s%s : %s %s" % (
                    graphmatch.group('graph'),
                    graphmatch.group('hash'),
                    BOLD + BLUE + '[' + hashes[hash] + ']' + ENDC,
                    graphmatch.group('message'),
                )
                has_ref = True
        if not has_ref:
            print "%s%s : %s" % (
                graphmatch.group('graph'),
                graphmatch.group('hash'),
                graphmatch.group('message'),
            )
    else:
        if pgraph_join.match(line):
            sys.stdout.write(line)
        else:
            print "Unexpected graph format"
            print line
            sys.exit()

