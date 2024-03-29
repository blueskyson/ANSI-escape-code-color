# aecc

**A**NSI **e**scape **c**ode **c**olor

A tool for looking up terminal color codes. 

## Screenshots

Show background color labels:

![](background.png)

Show font color labels:

![](font.png)

Get ANSI escape codes by labels.

![](usage.png)

## Build

C++

```
$ cd cpp
$ make
$ ./aecc
```

Python

```
$ python python/aecc256.py
```

## Usage

```
Usage: [options] font background 

ANSI escape code color lookup (256 colors)

Positional arguments:
font                    Specicfy font color by a number (e.g. 3). B[number] represents bold font (e.g. B122). 256 is the default color. 
background              Specicfy background color by a number (e.g. 5). 256 is the default background color. 

Optional arguments:
-h --help               shows help message and exits
-v --version            prints version information and exits
-f --font               Display font numbers. 
-b --background         Display background numbers.
```

