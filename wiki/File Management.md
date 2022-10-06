# File Management

A day plan in *today* can be saved in a file and reused later. This can be useful if you want to have a day plan for every Saturday or a day plan for a special occation.

## Saving A Day Plan

```
today --xs [filename]
```

`--xs` saves the current day plan in a new file (or overwrites an old one). The filename tells *today* the filename of the file. If another file with the same name exists, *today* will overwrite the old one.

## Loading A Saved Day Plan

```
today --xl [filename]
```

`--xl` loads a saved day plan. The filename tells *today* the filename of the saved day plan.

## Deleting A Saved Day Plan

```
today --xx [filename]
```

`--xx` deletes a saved day plan. The filename tells *today* the filename of the saved day plan.

## Listing All The Saved Day Plans

```
today --ls
```

`--ls` lists all the saved day plan.
