#!/usr/bin/python2

import re
import os
import logging
import argparse
import note
import threadpool
import shutil 

logger = logging.getLogger('taskn_admin')

########## Utility Functions ##########

def mkdir_if_needed(name, base):
    dir = os.path.join(base, name)
    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir

def symlink(name, target):
    if not os.path.islink(name):
        try:
            os.symlink(target, name)
        except AttributeError:
            from win32file import CreateSymbolicLink
            CreateSymbolicLink(name, target)
        except ImportError:
            logger.critical('platform does not contain support for symlinks. Windows users need to pywin32.')
            exit(1)

def worker_pool(jobs, func, *args):
    p = threadpool.ThreadPool(len(jobs))
    for item in jobs:
        p.putRequest(threadpool.WorkRequest(func, args=[item] + [ i for i in args]))
    p.wait()

########## Heavy Lifting ##########

def move_if_needed(src, dst, cond=None, value=None):
    if cond == value:
        if not os.path.exists(src):
            logger.debug('not moving {0} to {1}: source file doesn\'t exist'.format(src, dst))
        elif os.path.exists(os.path.join(dst, os.path.basename(src))):
            logger.warning('not moving {0} to {1}: destination file exists'.format(src, dst))
        else:
            shutil.move(src, dst)
            logger.debug('moved {0} to {1}'.format(src, dst))
    else:
        logger.debug('not moving {0} to {1}: {2} != {3}'.format(src, dst, cond, value))

def note_symlink(name, source, alias_dir):
    alias_path = os.path.join(alias_dir, name)

    if os.path.exists(alias_path):
        if os.readlink(alias_path) == source:
            logger.debug('not creating symlink "{0}" because it exists'.format(alias_path))
        elif not os.path.islink(alias_path):
            logger.warning('{0} is not a symbolic link. doing nothing'.format(alias_path))
        else:
            os.remove(alias_path)
            logger.debug('removed stale symlink to {0}'.format(alias_path))
            symlink(alias_path, source)
            logger.debug('created link from {0} to {1}'.format(source, name))
    else:
        symlink(alias_path, source)
        logger.debug('created link from {0} to {1}'.format(source, name))

########## Worker Wrapper Function ##########

def _move_note_if_needed(task, archive_dir, query):
    move_if_needed(task['note'], archive_dir, task['status'], query)

def _create_note_symlink(task, alias_dir):
    bugw_re = re.compile(r'\(bw\).*\#.* - (.*) \.\. .*')
    delim_re = re.compile(r'[\:\;\-\.\,\_]')

    name = bugw_re.sub(r'\1', task['task'])
    name = delim_re.sub(r' ', name)
    name = '-'.join(name.split()) 
    name = '.'.join([name, 'txt'])

    note_symlink(name, task['note'], alias_dir)
    
########## Major Functionality Wrappers ##########

def archive_stale(tasks, dir):
    archive_dir = mkdir_if_needed('archive', dir)

    worker_pool(tasks, _move_note_if_needed, archive_dir, 'completed')

def generate_aliases(tasks, dir):
    alias_dir = mkdir_if_needed('aliases', dir)

    worker_pool(tasks, _create_note_symlink, alias_dir)

########## User Interface ##########

def user_input():
    parser = argparse.ArgumentParser('administrative operations for tasknote management')

    parser.add_argument('--logfile', default=None)
    parser.add_argument('--debug', '-d', default=False, action="store_true")
    parser.add_argument('--notesdir', '-n', default=os.path.join(os.environ['HOME'], '.tasknote'))
    parser.add_argument('--ext', default='txt')
    parser.add_argument('cmd', nargs=1, default='list')

    return parser.parse_args()

def main():
    ui = user_input()
    note.init_logging(ui.logfile, ui.debug)

    tasks = note.list_tasks(None, ui.notesdir, ui.ext)

    if ui.cmd[0] == 'archive':
        archive_stale(tasks, ui.notesdir)
    elif ui.cmd[0] == 'alias':
        generate_aliases(tasks, ui.notesdir)

if __name__ == '__main__':
    main()
