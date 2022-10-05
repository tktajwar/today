# Todo List

Todo List in *today* is the list of tasks you want to do. Having a Todo List can make planning your day much easier.

All the flags in *Todo List* are in upper-case.

## Basic Todo List

### Adding A New Task

```
today -A [ID] [Name] [Duration]
```

`-A` adds a new task to the end of the todo list. If ID is provided then it will insert the task in that position. Name and Duration respectively tells *today* the name and the duration of the new task.

### Removing A Task

```
today -R [ID]
```

`-R` removes the last task from the todo list. If an ID is provided then *today* will remove the task with that ID.


### Copying A Task to The Todo List

```
today -C [ID] [ID]
```

`-C` copies a task from your day plan to your todo list. The first ID tells *today* which task you want to copy. If the second ID is provided then *today* will insert the copied task to that place in the todo list.

### Loading A Task From The Todo List

```
today -L [ID] [ID]
```

`-L` loads a task from your todo list to your day plan. The first ID tells *today* which task from the todo list you want to load. If the second ID is provided then *today* will insert the task to that place; otherwise, it will add it to the end of the day.

Note: This will delete the task from the Todo List.


### Copying All The Yesterday's Undone Tasks

```
today --CY
```

`--CY` copies all the undone tasks from yesterday.

Note: You need to use `--aa` to create yesterday's data.
