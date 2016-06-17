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

### Configuring AWP

Once you've installed AWP, you must create a `packager.json` file in the root of
your project; this file configures AWP for your specific project.

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
