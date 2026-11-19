"""Copies the O-Grader pages from a checkout of github.com/JackVermaak/ograder into site/ograder.

The files are copied unchanged, so the two copies cannot drift. The sitemap stays behind: the
pages' canonical address is jackingtothemax.com/ograder, where the Worker that serves
latest.json runs, and the pages ask that Worker for new ascents from here too.

Run: python3 tools/sync_ograder.py [path to the ograder repository, default ../ograder]
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {'sitemap.xml'}


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', 'ograder')
    src = os.path.join(repo, 'public', 'ograder')
    dst = os.path.join(HERE, '..', 'site', 'ograder')
    if not os.path.isfile(os.path.join(src, 'app.js')):
        sys.exit(f'No O-Grader pages at {src}. Pass the path to the ograder repository.')
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP])
    print(f'Copied {src} -> {os.path.normpath(dst)}')


if __name__ == '__main__':
    main()
