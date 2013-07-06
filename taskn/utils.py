import os
import logging
import yaml
import json

logger = logging.getLogger('taskn.utils')
__multi__ = 'thread'

if __multi__ == 'thread':
    logger.debug('using "threadpool" for the worker queue.')
    import threadpool

    def worker_pool(jobs, func, *args):
        p = threadpool.ThreadPool(len(jobs))
        for item in jobs:
            p.putRequest(threadpool.WorkRequest(func, args=[item] + [ i for i in args]))
        p.wait()

elif __multi__ == 'gevent':
    logger.debug('using "gevent" pools for the worker queue.')
    from  gevent.pool import Pool

    def worker_pool(jobs, func, *args):
        p = Pool(len(jobs))
        for item in jobs:
            p.spawn(func, item, *args)
        p.join()


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

def init_logging(logfile, debug=False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        if logfile is None:
            logging.basicConfig(level=logging.CRITICAL)
        else:
            logging.basicConfig(level=logging.WARNING, filename=logfile)

def expand_tree(path, input_extension):
    file_list = []

    for root, subFolders, files in os.walk(path):
        for file in files:
            f = os.path.join(root, file)

            if os.path.islink(f):
                continue
            elif f.endswith(input_extension):
                file_list.append(f)

    return file_list

def create_notes_dir(dir, strict):
    if not os.path.exists(dir):
        if not strict:
            logger.info("{0} notes directory doesn't exist. creating now.".format(dir))
            os.makedirs(dir)
        else:
            logger.critical('notes directory, "{0}" does not exist.'
                            'Create or restart without strict mode.'.format(dir))
            exit(1)

def dump_yaml(data):
    return yaml.safe_dump_all(data, default_flow_style=False, indent=3,
                         line_break=True) + '...'

def dump_json(data):
    return json.dumps(data, indent=3)
