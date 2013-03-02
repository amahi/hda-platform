hda-platform
============

This is the packaging "shell" repo for the Amahi platform.

The code for platform is a git submodule in a different repo at https://github.com/amahi/platform,
and it's hosted in this repo under html/

To get the latest submodule code,

```bash
git submodule init
git submodule update
cd html && git pull && git checkout master
```
