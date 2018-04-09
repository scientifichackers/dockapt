from pathlib import Path

DOCKAPT_DIR = Path.home().joinpath('.dockapt')
REPO_DIR = DOCKAPT_DIR.joinpath('repositories')

IMAGE_TAG = {
    'namespace': 'docapt__',
    'separator': '.',
    'tag_separator': ':'
}

FUZZY_RATIO_CUTOFF = 75

LOADING = '…'

LABELS = {
    'registry': 'registry_image',
    'run': 'docker_run_flags'
}

SPINNER = 'moon'
