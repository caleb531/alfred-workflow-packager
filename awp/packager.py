#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
import distutils.dir_util as distutils
import filecmp
import hashlib
import glob
import plistlib
import os
import os.path
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

import biplist


# Create parent directories for the given path if they don't exist
def create_parent_dirs(path):
    parent_path = os.path.dirname(path)
    if parent_path:
        try:
            os.makedirs(parent_path)
        except OSError:
            pass


# Retrieve correct path to directory containing Alfred's user preferences
def get_user_prefs_dir():

    library_dir = os.path.join(os.path.expanduser('~'), 'Library')
    try:
        core_prefs = biplist.readPlist(os.path.join(
            library_dir, 'Preferences',
            'com.runningwithcrayons.Alfred-Preferences-3.plist'))
    except IOError:
        core_prefs = biplist.readPlist(os.path.join(
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
        if hasattr(plistlib, 'load'):
            with open(info_path, 'rb') as info_file:
                info = plistlib.load(info_file)
        else:
            info = plistlib.readPlist(info_path)
        if info['bundleid'] == workflow_bundle_id:
            return workflow_dir, info

    # Assume workflow is not installed at this point
    raise OSError('Workflow is not installed locally')


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


# Check if resource (file or directory) is equal to destination resource
def resources_are_equal(resource_path, dest_resource_path):

    try:
        return dirs_are_equal(resource_path, dest_resource_path)
    except OSError:
        # Compare files if they are not directories
        try:
            return filecmp.cmp(resource_path, dest_resource_path)
        except OSError:
            # Resources are not equal if either does not exist
            return False


# Copy package resource to corresponding destination path
def copy_resource(resource_path, dest_resource_path):

    if not resources_are_equal(resource_path, dest_resource_path):
        try:
            distutils.copy_tree(resource_path, dest_resource_path)
        except distutils.DistutilsFileError:
            shutil.copy(resource_path, dest_resource_path)
        print('Copied {}'.format(resource_path))


# Copy all package resources to installed workflow
def copy_pkg_resources(workflow_path, workflow_resources):

    for resource_patt in workflow_resources:
        for resource_path in glob.iglob(resource_patt):
            create_parent_dirs(os.path.join(workflow_path, resource_path))
            dest_resource_path = os.path.join(workflow_path, resource_path)
            copy_resource(resource_path, dest_resource_path)


# Update the workflow README with the current project README
def update_workflow_readme(info, readme_path):

    orig_readme_hash = hashlib.sha1(info['readme']).hexdigest()
    with open(readme_path, 'r') as readme_file:
        info['readme'] = readme_file.read()
    if orig_readme_hash != hashlib.sha1(info['readme']).hexdigest():
        print('Updated workflow README')


# Set the workflow version to a new version number if one is given
def update_workflow_version(info, new_version_num):
    if new_version_num:
        info['version'] = new_version_num
        print('Set version to v{}'.format(new_version_num))


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
def package_workflow(config, version, export_file):

    workflow_path, info = get_installed_workflow(config['bundle_id'])

    copy_pkg_resources(workflow_path, config['resources'])
    if 'readme' in config:
        update_workflow_readme(info, config['readme'])
    update_workflow_version(info, version)
    plist_path = os.path.join(workflow_path, 'info.plist')
    if hasattr(plistlib, 'dump'):
        with open(plist_path, 'rb+') as plist_file:
            plistlib.dump(info, plist_file)
    else:
        plistlib.writePlist(info, plist_path)

    if export_file == '':
        export_file = config['export_file']

    if export_file:
        project_path = os.getcwd()
        export_workflow(workflow_path, os.path.join(
            project_path, export_file))
        print('Exported installed workflow successfully (v{})'.format(
            info['version']))
