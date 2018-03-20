# DockAPT
A magical fusion of `docker` and `apt` [for Humans™](https://www.kennethreitz.org/projects)

## WHY
1. apt is intrinsically designed to break your system
2. docker solves 1 
3. but, docker is designed for hackers, not end user

## INSTALL
`$ pip3 install dockapt`
`$ dockapt install self`

#### what does this do?
- checks if docker is installed
- creates the `~/.dockapt` directory
- `git clone` [this](https://github.com/jessfraz/dockerfiles) for a (fairly large) collection of `Dockerfiles`  
- adds an alias file to your your `~/.bashrc` / `~/.zshrc`


## HOW-TO
If you know `apt`, you know `dockapt`, mostly.

- ✨
    - `$ dockapt search foobar`
    - `$ dockapt install foobar`
    - `$ foobar`
    - `$ dockapt remove foobar`

- ✨
    - `$ dockapt list`
    - `$ dockapt update`
    - `$ dockapt upgrade`

- ✨
    - `$ dockapt-repo add https://github.com/foo/bar.git`
    - `$ dockapt-repo remove https://github.com/foo/bar.git`
    - `$ dockapt-repo list`

## HOW
- recursively searches `~/.dockapt/repositories/` for all `Dockerfile`(s) 
- builds the corresponding `Dockerfile` when you run `dockapt install`
    - (I am currently looking into integration with docker registry so you can just pull pre-built images)
- adds an alias for the `docker run ...` command (from `Dockerfile` comments)

## Screenshots
#### Its a WIP, but this is what it can do as of now.
![dockapt-repo add](https://i.imgur.com/LNWtF2A.png)

![dockapt-repo list](https://i.imgur.com/R9mWc1W.png)

![dockapt install](https://i.imgur.com/xlr8ji9.png)

![dockapt install](https://i.imgur.com/flFydBi.png)
