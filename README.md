# today

**Add Tasks, reserve time for them, Mark Task Done and Be Organised!**

How is it different from a program such as [Taskwarrior](https://taskwarrior.org/)? **Taskwarrior** is a powerful to do list manager, whereas **today** is a day planner. You can use Taskwarrior to add tasks, make them recurring and add due dates; you can use today to plan what tasks you will be doing today, when you will do them and how much time you are planning to spend on them.

**today** is in a state where it's useable but it's stipp a work in progress. All the feature requests, bug reports and changes made by the users are welcome.

# Getting Started

`$ python today.py -h`

```
positional arguments:
  ID               Task ID number
  Name             Task Name
  Duration         Task Duration (Minutes)

options:
  -h, --help       show this help message and exit
  -a, --add        add a new Task
  -d, --done       mark a task as done
  -u, --undo       mark a task as undone
  -r, --remove     remove Task
  -t, --toggle     toggle Skip of Task
  -da, --done-all  mark all tasks as done
  -ua, --undo-all  mark all tasks as undone
  -p, --purge      purge Task Data
  -v, --retrieve   retrieve from Purged Task Data
  -n, --new-day    store current Task Data as Yesterday and start a New Day
  -y, --yesterday  Show Yesterday's Data
```


`$ python today.py -a 0 Shower 20`

`$ python today.py -a 1 Breakfast 10`

`$ python today.py -a 2 Write 60`

`$ python today.py -a 3 Gym 60`

`$ python today.py -a Shower 20`

`$ python today.py -a Write 120`

`$ python today.py`

```
ID Time Name      Duration Skip     Done
0  7:0  Shower    0:20     False    False
1  7:20 Breakfast 0:10     False    False
2  7:30 Write     1:0      False    False
3  8:30 Gym       1:0      False    False
4  9:30 Shower    0:20     False    False
5  9:50 Write     2:0      False    False
```
`$ python today.py -d 0`

`Task 0: Shower done.`

```
ID Time Name      Duration Skip     Done
0  7:0  Shower    0:20     False    True
1  7:20 Breakfast 0:10     False    False
2  7:30 Write     1:0      False    False
3  8:30 Gym       1:0      False    False
4  9:30 Shower    0:20     False    False
5  9:50 Write     2:0      False    False
```

The actual program supports terminal colours and next task is highlighted.

# Get today

The only way to get **today** right now is by Git.

## CLI

Copy the link to this page and open terminal

`git clone link`

replace the *link* with the link you copied.

## GUI

You can click on the "Download" option and then unzip the file.
