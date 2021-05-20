# Jazz XML Parameter File Generator
This Python utility allows a user to quickly generate an XML config file to view MDV data in Jazz.
More information about Jazz: https://ral.ucar.edu/projects/jazz/

## Dependencies/Requirements
ConfigMaster: https://github.com/NCAR/ConfigMaster

Python3

## Getting started
You'll probably want to have your own config file for this tool locally. You can easily generate one and direct the output to a file:
```
jazzparamgen.py --print_params > my_jazzparamgen_conf.py
``` 
This file will have every available config option for this tool, along with a brief description of what each item does.

## Operating Modes
The following operating modes are available, listed in order of precedence. If you have multiple modes configured, this precedence will be used.
1. `inurl` mode --> a single file is processed
2. `rap_data_dir` mode --> traverse a single directory for all MDV files at all subdirectories
3. `inlist` --> process an explicit list of files provided by the user

Set the operating mode by setting the corresponding config item in the config file.

## Colorscale files
Please configure the `colorurl` config option to point to a local directory or an HTTP location where Jazz/CIDD color files exist. Note that you'll need to develop your own mapping of field names and color files to use for that field name. You can find the default behavior in `jazzparamgencolors.py`. Simply add further `elif` statements to this file locally, or create a new one with a Python function named `set_cmap()` following the outline in `jazzparamgencolors.py`.

## Excluding or including specific patterns
This tool supports two config options to help filter datatypes processed- `exclude` and `must_include`. You can leave both of these empty, or set one or the other but not both. Note this is only used in `rap_data_dir` mode. Both `exclude` and `must_include` are lists of strings. Set either of these to any expected string(s) in paths that will be processed to include or exclude them.

## A note about URL's
The following are acceptable forms of MDV URL's supported by this tool:

**A file URL using fully-qualified MDV URL syntax:**
```
mdvp:://hostname.rap.ucar.edu::/full/path/to/file/YYYYMMDD/HHMMSS.mdv
```

**A relative URL using fully-qualified MDV URL syntax (relative means all subdirectories prior to the YYYYMMDD subdirectory in the path):**
```
mdvp:://hostname.rap.ucar.edu::/relative/path/to/data
```

**A file URL using normal Linux path syntax (assumes localhost):**
```
/full/path/to/file/YYYYMMDD/g_HHHHHHH/HHMMSS.mdv
```

**A relative URL using normal Linux path syntax (relative means all subdirectories prior to the YYYYMMDD subdirectory in the path, assumes localhost):**
```
/relative/path/to/data
```

## Example 1
Generate a quick config file based upon a single MDV file

### Command
```
jazzparamgen.py --inurl mdvp:://hostname.rap.ucar.edu::/path/to/my/file.mdv --outfile quickconfig.xml
```

### Notes
This will obtain the field names from the exact file provided on the command line and generate an XML config file named **quickconfig.xml**

## Example 2
Specify a list of absolute or relative URL's to generate a config file

### Config Options
```
inlist = ['/path/to/dataset1','/path/to/another/mdv/YYYYMMDD/HHMMSS.mdv','mdvp:://remotehost.rap.ucar.edu::/this/is/a/path/on/another/machine/YYYYMMDD/HHMMSS.mdv']
```

### Command
```
jazzparamgen.py -c my_jazzparamgen_conf.py --outfile multipleurls.xml
```

### Notes
This will obtain the field names from the **latest** file at each URL provided in the `inlist` config option and generate an XML config file named **multipleurls.xml**

## Example 3
Provide a single directory (aka RAP_DATA_DIR) and traverse it and all subdirectories searching for MDV files

### Config Options
```
rap_data_dir = /path/to/my/data
rap_data_dir_host = hostname (can be localhost or remotehost)
remote = True/False (True for remotehost, False for localhost)
remuser = username (Only if remote = True, provide username with SSH keys set up on remotehost)
```

### Command
```
jazzparamgen.py -c my_jazzparamgen_conf.py --outfile rap_data_dir.xml
```

### Notes
This will obtain the field names from the **latest** file at each path in `rap_data_dir` where there was an MDV file found by the tool and generate an XML config file named **rap\_data\_dir.xml**
