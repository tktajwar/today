# today

**A terminal program to help you plan your day and execute it in an organised way**

![screenshot_1](screenshots/screenshot_1.png)

![screenshot_2](screenshots/screenshot_2.png)

# Getting Started

**today** is a day planner program written in *Python 3*. The intention of developing this program was to help people plan the tasks they are going take with the amount of time they are planning to spend on them. This Command Line program will help have a realistic idea of what you can do today and stay focused on your day plan throughout the day.

*today* has quite a few features so this short introduction will give you an idea of what this program is about and how to start using it.

To see how to install *today*, click [here](#Install today).

## learning what we can do from the help message

To see what we can do with this program, run the command below:

`today -h`

You should see a longer version of this help message:

```
positional arguments:
  Arguments            Task ID [int], Name [str], Duration [int]

options:
  -h, --help           show this help message and exit
  -a, --add            add/append a new Task [Name][Duration]
  -d, --done           mark a task as done [ID]
  -u, --undo           mark a task as undone [ID]
  -r, --remove         remove Task [ID]
  -t, --toggle         toggle Skip of Task [ID]
  -c, --settings       configure settings data
```

This is the shortened version of the help message for *today*. We will only be looking at what we need to know to get started using the program.

Let's say we woke up in the morning and the first task of our day will be to exercise for 40 minutes. But how do we add a new task? Well if you look under the options, you will see one that starts with `-a` with the message "add/append a new Task [Name] [Duration]".  Let's use that.

## adding a new task

`today -a Exercise 40m`

We are calling the program *today* and we are giving it the optional argument `-a` followed by two positonal arguments "Exercise" and "40m".

Now let's check what we added:

`today`



# Install today

**Requirements:**

* Python 3
* Pip
* Git

Open terminal and run:

`git clone https://github.com/TajwarHjkl/today`

`cd today`

`pip install .`

`today -h`
