hda-platform
============

This is the packaging "shell" repo for the Amahi platform.

The code for platform is a git submodule in a different repo at https://github.com/amahi/platform,
and it's hosted in this repo under html/

To get the latest submodule code,

```bash
git submodule init
git submodule update
cd html && git pull origin master && git checkout master
```

To develop and build on an rpm-based system, you may need to get the proper tools and dependencies in place. You can use this make target:

```bash
make rpm-devel-deps
```
To build the rpm, make sure you are using the system ruby in a system identical to the 
```bash
make disclean rpm
```
