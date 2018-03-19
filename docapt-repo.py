# fire makes making command line tools easier
import settings
import subprocess
from giturlparse import parse
import shutil
import click
import crayons


@click.group()
def cli():
    pass


@click.command()
def _list():
    """List all the repositories"""
    for repo in settings.REPO_DIR.glob('*'):
        click.echo(repo.name)


@click.command()
@click.argument('query')
def remove(query):
    """Remove a repository"""
    repos = list(settings.REPO_DIR.glob(query))

    if len(repos) == 0:
        click.echo(crayons.red('No matching repository found!'))
    else:
        if len(repos) == 1:
            repo = repos[0]
        else:
            count = 0
            for repo in repos:
                count += 1
                click.echo(f'{count}: {repo.name}')
            num = click.prompt('\nI found multiple repos from that query. Tell me which one?', type=int)
            repo = repos[num - 1]

        if click.confirm(crayons.red(f'Are you sure you want to remove this repo ({repo.name})?')):
            shutil.rmtree(repo)
            click.echo(crayons.blue(f'Successfully deleted repo ({repo.name})'))
        else:
            click.echo(crayons.green(f'Aborted!'))

@click.command()
@click.argument('git_remote')
def add(git_remote):
    """Add a new repository to look for Dockerfiles"""
    git_remote = parse(git_remote)

    if git_remote.valid:
        repo_name = f'{git_remote.owner}_{git_remote.repo}'
        destination = settings.REPO_DIR.joinpath(repo_name)

        if destination.exists():
            if click.prompt(crayons.cyan('That repo is already added, do you want me to add it again?')):
                click.echo(crayons.red('Removing existing repo..'))
                shutil.rmtree(destination)
            else:
                return

        click.echo(crayons.blue(f'Adding repo ({repo_name})..\n'))
        subprocess.check_call(['git', 'clone', git_remote.url2git, str(destination)])
        click.echo(crayons.green(f'\nSuccessfully added repo ({repo_name})'))
    else:
        click.echo(crayons.red("I don't think that's a valid git remote url, sorry."))


cli.add_command(add)
cli.add_command(remove)
cli.add_command(_list, name='list')

if __name__ == "__main__":
    cli()
