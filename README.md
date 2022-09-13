# today

**A terminal program to help you plan your day and execute it in an organise way**

![screenshot_1](screenshots/screenshot_1.png)

![screenshot_2](screenshots/screenshot_2.png)

# Getting Started

Use `help` option to see full lust of arguments.

`./today.py -h`

```
positional arguments:
  Arguments          Task ID [int], Name [str], Duration [int]

options:
  -h, --help         show this help message and exit
  -a, --add          add/append a new Task [?ID][Name][Duration]
  -d, --done         mark a task as done [ID]
  -u, --undo         mark a task as undone [ID]
  -r, --remove       remove Task [ID]
  -t, --toggle       toggle Skip of Task [ID]
  -da, --done-all    mark all tasks as done
  -ua, --undo-all    mark all tasks as undone
  -p, --purge        purge Task Data
  -v, --retrieve     retrieve from Purged Task Data
  -n, --new-day      store current Task Data as Yesterday and start a new Day
  -y, --yesterday    Show Yesterday's Data
  -c, --settings     configure settings data
  -g, --read-notes   show notes
  -w, --add_note     add a new note
  -x, --remove-note  delete a note
```

Use `today -a task_name task_duration` to append a new task.

`today -a Exercise 20m`

Run the program with no optional arguments to see your day.

`today`

```
ID Time  Name                     Duration Skip     Done
0   7:00 Exercise                  0:40    False    True
1   7:40 Shower                    0:20    False    True
2   8:00 Cook                      1:00    False    True
3   9:00 Calculus Course           0:30    False    False    <---
4   9:30 Work on Project           2:00    False    False
5  11:30 Data Structure course     0:30    False    False
6  12:00 Cook                      1:00    False    False
7  13:00 Watch La Maesta de El St  3:00    False    False
8  16:00 Shower                    0:20    False    False
9  16:20 solve puzzles             0:40    False    False
10 17:00 practise typing           1:00    False    False
11 18:00 Work on Project           2:00    False    False
12 20:00 Read a Book               1:00    False    False
13 21:00 Browse Internet           0:30    False    False
```

# Get today

**Requirements:**

* Python 3
* Git

Open your terminal and run this:

`git clone https://github.com/TajwarHjkl/today`

Then you can `cd` into the *today* directory and run:

`python3 today/today.py -h`
