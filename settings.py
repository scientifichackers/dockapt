from pathlib import Path

LOADING = '…'
DOCKAPT_DIR = Path.home().joinpath('.dockapt')
REPO_DIR = DOCKAPT_DIR.joinpath('repositories')

DOCKER_IMAGE_NAMESPACE = 'docapt__'

FUZZY_RATIO_CUTOFF = 75
