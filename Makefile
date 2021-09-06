.RECIPEPREFIX = %

up:
%python ./scripts/bootstrap.py
%echo "Start creating containers"
%docker-compose -f build/deploy_all.yml up --build

ansible:
%echo "Start provisioning containers"
%ANSIBLE_CFG=data/ansible.cfg ansible-playbook -i scripts/playbooks/inventory.yml scripts/playbooks/main.yml

down:
%echo "Start deleting containers"
%docker-compose -f build/deploy_all.yml down

clean:
%echo "Remove all caches from the system"
%rm -rf logs
%rm -rf build
%docker rmi amt-test
