#!/usr/bin/python
import optparse
import os
import sys
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/tnet'))

import tnet


class Error(Exception):

    pass


def log(msg, *args):
    if args:
        msg = msg % args
    print >> sys.stderr, msg


def CreateOptionsParser():
    parser = optparse.OptionParser()

  # Other options:
  # Capture stderr and put it in the record.  Normally it goes to the terminal.
  # -N like xargs?
  # You could get multiple files with curl...
  # The syntax is -O filename1 url1 -O filename2 url2, or something like that.

    parser.add_option(
        '-I',
        '--replace-str',
        dest='replace_str',
        type='str',
        default='_',
        help='Placeholder for the input value.  Only applicable when it is a string and not an array.  This is analogous to xargs -I.'
            ,
        )

  # Technically this could be done with 'sh -c "cd dir; $cmd' on the input, but
  # it relieves quoting problems.  TODO: think of a better way?  Could we
  # somehow execute a sequence of shell commands?

    parser.add_option(
        '-d',
        '--directory',
        dest='directory',
        type='str',
        default='',
        help='Current working directory of command',
        )

  # Hm, this syntax could be $1 like Rpeg.  And @1 to splice it in.

    return parser


def _ExpandTemplate(arg_template, value, replace_str):

  # For now, _ stands for the value, and that's it.  No escaping.
  # This should be replaced with JSON Stack at some point.

    argv = []
    for a in arg_template:
        if a == replace_str:
            argv.append(value)
        else:
            argv.append(a)
    return argv


def main(argv):
    """Returns an exit code."""

    (options, argv) = CreateOptionsParser().parse_args(argv)

    pid = os.getpid()

    log('Hello from exec.py, pid %d', pid)

  # _ just stands for the value

    arg_template = argv[1:] or [options.replace_str]

    while True:
        value = sys.stdin.readline().strip()
        if (len(value) == 0):
            break
            

        if isinstance(value, str):
            argv = _ExpandTemplate(arg_template, value,
                                   options.replace_str)
        elif isinstance(value, list):
            argv = value
        else:
            raise Error('Value should be list or string: %r' % value)

        log('exec: Running %s', argv)

    # stderr goes to this wrapper process's stderr (which can be logged by xmap)

        if options.directory:
            p = subprocess.Popen(argv, stdout=subprocess.PIPE,
                                 cwd=options.directory)
        else:
            p = subprocess.Popen(argv, stdout=subprocess.PIPE)
        stdout = p.stdout.read()
        exit_code = p.wait()

        response = {'input': value, 'status': exit_code,
                    'stdout': stdout}

        sys.stdout.write(tnet.dumps(response))

    # This is needed -- otherwise we would get 4K of responses at once...

        sys.stdout.flush()

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except Error, e:
        print >> sys.stderr, e.args[0]
        sys.exit(1)
