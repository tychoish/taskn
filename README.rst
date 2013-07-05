============================================
``taskn`` -- Notebook System for TaskWarrior
============================================

``taskn`` is a note taking system for TaskWarrior, designed as an
expansion of the `tasknote
<http://taskwarrior.org/projects/taskwarrior/wiki/Tasknote>`_
script. It offers the following additional features:

- "aliases" to allow you to access note files directly via symlinks. 

- "archives" to migrate notes for completed tasks out of your main
  working folder.

- reporting. ``taskn`` outputs reports of current notes and associated
  tasks as YAML streams for easy reading on the console and use by
  other programs.
  
- performance at scale. ``taskn`` performance will not degrade
  linearly as you add tasks and notes.

Requirements
------------

- Python 2.7 
  
- A collection of fine Python Modules: ``taskw``, ``threadpool``, and
  ``pyyaml``. 

- TaskWarrior.

Get Started!
------------

The best way to install ``taskn`` is to use ``pip`` or
``easy_install`` to install the package from `PyPi
<https://pypi.python.org/pypi/taskn>`_. [#pkg]_ Issue one of the
following commands to install ``taskn``: ::
  
  pip install taskn

  easy_install taskn

Alternately, you can install from source with the following sequence
of operations: ::
  
  git clone git@github.com:tychoish/taskn.git

  cd taskn

  python setup.py install 

.. [#pkg] If you're interested in packaging ``taskn`` for a system
   package manager, please do coordinate with me and I'll add that to
   the instructions here.

Documentation
-------------

When you install ``taskn`` you will have two new shell scripts in your
path: ``taskn`` and ``tasknadm``. The following sections provide an
inventory of the interface common operations.

``taskn``
~~~~~~~~~

``taskn`` commands generally take the following form: ::
  
  taskn <options> <task_id>

``<options>`` specifies one of the following options, while
``<task_id>`` is one of the current ordinal task identifiers. Given
the following command: ::
  
  taskn 12
  
``taskn`` will open a note for task #12 in your editor. Consider the
following assumptions and finer points.

- The note will be located in the notes directory (``--notesdir``)
  which defaults to ``~/.tasknote``. If the notes directory does note
  exist ``taskn`` will create it.
  
- The note will have the ``.txt`` extension (``--ext``.) The name of
  the file is the TaskWarrior UUID. 
  
- If you have a previous note, for this task, ``taskn`` opens it. Each
  task can only have one note. 
  
- When you save the note, ``taskn`` will add an annotation to the task
  with the content of the first line of your note file. If you change
  the first line of your file, tasknote will update the annotation.

The following examples all specific "long form"  command line
options. Short forms exist for convince.

Lists
`````

If you call ``taskn`` without any arguments, ``taskn`` prints a
sequence of YAML documents for each note associated with a pending
task. To list all, including completed tasks, use the following
operation: ::
  

  taskn --list

You can filter results based on status using the ``--filter`` options:
::
   
  taskn --list --filter deleted
  
Possible filters are: ``pending``, ``deleted``, ``completed``,
``waiting``, and ``recurring``.

Views
`````

You can use the ``--view`` and ``--format`` arguments to display task
and note information on the console, as in the following: ::
  
  taskn --view 12
  
This operation outputs a YAML document of the task, and adds the note
to the output. To return JSON output, use ``--format`` as follows: :: 

  taskn --view 12 --format json

.. important:: ``taskn`` does not sanitize the YAML output of note
   data.

Default Behavior
````````````````

The following options allow users to control default behavior. 

``--notesdir``
   Specifies the directory that holds the notes. Defaults to
   ``~/.tasknote``. 

``--ext``
   Sepecifies the default extension for notes. Defaults to ``.txt``.

``--editor``
   By default, ``taskn`` use ``$VISUAL`` from the environment. Specify
   a different editor with ``--editor``. 

``--strict`` 
   Prevents ``taskn`` from creating the ``--notesdir`` if it doesn't
   currently exist.

``--async``
   By default, ``taskn`` will wait for the editor to exit to annotate
   the task. If you specify ``--async``, ``taskn`` does not wait for
   the editor *and* will *not* annotate the task.

Other Options
`````````````

``--logfile``
   Specify a file to write information and status output. Lowers the
   threshold to ``WARNING`` from ``CRITICAL``. The logfile is not
   required.

``--debug``
   Lowers the logging threshold from ``CRITICAL`` to ``DEBUG`` which
   outputs all messages.

``tasknadm``
~~~~~~~~~~~~

Commands
````````

``tasknadm`` has two sub-commands: 

``archive``
   Moves all notes that refer to completed tasks to the ``archive``
   sub-directory of the current note directory.

``alias``
   Creates symbolic links in the ``aliases`` sub-directory of the
   current note directory to all current and archived notes. The names
   of these links derive from the task description, and allow direct
   editing of existing notes using a conventional workflow and editing
   experience.

Options
```````

Like ``taskn``, ``taskadm`` has the following (related options): 

``--logfile``
   Specify a file to write information and status output. Lowers the
   threshold to ``WARNING`` from ``CRITICAL``. The logfile is not
   required.

``--debug``
   Lowers the logging threshold from ``CRITICAL`` to ``DEBUG`` which
   outputs all messages.

``--notesdir``
   Specifies the directory that holds the notes. Defaults to
   ``~/.tasknote``. 

``--ext``
   Sepecifies the default extension for notes. Defaults to ``.txt``.

Development Goals
-----------------

- Filtering notes by tag.
  
- Unified primary/administrative interface. 

- Better/Any API to provide access to notes. 

- Full documentation.
  
- Test suite with unit and functional tests.
