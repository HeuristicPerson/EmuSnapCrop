#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

import files

# Constants
#=======================================================================================================================
u_IMG_VIEWER = u'xviewer'


# Generic Class for executing consoles commands
#=======================================================================================================================
class Command:
    """
    Simple class to store and execute a command line command.
    """
    def __init__(self, pu_cmd):
        self.u_cmd = pu_cmd
        self.b_executed = False
        self.u_stdout = None
        self.u_stderr = None

    def __str__(self):
        u_output = u'<Command>\n'
        u_output += u'  .u_convert_cmd:      %s\n' % self.u_cmd
        u_output += u'  .b_executed: %s\n' % self.b_executed

        if not self.u_stdout:
            u_output += u'  .u_stdout:   %s\n' % self.u_stdout
        else:
            i_line = 0
            for u_line in self.u_stdout.splitlines():
                i_line += 1
                if i_line == 1:
                    u_output += u'  .u_stdout:   %s\n' % u_line
                else:
                    u_output += u'               %s\n' % u_line

        if not self.u_stderr:
            u_output += u'  .u_stderr:   %s\n' % self.u_stderr
        else:
            i_line = 0
            for u_line in self.u_stderr.splitlines():
                i_line += 1
                if i_line == 1:
                    u_output += u'  .u_stderr:   %s\n' % u_line
                else:
                    u_output += u'               %s\n' % u_line

        return u_output.encode('utf8')

    def execute(self):
        """
        Method to execute the command.
        :return:
        """
        if not self.b_executed:
            self.b_executed = True
            o_process = subprocess.Popen(self.u_cmd.encode('utf8'),
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         shell=True)

            u_stdout, u_stderr = o_process.communicate()

            self.u_stdout = u_stdout.decode('utf8')
            self.u_stderr = u_stderr.decode('utf8')


# General use commands
#=======================================================================================================================
def file_cp(pu_src_file, pu_dst_file):
    u_cmd = u'cp "%s" "%s"' % (pu_src_file, pu_dst_file)
    o_command = Command(u_cmd)
    o_command.execute()


def file_del(pu_file):
    u_cmd = u'rm "%s"' % pu_file
    o_command = Command(u_cmd)
    o_command.execute()


def display_img(pu_img):
    """
    Function to view an image.
    :param pu_img:
    :return:
    """
    u_cmd = u'%s "%s"' % (u_IMG_VIEWER, pu_img)
    o_command = Command(u_cmd)
    o_command.execute()


def git_get_file_commits(pu_git_root=None, pu_file=None):
    """
    Function to get the list of commits where a file was changed.

    :param pu_file: File path.

    :return: A tuple of commits like (u'8be4b57', u'9744c27', ...)
    """
    # 1st we save the current working directory and we change it to the root of the git repository because there is
    # a severe issue or difficulty working with git from another directory. So, I take the easy (and dirty) workaround.
    u_prev_dir = os.getcwd()
    os.chdir(pu_git_root)

    # TODO: Since I change the cwd, I shouldn't need --git.dir anymore

    # 1st, we obtain the changes history of the file. The output is like:
    u_cmd = u'git --git-dir="%s.git" log --oneline "%s"' % (pu_git_root, pu_file)
    o_command = Command(u_cmd)
    o_command.execute()

    if o_command.u_stderr:
        print o_command.u_stderr

    # The output of the command to parse is something like:
    #
    #     8be4b57 5 megadrive + 1 nes coming from TheCoverProject
    #     9744c27 Initial commit
    #
    # Where the 1st part is the [beginning] os commit's SHA1 and the second part, the title of the commit.
    lu_commits = []
    for u_line in o_command.u_stdout.splitlines():
        u_sha1 = u_line.split()[0]
        lu_commits.append(u_sha1)

    lu_commits.reverse()

    # We add an empty commit to represent the current status of the files (probably uncommmited)
    lu_commits.append(u'')

    # Finally, we leave the working directory as it was before
    os.chdir(u_prev_dir)

    # Todo, return more data, maybe a dict containing the one-line description of the commits.

    return tuple(lu_commits)


def git_save_file_from_commit(pu_git_root=None, pu_src_file=None, pu_commit=None, pu_dst_file=None):
    """
    Function to "extract" one file from a commit and save it to disk.
    :param pu_src_file:
    :param pu_commit:
    :param pu_dst_file:
    :return:
    """

    # 1st we save the current working directory and we change it to the root of the git repository because there is
    # a severe issue or difficulty working with git from another directory. So, I take the easy (and dirty) workaround,
    # changing the working directory to the git repository root and changing the file path to make it relative to that
    # root.
    u_prev_dir = os.getcwd()
    os.chdir(pu_git_root)

    o_src_img_rel_fp = files.FilePath(pu_src_file)
    o_src_img_rel_fp = o_src_img_rel_fp.root_replace(pu_git_root, u'')

    if pu_commit:
        # 2nd, we copy the images to /tmp folder with
        u_cmd = u'git show %s:"%s" > "%s"' % (pu_commit, o_src_img_rel_fp.u_path, pu_dst_file)
        o_command = Command(u_cmd)
        o_command.execute()

        if o_command.u_stderr:
            print o_command.u_stderr

    else:
        # If the commit is empty, we simply copy the current status of the file
        u_cmd = u'cp "%s" "%s"' % (pu_src_file, pu_dst_file)
        o_command = Command(u_cmd)
        o_command.execute()

        if o_command.u_stderr:
            print o_command.u_stderr

    # Finally, we leave the working directory as it was before
    os.chdir(u_prev_dir)