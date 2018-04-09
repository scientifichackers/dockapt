import shlex
import subprocess

import click
import crayons
import docker
import git
from dockerfile_parse import DockerfileParser
from fuzzywuzzy import fuzz
from halo import Halo

import settings

docker_client = docker.from_env()


def find_pkg_dirs(query=None, exact=True, repo_dir=None):
    """
    Yields all package directories that satisfy a filter, if provided.

    Args:
        query: Filter the packages by name, useful for searching packages
        exact: Whether to filter packages by an exact match
        repo_dir: Directory of repo to look for packages

    Returns:
        Generator whose each element contains a Path object,
         referring to some package's directory (containing its Dockerfile)
    """

    if repo_dir:
        dockerfiles = repo_dir.rglob('Dockerfile')
    else:
        dockerfiles = settings.REPO_DIR.rglob('Dockerfile')

    for potential_pkg in dockerfiles:
        dfp = DockerfileParser(path=str(potential_pkg))

        pkg_dir = potential_pkg.parent

        if ((not query) or
                (
                        query and
                        (
                                (exact and query == pkg_dir.name) or
                                (not exact and are_similar(query, pkg_dir.name))
                        )
                )):
            yield pkg_dir


def get_repo_name(package_dir):
    """Extract the repo name, given a package dir"""
    return package_dir.parts[package_dir.parts.index(settings.REPO_DIR.name) + 1]


def are_similar(str1, str2, fuzzy_ratio_cutoff=settings.FUZZY_RATIO_CUTOFF):
    return fuzz.partial_ratio(str1, str2) >= fuzzy_ratio_cutoff


@click.group()
def cli():
    pass


@click.command()
@click.argument('package')
def search(package):
    found_none = True

    print(
        f'Finding packages with exact match {settings.LOADING}'
    )

    for repo_dir in settings.REPO_DIR.iterdir():
        with Halo(spinner=settings.SPINNER):
            package_dirs = list(find_pkg_dirs(repo_dir=repo_dir, query=package, exact=False))

        if package_dirs:
            found_none = False
            print(crayons.cyan(repo_dir.name, bold=True))

            for package_dir in package_dirs:
                print(4 * '' + package_dir.name)

    if found_none:
        print(
            crayons.magenta(f"I couldn't find ", bold=True) + crayons.green(package, bold=True) + crayons.magenta(
                " in my repositories", bold=True)
        )


@click.command()
@click.argument('package')
def install(package):
    """Install a package"""
    print(
        f'Finding packages with exact match{settings.LOADING}'
    )
    exact_match = True
    with Halo(spinner=settings.SPINNER):
        matching_dirs = find_pkg_dirs(package)

    if not matching_dirs:
        exact_match = False
        print(crayons.red('Exact match not found!'))
        print(f'Finding packages with similar names{settings.LOADING}')
        with Halo(spinner=settings.SPINNER):
            matching_dirs = [
                i.parent for i in settings.REPO_DIR.rglob('Dockerfile') if are_similar(i.parent.name, package)
            ]
    if matching_dirs:
        dir_index = 1
        # show a list of packages to choose from
        if len(matching_dirs) > 1 or not exact_match:
            count = 0
            print()
            for matching_dir in matching_dirs:
                count += 1
                print(
                    '[{0}] {1} ↜ {2}'.format(
                        crayons.white(count, bold=True),
                        crayons.green(matching_dir.name),
                        crayons.cyan(get_repo_name(matching_dir))
                    )
                )
            print()
            dir_index = click.prompt(
                crayons.white(
                    "Which one do you want me to install?", bold=True
                ),
                type=int, default=1
            )
        # resolve the required details for building the image
        pkg_dir = matching_dirs[dir_index - 1]
        repo_name = get_repo_name(pkg_dir)
        image_tag = f'{settings.IMAGE_TAG["namespace"]}{repo_name}.{pkg_dir.name}'

        print(f'Using Dockerfile from {pkg_dir}')
        print(f'tagging image as {image_tag}')

        print(
            '{0} {1}{2}'.format(
                crayons.white('Installing', bold=True),
                crayons.green(pkg_dir.name),
                crayons.white(settings.LOADING, bold=True)
            )
        )

        dfp = DockerfileParser(path=str(pkg_dir))

        if settings.LABELS['registry'] in dfp.labels:
            with Halo(spinner=settings.SPINNER):
                image = docker_client.images.pull(
                    dfp.labels[settings.LABELS['registry']]
                )
                image[0].tag(image_tag)
        else:
            print(
                "{0} {1} {2} {3}".format(
                    crayons.red("This docker file doesn't contain a"),
                    crayons.blue(settings.LABELS['registry']),
                    crayons.red('label'),
                    crayons.red("It is recommended to have it in production.")
                )
            )

            print(
                crayons.white("Building the docker image. This will take some time", bold=True) + settings.LOADING
            )

            with Halo(spinner=settings.SPINNER):
                docker_client.images.build(
                    path=str(pkg_dir),
                    tag=image_tag,
                    quiet=False
                )

        print(crayons.cyan(f'Successfully built image. Type `dockapt run {pkg_dir.name}` to use it'))
    else:
        print(
            crayons.magenta(f"I couldn't find ", bold=True) + crayons.green(package, bold=True) + crayons.magenta(
                " in my repositories", bold=True)
        )


@click.command()
def update():
    """update the repositories"""
    for repo_dir in settings.REPO_DIR.iterdir():
        try:
            repo = git.Repo(str(repo_dir))

            print(
                '{0} {1}{2}'.format(
                    crayons.white('Updating repo', bold=True),
                    crayons.green(repo_dir.name),
                    settings.LOADING
                )
            )
            with Halo(spinner=settings.SPINNER):
                repo.remote().pull()
        except git.exc.InvalidGitRepositoryError:
            pass

    print(crayons.cyan('All repos are up-to date!'))


def parse_dockapt_tag(tag):
    """Parses a given dockapt image tag and Returns - (<repo_name>, <package_name>)"""
    y = tag.split(settings.IMAGE_TAG['namespace'])
    z = y[-1].split(settings.IMAGE_TAG['separator'])
    t = z[-1].split(settings.IMAGE_TAG['tag_separator'])
    return z[0], t[0]


@click.command()
def upgrade():
    """update the installed packages"""
    for image in docker_client.images.list():
        dockapt_tags = [tag for tag in image.tags if tag.startswith(settings.IMAGE_TAG['namespace'])]

        if dockapt_tags:
            package_name = parse_dockapt_tag(dockapt_tags[0])[1]
            for pkg_dir in find_pkg_dirs(package_name):
                pkg_dir

    print(crayons.cyan('All packages are up-to date!'))


@click.command()
@click.argument('package')
def run(package):
    package_img = None
    for image in docker_client.images.list():
        dockapt_tags = [tag for tag in image.tags if tag.startswith(settings.IMAGE_TAG['namespace'])]

        if dockapt_tags and parse_dockapt_tag(dockapt_tags[0])[1] == package:
            package_img = image
            break

    if package_img:
        args = shlex.split(package_img.labels[settings.LABELS['run']])
        subprocess.call(['docker', 'run', *args, package_img.tags[0]])
    else:
        print(
            '{0} {1}'.format(
                crayons.green(package),
                crayons.magenta('is not installed!')
            )
        )


@click.command()
def _list():
    """list all installed packages"""
    for image in docker_client.images.list():
        dockapt_tags = [tag for tag in image.tags if tag.startswith(settings.IMAGE_TAG['namespace'])]

        if dockapt_tags:
            print(
                '{0} ↜ {1}'.format(
                    *parse_dockapt_tag(dockapt_tags[0])
                )
            )


cli.add_command(install)
cli.add_command(search)
cli.add_command(update)
cli.add_command(upgrade)
cli.add_command(run)
cli.add_command(_list, name='list')

if __name__ == "__main__":
    cli()
