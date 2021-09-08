.RECIPEPREFIX = %
BUILD_DIR = build
LOGS_DIR = logs
IMAGE_NAME = amt-test

up:
%python ./scripts/bootstrap.py
%echo "Start creating containers"
%docker-compose -f $(BUILD_DIR)/deploy_all.yml up --build
%echo "Copying SSH key into newly created containers"
%read -p "Full path to SSH public key: " mypubkey; for container in alpha bravo charlie; do cat $$mypubkey | docker exec -it $container 'cat >> .ssh/authorized_keys';done

ansible:
%echo "Start provisioning containers"
%ANSIBLE_CFG=data/ansible.cfg ansible-playbook -i $(BUILD_DIR)/inventory.yml scripts/playbooks/main.yml

down:
%echo "Start deleting containers"
%docker-compose -f $(BUILD_DIR)/deploy_all.yml down

clean:
%echo "Remove all caches from the system"
%rm -rf $(LOGS_DIR)
%rm -rf $(BUILD_DIR)
%docker rmi $(IMAGE_NAME)
