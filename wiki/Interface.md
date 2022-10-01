# Interface

## Why CLI

It's fast, intuitive and easily scriptable. Some things are better done with a Graphical User Interface. But, most programs are much efficient with a command line interface. A day planner is one of those programs.

## Positional Arguments

```
today [ID] [Name] [Duration]
```

**Positional Arguments** are the arguments passed by the user in a proper order. These can be a file name, a date, a number, anything specified by the program. Today takes three positional arguments and they are:

* **ID**: Integer (whole number) that tells today which task the user wants to select
* **Name**: String of Characters that tells today what name to give a new task or change to of an old one
* **Duration**: Time that tells today the duration of a task; it can be writted as 180, 3h and 3:00

For example:

```
today 12 shower 20m
```

Although the positional arguments are required be in their proper order, today does not mind if one, two or all of the positional arguments are missing. So you can have `today ID` without Name and Duration, or `today ID Duration`, or `today Name`. Today will use Default name and duration when they are missing (you can change them in the settings). For missing ID, today will use next or last Task based on the option.

## Flags

A flag is an argument that starts with `-`. For example: `-a`, `--arg`. Some flags act as boolean. If they are passed, the program should act differently than when they are not. For example, `-I` in today increments ID by 1 after every iteration (bit advanced). Some flags also take arguments. For example, `--xs [filename]` takes the user argument `filename` to save as. There are two kinds of flags:

### Long Flags

Flag names that start with double hypens (`--`) are called long flags. If the name of the flag is `flag` and it takes an Integer argument then it can be written as `--flag 5` (the user passed 5 as the argument).

### Short Flags

Flag names that start with single hypen (`-` are called short flags. They are one character long and they often act like switches. If a single flag is called `f` and it takes an Integer argument then it can be written as both `-f5` and `-f 5`. Multiple single flags can also be written together; for example, short flags `-a`, `-b`, `-c`, `-d` can all be written as `-abcd`.
