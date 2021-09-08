# Alpha, Bravo and Charlie
A sample 3 container application which is provisioned and managed entirely using Ansible and Docker

# How to run

make up - Start all containers 

 ###Python bootstrap script:

- Makes sure that the [Jinja2 templates](https://jinja.palletsprojects.com/en/3.0.x/templates/) under the ./templates folder
- These templates provide substitution to variables like container names, SSH welcome messages and so on. 
  Example:
`{{alpha.ip_address}}` translates to `172.16.100.140` which is defined in constants.yml

- Ansible inventory is fully templated to ensure minimum hard-coding.

make ansible - Provision and customize the containers


## Common Components of each container
Based off of Ubuntu LTS 20.04
Init-like daemon runs as PID 1: OpenSSH server runs as a child
The hostnames match the container names (alpha, bravo, charlie) respectively
When executing make up, the containers should come up in the following
order:
1. alpha
2. bravo
3. charlie

Bravo should not start until the sshd running in alpha does not open its
listening port. Charlie should not start until the sshd running in bravo
does not open its listening port.

If the kernel runs short of memory and decides to unleash the OOM killer,
charlie should have more chance to survive than alpha and bravo.

The timezone inside the containers should be set to the value of the
timezone Ansible inventory variable.

APT inside the containers should be configured to use the APT mirror specified by the apt_mirror Ansible inventory variable. An example value for
the apt_mirror variable would be http://ftp.hosteurope.de/mirror/archive.ubuntu.com/ubuntu
(one of the official Ubuntu mirror servers).


## Network configuration

All three containers should be on a dedicated Docker network. The network should be a block of 64 IP addresses
starting with 172.16.100.128. The containers should have the following IP addresses:
- alpha: 172.16.100.140
- bravo: 172.16.100.141
- charlie: 172.16.100.142

## Inventory specific stuff
When we SSH into any container in the west group, the greeting message printed by the server should contain the following string: 

Once upon a time in the west.

When we SSH into any container in the east group, the greeting message printed by the server should contain the following string: 

Eastern promises.


## Alpha
Inventory: east

## Bravo
Inventory: east

Bravo should not be able to use more than 10% of a single CPU core.

Bravo should not be able to use more than 4 GB of memory.

## Charlie
Inventory: west

The contents of the path /opt/data will be persisted

Env Variables:

CONTI_ENV and CONTI_DB_NAME. If the user sets and exports these variables in the shell environment before executing
make up, their values should be visible by the sshd process running inside charlie.
- If the CONTI_ENV variable is not set by the user, it should default to prod.
- If the CONTI_DB_NAME variable is not set by the user, make up should fail
with the following error message: "You must specify CONTI_DB_NAME in the environment."

The sshd process running in charlie should be able to open at least 1048576 file descriptors.
