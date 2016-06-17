# Alfred Workflow Packager

*Copyright 2016 Caleb Evans*  
*Released under the MIT license*

Alfred Workflow Packager is a command-line utility which makes the process of
packaging and exporting an Alfred workflow incredibly quick and easy. The
utility supports both Alfred 2 and Alfred 3.

This utility is in beta, so anything can break at any time. Consider yourself
warned!

## Setup

You can install the utility via `pip`, either globally or within a virtualenv:

```
pip install git+https://github.com/caleb531/alfred-workflow-packager.git
```

## Usage

### 1. Create configuration file

Once you've installed AWP, you must configure it for every project where you
wish to use it. To do so, create a `packager.json` file in the root directory of
your project; this file configures AWP for that particular project.

#### Example

```json
{
  "alfred_version": 3,
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

#### Required options

##### alfred_version

The version of Alfred this workflow supports (accepted values are `2` and `3`).

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
    - apple.json
    - banana.json
    - orange.json
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
    - apple.json
    - banana.json
    - orange.json
```

Note that files and folders already present in the installed workflow are *not*
touched if they are not in the *resources* list.

#### Optional options

##### readme

The path to the README file to use for this workflow; the *About this Workflow*
field in your workflow is populated with the contents of this file.

### 2. Validate configuration file

Once you've finished writing the `packager.json` file for your project, you
should validate it by running `awp --validate` from the root directory of your
project. If you are missing any options or if any of the option values are in
the wrong format, the utility will output those respective error messages.

### 3. Run utility

Now that your project has a valid `packager.json` file, you can run the utility
via the `awp` command:

```
awp
```

Running `awp` will always do a few things:

1. Copy those project resources listed in `packager.json` to the installed
workflow (in their respective locations)

2. Update the installed workflow's README with the contents of the README file
listed in `packager.json` (if one is listed)

#### Setting the workflow version

Passing the `--version` option to `awp` allows you to set the version of the
installed workflow directly. I highly recommend using [semantic
versioning](http://semver.org/) to version your workflow releases.

```
awp --version 1.2.0
```

#### Exporting the workflow

When you're pleased with your work and you're ready to publish a new release,
you can export the installed workflow to your project directory by passing the
`--export` flag to `awp`.

```
awp --export
```

Note that you can set the version and export the workflow simultaneously:

```
awp --version 1.2.0 --export
```
