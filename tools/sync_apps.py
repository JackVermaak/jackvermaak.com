"""Copies the web apps that live in their own repositories into site/, unchanged, so the copies
cannot drift from their source.

  ograder           github.com/JackVermaak/ograder           -> site/ograder
  frictionforecast  github.com/JackVermaak/friction-forecast -> site/frictionforecast

The O-Grader's sitemap stays behind: its canonical address is jackingtothemax.com/ograder, where
the Worker that serves latest.json runs. Friction Forecast's canonical address is this site, so
gen.py lists its pages in sitemap.xml.

Run: python3 tools/sync_apps.py [app ...]   (default: all apps; repositories are expected next to
this one, e.g. ../ograder, or set the path with app=path, e.g. ograder=~/code/ograder)
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# app folder: (repository folder name, files to leave behind)
APPS = {
    'ograder': ('ograder', {'sitemap.xml'}),
    'frictionforecast': ('friction-forecast', set()),
}


def sync(app, repo):
    _, skip = APPS[app]
    src = os.path.join(os.path.expanduser(repo), 'public', app)
    dst = os.path.join(HERE, '..', 'site', app)
    if not os.path.isfile(os.path.join(src, 'index.html')):
        sys.exit(f'No {app} pages at {src}. Pass the repository path as {app}=PATH.')
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in skip])
    print(f'Copied {os.path.normpath(src)} -> {os.path.normpath(dst)}')


def main():
    args = sys.argv[1:] or list(APPS)
    for arg in args:
        app, _, repo = arg.partition('=')
        if app not in APPS:
            sys.exit(f'Unknown app {app!r}. Known: {", ".join(APPS)}')
        sync(app, repo or os.path.join(HERE, '..', '..', APPS[app][0]))


if __name__ == '__main__':
    main()
