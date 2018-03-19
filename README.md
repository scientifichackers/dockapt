#Docker APT

A magical fusion of `apt` and `docker` [for Humans™](https://www.kennethreitz.org/projects)

(might be a replacement for snap and flatpak?)

##WHY
1. apt is intrinsically designed to break your system
2. docker solves 1 
3. but, docker is designed for hackers, not end user

##INSTALL
`$ docker-apt install self`

####what does this do?
- checks if docker is installed
- creates the `~/.docker-apt` directory
- `git clone` [this](https://github.com/jessfraz/dockerfiles) for a (fairly large) collection of `Dockerfiles`  
- adds an alias file to your your `~/.bashrc` / `~/.zshrc`


##TEACH ME MASTER!
If you know `apt`, you know `docker-apt`. Trust me.
- `$ docker-apt update`
- `$ docker-apt search foobar`
- `$ docker-apt install foobar`
- `$ foobar`
- `$ docker-apt upgrade`
- `$ docker-apt remove foobar`
- `$ docekr-apt add-repo https://github.com/foo/bar.git`

##HOW
- recursively searches `~/.docker-apt/dockerfiles/` for all `Dockerfile`(s) 
- builds the corresponding `Dockerfile` when you run `docker-apt install`
- adds an alias for the `docker run ...` command (from `Dockerfile` comments)
- docker does it magic

