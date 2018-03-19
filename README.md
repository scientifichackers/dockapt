# DOCAPT
A magical fusion of `docker` and `apt` [for Humans™](https://www.kennethreitz.org/projects)

## WHY
1. apt is intrinsically designed to break your system
2. docker solves 1 
3. but, docker is designed for hackers, not end user

## INSTALL
`$ docapt install self`

#### what does this do?
- checks if docker is installed
- creates the `~/.docapt` directory
- `git clone` [this](https://github.com/jessfraz/dockerfiles) for a (fairly large) collection of `Dockerfiles`  
- adds an alias file to your your `~/.bashrc` / `~/.zshrc`


## TEACH ME MASTER!
If you know `apt`, you know `docapt`, mostly.

+
    + `$ docapt search foobar`
    + `$ docapt install foobar`
    + `$ foobar`
    + `$ docapt remove foobar`
+
    + `$ docapt list`
    + `$ docapt update`
    + `$ docapt upgrade`
+ 
    + `$ docapt-repo add https://github.com/foo/bar.git`
    + `$ docapt-repo remove https://github.com/foo/bar.git`
    + `$ docapt-repo list`

## HOW
- recursively searches `~/.docapt/repositories/` for all `Dockerfile`(s) 
- builds the corresponding `Dockerfile` when you run `docapt install`
- adds an alias for the `docker run ...` command (from `Dockerfile` comments)
- docker does it magic

