# Alfred Workflow Packager

*Copyright 2016-2021 Caleb Evans*  
*Released under the MIT license*

Alfred Workflow Packager is a command-line utility which makes the process of
packaging and exporting an [Alfred](https://www.alfredapp.com/) workflow
incredibly quick and easy. The utility supports Alfred 3 and up, on projects running Python 2 *or* Python 3.

## Setup

You can install the utility via `pip`, either globally or within a virtualenv:

```
pip install alfred-workflow-packager
```

## Usage

### 1. Create configuration file

Once you've installed AWP, you must configure it for every project where you
wish to use it. To do so, create a `packager.json` file in the root directory of
your project; this file configures AWP for that particular project.

#### Example

```json
{
  "export_file": "Fruit.alfredworkflow",
  "bundle_id": "com.yourname.fruit",
  "readme": "README.txt",
  "resources": [
      "icon.png",
      "dostuff/*.py",
      "dostuff/data/*.json"
  ]
}
```

#### Required settings

##### export_file

The path of the exported workflow (relative to your project directory).

##### bundle_id

The unique bundle ID of your workflow. You must have one set in the installed
workflow, or AWP will not be able to find your workflow when packaging.

##### resources

A list of zero or more files/folder patterns representing files or folders to
copy from your project to the installed workflow. The directory structures and
filenames are preserved when copying.

*Local project:*

```
- icon.png
- fruit
    - apple.py
    - banana.applescript
    - orange.php
```

*Installed workflow (before running utility):*

```
- info.plist
- special_file.json
```

*packager.json resources:*

```json
[
    "icon.png",
    "fruit/*.json"
]
```

*Installed workflow (after running utility):*

```
- info.plist
- icon.png
- special_file.json
- fruit
    - apple.py
    - banana.applescript
    - orange.php
```

Note that files and folders already present in the installed workflow are *not*
touched if they are not in the *resources* list.

#### Optional settings

##### readme

The path to the README file to use for this workflow; the *About this Workflow*
field in your workflow is populated with the contents of this file.

### 2. Validate configuration file

Once you've finished writing the `packager.json` file for your project, you
should validate it by running `awp --validate` from the root directory of your
project. If you are missing any settings or if any of the setting values are in
the wrong format, the utility will output those respective error messages.

### 3. Run utility

Now that your project has a valid `packager.json` file, you can run the utility
via the `awp` command:

```
awp
```

Running `awp` will always copy those project resources listed in
`packager.json` to the installed workflow (in their respective locations). By
default, only changes files/directories are copied, but you can force the
copying of all files/directories by passing `--force` / `-f`.

```
awp --force
```

```
awp -f
```

If a file's permissions have changed but the contents remain the same, you must
use `--force` / `-f`. Automatic permission-checking is being considered for a
future Alfred Workflow Packager release, though!

#### Setting the workflow version

Passing the `--version` option (also `-v`) to `awp` allows you to set the
version of the installed workflow directly. I highly recommend using [semantic
versioning](http://semver.org/) to version your workflow releases.

```
awp --version 1.2.0
```

```
awp -v 1.2.0
```

#### Exporting the workflow

When you're pleased with your work and you're ready to publish a new release,
you can export the installed workflow to your project directory by passing the
`--export` flag (or `-e`) to `awp`.

```
awp --export
```

```
awp -e
```

Note that you can set the version and export the workflow simultaneously:

```
awp -v 1.2.0 -e
```

**New in AWP v1.1.0:** If you wish to temporarily export the workflow to a
different file (different from `export_file` in `packager.json`), you can
pass an optional path to `--export`:

```
awp -v 1.3.0-beta.1 -e ~/Desktop/fruit-beta.alfredworkflow
```

### 4. Configure workflow objects

The last important step is to update any script objects in your workflow (*i.e.*
objects of type **Script Filter**, **Run Script**, *etc.*) to reference the
files copied to the installed workflow directory.

You should set the *Language* to `/bin/bash` and use the appropriate shell
command to call your script. Use `"$@"` if your input is passed as argv, or
`"{query}"` if your input is passed as {query}.

#### Python

```
/usr/bin/python -m fruit.apple "$@"
```

```
/usr/bin/python -m fruit.apple "{query}"
```

#### AppleScript

```
/usr/bin/osascript fruit/banana.applescript "$@"
```

```
/usr/bin/osascript fruit/banana.applescript "{query}"
```

#### PHP

```
/usr/bin/php fruit/orange.php "$@"
```

```
/usr/bin/php fruit/orange.php "{query}"
```
