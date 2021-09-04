.RECIPEPREFIX = %

up:
%echo "Start creating containers"
%python ./scripts/bootstrap.py

ansible:
%echo "Start provisioning containers"

down:
%echo "Start deleting containers"

clean:
%echo "Remove all caches from the system"
%rm -rf results
%rm -rf rendered
