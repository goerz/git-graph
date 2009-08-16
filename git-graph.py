#!/usr/bin/python
import os
import re
import sys

pref = re.compile(r'^(?P<hash>[0-9a-f]+) refs/(?P<name>.*)')
pgraph1 = re.compile(r'^(?P<graph>[\s\\/\*|]+)(?P<longhash>[0-9a-f]+) (?P<hash>[0-9a-f]+) : (?P<info>.*)$')
pgraph2 = re.compile(r'^(?P<graph>[\s\\/\*|]+) (?P<message>.*)$')
pgraph3 = re.compile(r'^(?P<graph>[\s\\/\*|]+)$')

BOLD = '\033[1m'
BLUE = '\033[94m'
ENDC = '\033[0m'


ref_for_hash = {}

refs = os.popen('git show-ref', 'r', 0)
for line in refs:
    refmatch = pref.match(line)
    if refmatch:
        ref_for_hash[refmatch.group('hash')] = refmatch.group('name')
    else:
        print "Unexpected ref format"
        print line
        sys.exit()

graph = os.popen(
'git log --all --pretty=format:\'%H %h : %an %ai %n %s%n\' --date-order --graph', 'r', 0)
for line in graph:
    graphmatch = pgraph1.match(line)
    if graphmatch:
        if ref_for_hash.has_key(graphmatch.group('longhash')):
            print "%s%s : %s %s" % (
                graphmatch.group('graph'),
                graphmatch.group('hash'),
                BOLD + BLUE + 
                '[' + ref_for_hash[graphmatch.group('longhash')] + ']' 
                + ENDC,
                graphmatch.group('info'),
            )
        else:
            print "%s%s : %s" % (
                graphmatch.group('graph'),
                graphmatch.group('hash'),
                graphmatch.group('info'),
            )
    else :
        graphmatch = pgraph2.match(line)
        if graphmatch:
            print "%s %s" % (
                graphmatch.group('graph'),
                graphmatch.group('message')
            )
        elif pgraph3.match(line):
            sys.stdout.write(line)
        else:
            print "Unexpected graph format"
            print line
            sys.exit()

