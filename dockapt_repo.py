import shutil

import click
import crayons
import git
from giturlparse import parse
from halo import Halo

import settings


@click.group()
def cli():
    pass


@click.command()
def _list():
    """List all the repositories"""
    for repo in settings.REPO_DIR.iterdir():
        print(repo.name)


@click.command()
@click.argument('query')
def remove(query):
    """Remove a repository"""
    repos = list(settings.REPO_DIR.glob(query))

    if len(repos) == 0:
        print(crayons.red('No matching repository found!'))
    else:
        if len(repos) == 1:
            repo = repos[0]
        else:
            count = 0
            for repo in repos:
                count += 1
                print(f'{count}: {repo.name}')
            num = click.prompt('\nI found multiple repos from that query. Tell me which one?', type=int)
            repo = repos[num - 1]

        if click.confirm(crayons.red(f'Are you sure you want to remove this repo ({repo.name})?')):
            shutil.rmtree(repo)
            print(crayons.blue(f'Successfully removed repo ({repo.name})'))
        else:
            raise click.Abort


@click.command()
@click.argument('git_remote')
def add(git_remote):
    """Add a new repository to look for Dockerfiles"""
    git_remote = parse(git_remote)

    if git_remote.valid:
        repo_name = f'{git_remote.owner}_{git_remote.repo}'
        destination = settings.REPO_DIR.joinpath(repo_name)

        if destination.exists():
            if click.confirm(crayons.cyan('That repo is already added, do you want me to add it again?')):
                print(crayons.red('Removing existing repo' + settings.LOADING))
                shutil.rmtree(destination)
            else:
                raise click.Abort

        print(
            '{0} {1}{2}'.format(crayons.white('Adding repository', bold=True), crayons.green(repo_name),
                                crayons.white(settings.LOADING, bold=True))
        )
        print(f'repo dir - {str(destination)}')
        with Halo(spinner=settings.SPINNER):
            git.Repo.clone_from(git_remote.url2git, str(destination))

        print(crayons.cyan('Successfully added repository ', bold=True) + crayons.green(repo_name))
    else:
        print(crayons.red("I don't think that's a valid git remote url, sorry."))


cli.add_command(add)
cli.add_command(remove)
cli.add_command(_list, name='list')

if __name__ == "__main__":
    cli()
