# DockAPT
###### A magical fusion of Docker and APT [for Humans™](https://www.kennethreitz.org/projects)
__DockAPT__ brings together the power of Docker and APT into a single toolchain giving the best of both worlds!


## Why
_TLDR; I was tired of breaking my linux everyday._

1. APT is intrinsically designed to break your system.
2. Docker solves 1.
3. But, docker is designed for hackers, not the end user.

UNIX was built on the [philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) of modular software development.

Now, it's time for modular & _isolated_ software development

## Install
Make sure you have python3.6 on your system, or install it using [pyenv](https://github.com/pyenv/pyenv-installer)

- `$ pip3 install dockapt`
- `$ dockapt install self` #TODO
    - checks if docker is installed
    - creates the `~/.dockapt` directory
    - `git clone` [this](https://github.com/jessfraz/dockerfiles) for a (fairly large) collection of `Dockerfiles`
    - adds an alias file to your your `~/.bashrc` / `~/.zshrc`


## How-TO
If you know APT, you know dockapt, mostly.

- ✨
    - `$ dockapt search foobar`
    - `$ dockapt install foobar`
    - `$ dockapt run foobar` #TODO
    - `$ dockapt uninstall foobar` #TODO

- ✨
    - `$ dockapt list`
    - `$ dockapt update`
    - `$ dockapt upgrade` #TODO

- ✨
    - `$ dockapt-repo add https://github.com/foo/bar.git`
    - `$ dockapt-repo remove https://github.com/foo/bar.git`
    - `$ dockapt-repo list`

## Core ideology
While not completely worked out, it's still a good idea to write down how stuff should ideally work.

- Use existing technologies instead of creating new ones.
    - dockapt doesnt keep a database. It works mostly with the filesystem.
    - dockapt uses a `Dockerfile`'s `LABEL`(s), instead of its own `revolutionary` file

- Minimize developer effort in making projects "dockapt-compatible"
    - write out how to run your application and what it depends on, directly in your `Dockerfile`

- Avoid dependency hell as much as possible
    - Install dependencies separately for each package, as opposed to the usual one-pacakge-for-all-depends strategy.

- Only change the existing API if it's too botched up.
    - You might have noticed how dockapt keeps all the commands from `apt` but changes the API for `add-apt-repository`.

## How

#### search
- recursively searches `~/.dockapt/repositories/` for all `Dockerfile`(s)
- establishes the name of directory containing the `Dockerfile` as the package's name
- uses fuzzy matching for package names if required

#### install
- builds the package's `Dockerfile` when you run `dockapt install`
- builds the `Dockerfile` of all dependencies #TODO
- stores a file containing the docker image's hash and other meta-data #TODO

#### Dockerfiles
`Dockerfiles` contain `LABEL`(s) that help dockapt figure out what to do with that `Dockerfile`, like
- figuring out the dependencies
- how to actually run that image once its built
- docker registry image url that it can pull from, to save time building the image

## Local Development
```
git clone https://github.com/pycampers/dockapt.git
cd dockapt
pipenv install
```

`pipenv shell`

```
pip install --editable .
dockapt --help
```

## Screenshots and general updates

I've taken [this](https://github.com/devxpy/dockerfiles/blob/302decc29dc323d84f39b182aca6b8e62792fcc8/couchpotato/Dockerfile) as sort of a first try on making a working package.

#### Its a WIP, but this is what it can do as of now.
![dockapt-repo add](https://i.imgur.com/LNWtF2A.png)

![dockapt-repo list](https://i.imgur.com/R9mWc1W.png)

![dockapt install](https://i.imgur.com/xlr8ji9.png)

![dockapt install](https://i.imgur.com/flFydBi.png)
