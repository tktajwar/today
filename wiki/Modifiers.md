# Modifiers

## Do Action For Every Tasks

The `-E` modifiers modifies the way some functions work by working on all the tasks on your day plan.

For example, `today -r -E` or `today -Er` will remove all the tasks from your day plan.

Note: only some functions take "every" argument and `-E` has no effect on the functions that don't.

## Iteration

Iteration allows you to make *today* do same action multiple times. There are two different flags for iteration in *today*: `-i` and `-I`. The first one iterates with a constant ID and the second one iterates with incrementing ID.

### Iteration With Constant ID

```
today [...] -i [int]
```

`-i` makes *today* run the same command multiple times with a constant ID. int tells *today* the number of times the command to run.

If you want to delete three tasks from the task with the ID 4, you can run:

```
today -r 4 -i 3
```

If you want to add the same task three times:

```
today -a Hello World 30m -i 3
```

### Iteration With Incrementing ID

```
today [...] -I [int]
```

`-I` makes *today* run the same command multiple times with incrementing ID (the ID will be incremented by 1 every iteration). int tells *today* the number of times the command to run. 

If you want to mark three tasks done from the task with the ID 4, you can run:

```
today -d 4 -I 3
```

If you want to make 2nd and 3rd tasks' duration 30 minutes:

```
today -m 1 30m -I 2
```

