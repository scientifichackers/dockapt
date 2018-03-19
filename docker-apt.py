# fire makes making command line tools easier
import fire

class DockerAPT:
  update
  install


if __name__ == '__main__':
  fire.Fire(DockerAPT)

"""
if [ -f ~/.bash_aliases ]; then
. ~/.bash_aliases
fi
"""