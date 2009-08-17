#!/usr/bin/python
############################################################################
#    Copyright (C) 2009 by Michael Goerz                                   #
#    http://www.physik.fu-berlin.de/~goerz                                 #
#                                                                          #
#    This program is free software; you can redistribute it and/or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 3 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################
"""
This script shows an ascii-art graph of all git commits in the repository. 

"""
import os
import re
import sys
from optparse import OptionParser


BOLD = '\033[1m'
RED = '\033[91m'
BLUE = '\033[94m'
GREEN = '\033[92m'
ENDC = '\033[0m'


def get_refs():
    """
    Collect a dictionary of all the references in the repository
    """
    ref_for_hash = {}
    refs = os.popen('git show-ref', 'r', 0)
    pref = re.compile(r'^(?P<hash>[0-9a-f]+) refs/(?P<name>.*)')
    for line in refs:
        refmatch = pref.match(line)
        if refmatch:
            ref_for_hash[refmatch.group('hash')] = refmatch.group('name')
        else:
            print "Unexpected ref format"
            print line
            return None
    return ref_for_hash


def turn_off_colors():
    """
    Disable all (global) color codes
    """
    global BOLD
    BOLD = ''
    global RED
    RED = ''
    global BLUE
    BLUE = ''
    global GREEN
    GREEN = ''
    global ENDC
    ENDC = ''


def format_commit_ref(commit_ref):
    """
    Format a commit reference

    Remote refs are prefixed with 'r:' and colored in blue.
    Local refs are colored in green.
    Unknown refs are colored in red.
    """
    if commit_ref.startswith('remotes/'):
        commit_ref = commit_ref.replace('remotes/', 'r:', 1)
        commit_ref = BOLD + BLUE + '[' + commit_ref + ']' + ENDC
    elif ref.startswith('heads/'):
        commit_ref = commit_ref.replace('heads/', '', 1)
        commit_ref = BOLD + GREEN + '[' + commit_ref + ']' + ENDC
    else:
        commit_ref = BOLD + RED + '[' + commit_ref + ']' + ENDC
    return commit_ref


def main(options=None):
    """
    Print a graph of all commits to stdout.
    """
    ref_for_hash = get_refs()
    if ref_for_hash is None: return 1
    graph = os.popen(
        'git log --all --pretty=format:\'%H %h : %an %ai %n %s%n\' '+
        '--date-order --graph', 'r', 0)
    pgraph1 = re.compile(
        r'^(?P<graph>[\s\\/\*|]+)(?P<longhash>[0-9a-f]+) '
        +r'(?P<hash>[0-9a-f]+) : (?P<info>.*)$')
    pgraph2 = re.compile(
        r'^(?P<graph>[\s\\/\*|]+) (?P<message>.*)$')
    pgraph3 = re.compile(
        r'^(?P<graph>[\s\\/\*|]+)$')
    if options.no_color: turn_off_colors()
    for line in graph:

        graphmatch = pgraph1.match(line)

        if graphmatch:

            if ref_for_hash.has_key(graphmatch.group('longhash')):

                commit_hash = graphmatch.group('hash')

                commit_ref = ref_for_hash[graphmatch.group('longhash')]
                commit_ref = format_commit_ref(commit_ref)

                print "%s%s : %s %s" % (
                    graphmatch.group('graph'),
                    commit_hash,
                    commit_ref,
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
                return 1

    return 0


if __name__ == "__main__":
    arg_parser = OptionParser(usage = "git_graph.py [options] [path] ",
                              description = __doc__)
        
    arg_parser.add_option('--no-hash', action='store_true', dest='no_hash',
                        default=False, help="Don't print the commit hash")
    arg_parser.add_option('--no-color', action='store_true', dest='no_color',
                        default=False, help="Don't mark refs with color")
    options, args = arg_parser.parse_args(sys.argv)

    if len(args) > 1:
        os.chdir(args[1])

    sys.exit(main(options))
