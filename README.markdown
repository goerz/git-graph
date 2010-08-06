# git-graph

[http://github.com/goerz/git-graph](http://github.com/goerz/git-graph)

Author: [Michael Goerz](http://michaelgoerz.net)

The git-graph.py script shows an ascii-art graph of all git commits in the
repository. If the output is not redirected, it is shown in a pager.  The
command is more or less  a wrapper around 'git log --graph', but with better
formatting of the refs and the option to show svn commit numbers, which is
useful for planning a svn merge.

This code is licensed under the [GPL](http://www.gnu.org/licenses/gpl.html)

## Install ##

Store the git-graph.py script anywhere in your `$PATH`

## Dependencies ##

* You must have [git][1] installed

[1]: http://git-scm.com/

## Usage ##

    Usage: git_graph.py [options] [path] 
    
    Options:
      -h, --help            show this help message and exit
      --no-hash             Don't print the commit hash
      --no-color            Don't mark refs with color
      --color               Mark refs with color even if output is redirected
      --oneline             Print only one line per commit
      --svn                 Print svn revision number
      --pager=PAGER         Set pager (default: less -RS)
      --date=DATE           Set date format. Possible values are 'relative',
                            'local', 'iso', 'fc', 'short' (default), 'raw',
                            'default'. For an explanation, see 'git help log'
      --max-length=MAX_LENGTH
                            Set maximum line length
