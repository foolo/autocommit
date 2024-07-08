#!/usr/bin/env python3
from dataclasses import dataclass
import subprocess


@dataclass
class GitStatus:
    status: str
    info: str


def main():
    cmd = ['git', 'status', '--porcelain']
    output = subprocess.check_output(cmd).decode()
    lines = sorted(output.splitlines())
    index_changes: list[GitStatus] = []
    worktree_changes: list[GitStatus] = []
    for line in lines:
        status_index = line[0]
        status_wtree = line[1]
        info = line[3:]
        if status_index != ' ':
            index_changes.append(GitStatus(status_index, info))
        if status_wtree != ' ':
            worktree_changes.append(GitStatus(status_wtree, info))

    if len(worktree_changes) > 0:
        print(f'unstaged changes:')
        for change in worktree_changes:
            print(f'  {change}')
        user_input = input('Continue with commit? (y/n): ')
        if user_input.lower() != 'y':
            return
    if len(index_changes) == 0:
        print('nothing to commit')
        return
    message = ', '.join([(s.status + ' ' + s.info) for s in index_changes])
    print(f'committing: {message}')
    subprocess.run(['git', 'commit', '--message', message], check=True)


if __name__ == '__main__':
    main()
