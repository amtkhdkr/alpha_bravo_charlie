.RECIPEPREFIX = %

up:
%python ./scripts/bootstrap.py
%echo "Start creating containers"
%docker-compose -f build/deploy_all.yml up

ansible:
%echo "Start provisioning containers"

down:
%echo "Start deleting containers"
%docker-compose -f build/deploy_all.yml down

clean:
%echo "Remove all caches from the system"
%rm -rf logs
%rm -rf build
