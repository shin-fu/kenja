from __future__ import absolute_import
import re
from git import Repo


class GitDiffParser:
    # header_regex = re.compile(r'^diff --git (a/)+(.*) (b/)+(.*)$')

    header_a_blob_regex = re.compile(r'^--- (a/)?(.*)$')
    header_b_blob_regex = re.compile(r'^\+\+\+ (b/)?(.*)$')

    head_lineno_regex = re.compile(r'^@@ \-(\d+),?\d* \+(\d+),?\d* @@')

    def parse(self, diff_str):
        lines = diff_str.splitlines()

        a_blob_index = 0
        b_blob_index = 0
        deleted_lines = []
        added_lines = []
        while(lines):
            line = lines.pop(0)
            # if line[0] == 'd' and line[1] == 'i':
            #    print line
            if line[0] == '-':
                match = self.header_a_blob_regex.match(line)
            elif line[0] == '+':
                match = self.header_b_blob_regex.match(line)
            if line[0] == '@':
                match = self.head_lineno_regex.match(line)

                a_blob_index = int(match.group(1))
                b_blob_index = int(match.group(2))

                break

        while(lines):
            line = lines.pop(0)
            if line[0] == '+':
                added_lines.append((b_blob_index, line[1:]))
                b_blob_index += 1
            elif line[0] == '-':
                deleted_lines.append((a_blob_index, line[1:]))
                a_blob_index += 1
            elif line[0] == '@':
                match = self.head_lineno_regex.match(line)
                a_blob_index = int(match.group(1))
                b_blob_index = int(match.group(2))

        return (deleted_lines, added_lines)


def check_same_repository(a_repo_path, b_repo_path):
    a_repo = Repo(a_repo_path)
    b_repo = Repo(b_repo_path)
    print(check_branches(a_repo, b_repo))

def check_branches(a_repo, b_repo):
    a_branches = set([branch.name for branch in a_repo.branches])
    b_branches = set([branch.name for branch in b_repo.branches])
    return a_branches == b_branches


if __name__ == '__main__':
    import sys
    if(len(sys.argv) != 3):
        print("{0} {1} {2}".format(sys.argv[0], "a_repo", "b_repo"))
    check_same_repository(sys.argv[1], sys.argv[2])
