# Task and Data

## Basic Task and Data

### The Concept of Next

**Next** is a simple yet important concept in *today*. It means the next undone task.

When all your tasks are displayed, the next task will be highlighted and most actions in *today* will use the next task as the default task.

### Add A New Task

```
today -a [ID] [Name] [Duration]
```

`-a` adds a new task to end of the day. If an ID is provided then *today* will add the new task to that place.

`[Name]` and `[Duration]` tell *today* the Name and Duration of the new task respectively. In their absence *today* will use Default Name and Duration, which can be changed in the settings.


Examples:

```
today -a shower 20m
```

```
today -a watch a film 2:40
```

### Mark Done

```
today -d [ID]
```

`-d` marks the *next* task as done. In case an ID is passed, *today* will mark that task as done.

### Mark Undone

```
today -D [ID]
```

`-D` marks the last done task as undone. In case an ID is passed, *today* will mark that task as undone.

### Remove A Task

```
today -r [ID]
```

`-r` removes a task. If no ID is passed then the last task will be removed.

(This action is not undoable)

### Skip A Task

```
today -s [ID]
```

`-s` skips the next task. If an ID is passed then *today* will skip that task. A skipped task won't be highlighted as *next*.

### Unskip A Task

```
today -S [ID]
```

`-S` unskips the last skipped task. If an ID is passed then *today* will unskip that task.

### Modify A Task

```
today -m [ID] [New ID] [New name] [New Duration]
```

`-m` modifies ID, Name and Duration of a task with the new ID, Name and Duration. The ID tells today which task to modify.


### Display Tasks

```
today
```

or

```
today -y
```

*today* will display your day if no arguments are passed or if you pass the argument `-y`.

`-y` can be used with other single flags, for example: `today -dy`, `today -sy`, and `today -m2 1 -y`.

### Task Start Time

```
today -a [ID] [Name] [Duration] -t [time]
```

```
today -m [ID] [New ID] [New Name] [New Duration] -t [time]
```

Although this is not how *today* is meant to be used, in special cases you can use `-t` to tell *today* the time a task starts.

To remove the start time from a task:

```
today -m [ID] -t -1
```

## Advanced Data

### Purge Task Data

```
today -p
```

`-p` purges the task data. A `purged.json` file will be created in your `.today` directory where your purged task data will be saved.

### Retrieve Purged Task Data

```
today -P
```

`-P` retrieves purged task data. Your current data will be lost.

If you are looking for a way to save task data, then look at [Data File Management](Data File Management).

### Start A New Day

```
today --aa
```

`--aa` saves current data as yesterday's and starts a new day. This can be useful because you can [copy all yesterday's undone task to your todo list](copy all yesterday's undone task to your todo list).

### Display Yesterday

```
today --yy
```

`--yy` displays yesterday's task data.
