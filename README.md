Personal Website
=========
Flask App powered personal website

Installation
----
The main system dependencies are Python, Postgresql, and their respective development packages.

#### 1. System dependencies:
On Ubuntu or Debian, first install:

    sudo apt-get install postgresql python-dev libpq-dev

Red Hat, Fedora, and other derivatives:

    yum install postgresql-devel postgresql-libs libpqxx-devel

Here's a [brief article](http://initd.org/psycopg/articles/2011/06/05/psycopg-windows-mingw/) on getting these dependencies running on Windows (exact instructions would be welcome).

#### 2. Python virtual environment and dependencies
It's probably a good idea to create a virtual environment for this project

Then, clone the repo, cd into it, and create a project virtual environment.

    git clone git@bitbucket.org:loanbee/loanbee-analysis-service.git
    cd loanbee-analysis-service
    python3 -m venv venv
    source venv/bin/activate

Once you have the virtual environment installed on your system, and the system dependencies, the rest is simple:

    pip install -r requirements.txt

Configuration
----
* Copy `.env_example` into a new file `.env` at the root of the project folder.
* Update `.env` with your development environment information.

Run
----
* To start the flask development server: `python app.py`.

Tests
----
* TODO Add documentation

Contributing
-----
Use [gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows#gitflow-workflow).
Kindly always tag releases to `develop` and `master`.

Deploying
-------
Ansible is used for deployment, so you should install that first on your machine.
See the [installation instructions](http://docs.ansible.com/ansible/latest/intro_installation.html).
For deployments to prod, make sure all changes are tested and working. Preferably, do a canary release first if possible.

Deployment commands:

    cd playbooks/deploy


    ansible-playbook service.yml -i hosts (-l [SERVER_GROUP]) --tags "deploy"
    e.g
    ansible-playbook service.yml -i hosts -l prod_app_servers --tags "deploy"
    ansible-playbook service.yml -i hosts -l test_app_servers --tags "deploy"

If you need to setup the app on a new server, add the `setup` tag to the role. 

       ansible-playbook service.yml -i hosts (-l [SERVER_GROUP]) --tags "setup,deploy"

You might also need to request for one or more `group_vars` files, which contain sensitive information such as passwords. Once you receive it, copy them to the `playbooks/deploy/group_vars` folder.
