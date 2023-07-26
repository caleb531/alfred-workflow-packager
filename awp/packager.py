#!/usr/bin/env python3
# coding=utf-8

import distutils.dir_util as distutils
import contextlib
import filecmp
import glob
import plistlib
import os
import os.path
import shutil
import xml
from zipfile import ZipFile, ZIP_DEFLATED


# Create parent directories for the given path if they don't exist
def create_parent_dirs(path):
    parent_path = os.path.dirname(path)
    if parent_path:
        try:
            os.makedirs(parent_path)
        except OSError:
            pass


# Read a .plist file from the given path and return a dictionary representing
# the contents
def read_plist_from_path(plist_path):
    with open(plist_path, 'rb') as plist_file:
        try:
            return plistlib.load(plist_file)
        # For whatever reason, the plist-writing process can sometimes add some
        # extraneous junk to the end of the file which causes the XML to be
        # malformed and raises an error; to solve this, we catch that error and
        # properly parse out the valid XML
        except xml.parsers.expat.ExpatError:
            plist_contents = plist_file.read()
            junk_marker = b'</plist>'
            plist_contents = plist_contents[:plist_contents.index(junk_marker) + junk_marker]
            return plistlib.loads(plist_contents)


# Retrieve correct path to directory containing Alfred's user preferences
def get_user_prefs_dir():

    library_dir = os.path.join(os.path.expanduser('~'), 'Library')
    try:
        core_prefs = read_plist_from_path(os.path.join(
            library_dir, 'Preferences',
            'com.runningwithcrayons.Alfred-Preferences-3.plist'))
    except IOError:
        core_prefs = read_plist_from_path(os.path.join(
            library_dir, 'Preferences',
            'com.runningwithcrayons.Alfred-Preferences.plist'))

    # If user is syncing their preferences using a syncing service
    if 'syncfolder' in core_prefs:
        return os.path.expanduser(core_prefs['syncfolder'])
    else:
        return os.path.join(
            library_dir, 'Application Support', 'Alfred')


# Retrieve path to and info.plist object for installed workflow
def get_installed_workflow(workflow_bundle_id):

    # Retrieve list of the directories for all installed workflows
    workflow_dirs = glob.iglob(os.path.join(
        get_user_prefs_dir(), 'Alfred.alfredpreferences', 'workflows', '*'))

    # Find workflow whose bundle ID matches this workflow's
    for workflow_dir in workflow_dirs:
        info_path = os.path.join(workflow_dir, 'info.plist')
        info = read_plist_from_path(info_path)
        if info['bundleid'] == workflow_bundle_id:
            return workflow_dir, info

    # Assume workflow is not installed at this point
    raise OSError('Workflow is not installed locally')


# Retrieve the octal file permissions for the given file as a base-10 integer
def get_permissions(file_path):
    return os.stat(file_path).st_mode


# Return True if the permissions of the two files are equal; return False
# otherwise
def cmp_permissions(src_file_path, dest_file_path):
    return get_permissions(src_file_path) == get_permissions(dest_file_path)


# Return True if the item counts for the given directories match; otherwise,
# return False
def check_dir_item_count_match(dir_path, dest_dir_path, dirs_cmp):

    return (not dirs_cmp.left_only and not dirs_cmp.right_only and
            not dirs_cmp.funny_files)


# Return True if the contents of all files in the given directories match;
# otherwise, return False
def check_dir_file_content_match(dir_path, dest_dir_path, dirs_cmp):

    match, mismatch, errors = filecmp.cmpfiles(
        dir_path, dest_dir_path, dirs_cmp.common_files, shallow=False)
    return not mismatch and not errors


# Return True if the contents of all subdirectories (found recursively) match;
# otherwise, return False
def check_subdir_content_match(dir_path, dest_dir_path, dirs_cmp):

    for common_dir in dirs_cmp.common_dirs:
        new_dir_path = os.path.join(dir_path, common_dir)
        new_dest_dir_path = os.path.join(dest_dir_path, common_dir)
        if not dirs_are_equal(new_dir_path, new_dest_dir_path):
            return False
    return True


# Recursively check if two directories are exactly equal in terms of content
def dirs_are_equal(dir_path, dest_dir_path):

    dirs_cmp = filecmp.dircmp(dir_path, dest_dir_path)

    if not check_dir_item_count_match(dir_path, dest_dir_path, dirs_cmp):
        return False
    if not check_dir_file_content_match(dir_path, dest_dir_path, dirs_cmp):
        return False
    if not check_subdir_content_match(dir_path, dest_dir_path, dirs_cmp):
        return False

    return True


# Return True if the resource (file or directory) is equal to the destination
# resource; return False otherwise
def resources_are_equal(resource_path, dest_resource_path):

    try:
        return dirs_are_equal(resource_path, dest_resource_path)
    except OSError:
        # Compare files if they are not directories
        try:
            return (
                filecmp.cmp(resource_path, dest_resource_path)
                and
                cmp_permissions(resource_path, dest_resource_path)
            )
        except OSError:
            # Resources are not equal if either does not exist
            return False


# Copy package resource to corresponding destination path
def copy_resource(resource_path, dest_resource_path, force=False):

    if force or not resources_are_equal(resource_path, dest_resource_path):
        try:
            distutils.copy_tree(resource_path, dest_resource_path)
        except distutils.DistutilsFileError:
            with contextlib.suppress(FileNotFoundError):
                os.remove(dest_resource_path)
            shutil.copy(resource_path, dest_resource_path)
        print('Copied {file}'.format(file=resource_path))
        return True
    else:
        return False


# Copy all package resources to installed workflow
def copy_pkg_resources(workflow_path, workflow_resources, force=False):

    copied_any = False
    for resource_patt in workflow_resources:
        for resource_path in glob.iglob(resource_patt):
            create_parent_dirs(os.path.join(workflow_path, resource_path))
            dest_resource_path = os.path.join(workflow_path, resource_path)
            copied = copy_resource(
                resource_path,
                dest_resource_path,
                force=force)
            if copied:
                copied_any = True
    if not copied_any:
        print('Nothing to copy; workflow is already up-to-date')


# Update the workflow README with the current project README
def update_workflow_readme(info, readme_path):

    orig_readme = info['readme']
    with open(readme_path, 'r') as readme_file:
        new_readme = readme_file.read()
    if orig_readme != new_readme:
        info['readme'] = new_readme
        print('Updated workflow README')


# Set the workflow version to a new version number if one is given
def update_workflow_version(info, new_version_num):
    if new_version_num:
        info['version'] = new_version_num
        print('Set version to v{version}'.format(version=new_version_num))


# Write installed workflow subdirectory files to the given zip file
def zip_workflow_dir_files(workflow_path, zip_file,
                           root, relative_root, files):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        # Get path to current file relative to workflow directory
        relative_file_path = os.path.join(relative_root, file_name)
        zip_file.write(file_path, relative_file_path)


# Write installed workflow subdirectories to the given zip file
def zip_workflow_dirs(workflow_path, zip_file):
    # Traverse installed workflow directory
    for root, dirs, files in os.walk(workflow_path):
        # Get current subdirectory path relative to workflow directory
        relative_root = os.path.relpath(root, workflow_path)
        # Add subdirectory to archive and add files within
        zip_file.write(root, relative_root)
        zip_workflow_dir_files(
            workflow_path, zip_file, root, relative_root, files)


# Export installed workflow to project directory
def export_workflow(workflow_path, archive_path):

    # Create new Alfred workflow archive in project directory
    # Overwrite any existing archive
    create_parent_dirs(archive_path)
    with ZipFile(archive_path, 'w', compression=ZIP_DEFLATED) as zip_file:
        zip_workflow_dirs(workflow_path, zip_file)


# Package installed workflow by copying resources from project, updating
# README, and optionally exporting workflow
def package_workflow(config, version, export_files, force=False):

    workflow_path, info = get_installed_workflow(config['bundle_id'])

    copy_pkg_resources(workflow_path, config['resources'], force=force)
    if 'readme' in config:
        update_workflow_readme(info, config['readme'])
    update_workflow_version(info, version)
    plist_path = os.path.join(workflow_path, 'info.plist')
    with open(plist_path, 'rb+') as plist_file:
        plistlib.dump(info, plist_file)

    # Do not export anything if --export/-e option is not supplied
    if export_files is None:
        return

    # If --export/-e is supplied but without any arguments, default to the
    # export_files list defined in packager.json (this must match the 'const'
    # parameter in the argument definition for --export/-e)
    if export_files == []:
        export_files = config.get('export_files', [])

    for export_file in export_files:
        project_path = os.getcwd()
        export_workflow(workflow_path, os.path.join(
            project_path, export_file))
        print('Exported v{version} to {file}'.format(
            version=info['version'],
            file=export_file))
