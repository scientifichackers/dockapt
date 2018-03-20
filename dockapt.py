import click
import click_tools
import crayons
import docker
from fuzzywuzzy import fuzz
from halo import Halo

import settings

docker_client = docker.from_env()


def get_repo_name(package_dir):
    """Extract the repo name, given a package dir"""
    return package_dir.parts[package_dir.parts.index(settings.REPO_DIR.name) + 1]


def are_similar(str1, str2):
    return fuzz.partial_ratio(str1, str2) >= settings.FUZZY_RATIO_CUTOFF


@click.group()
def cli():
    pass


@click.command()
@click.argument('package')
def search(package):
    for repo_dir in settings.REPO_DIR.iterdir():
        package_dirs = [i.parent for i in settings.REPO_DIR.rglob('Dockerfile') if package in i.parent.name]
        if package_dirs:
            click.echo(crayons.cyan(repo_dir.name, bold=True))

            for package_dir in package_dirs:
                with click_tools.indent(4):
                    click_tools.puts(4 * '' + package_dir.name)


@click.command()
@click.argument('package')
def install(package):
    """Install a package"""
    click.echo(
        f'Finding packages having exact match{settings.LOADING}'
    )
    exact_match = True
    with Halo():
        matching_dirs = [i.parent for i in settings.REPO_DIR.rglob('Dockerfile') if package == i.parent.name]

    if not matching_dirs:
        exact_match = False
        click.echo(crayons.red('Exact match not found!'))
        click.echo(f'Finding packages with similar names{settings.LOADING}')
        with Halo():
            matching_dirs = [
                i.parent for i in settings.REPO_DIR.rglob('Dockerfile') if are_similar(i.parent.name, package)
            ]
    if matching_dirs:
        dir_index = 1
        # show a list of packages to choose from
        if len(matching_dirs) > 1 or not exact_match:
            count = 0
            click.echo()
            for matching_dir in matching_dirs:
                count += 1
                click.echo(
                    '[{0}] {1} ↜ {2}'.format(
                        crayons.white(count, bold=True),
                        crayons.green(matching_dir.name),
                        crayons.cyan(get_repo_name(matching_dir))
                    )
                )
            click.echo()
            dir_index = click.prompt(
                crayons.white(
                    "Which one do you want me to install?", bold=True
                ),
                type=int, default=1
            )
        # resolve the required details for building the image
        required_dir = matching_dirs[dir_index - 1]
        repo_name = get_repo_name(required_dir)
        image_tag = settings.DOCKER_IMAGE_NAMESPACE + f'{repo_name}.{required_dir.name}'

        click.echo(
            '{0} {1}{2}'.format(
                crayons.white('Installing', bold=True),
                crayons.green(required_dir.name),
                crayons.white(settings.LOADING, bold=True)
            )
        )
        # build docker image
        click.echo(f'Using Dockerfile from {required_dir}')
        click.echo(f'tagging image as {image_tag}')
        with Halo():
            image = docker_client.images.build(
                path=str(required_dir),
                tag=image_tag,
                quiet=False
            )
            print(image)
    else:
        click.echo(
            crayons.magenta(f"I couldn't find ", bold=True) + crayons.green(package, bold=True) + crayons.magenta(
                " in my repositories", bold=True)
        )


cli.add_command(install)
cli.add_command(search)
if __name__ == "__main__":
    cli()
