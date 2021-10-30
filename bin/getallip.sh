#!/bin/bash

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#OUTPUTDIR=$(echo $DIR| rev| cut -d '/' -f2-| rev)"/outputinfo"
ansible-playbook -i /etc/ansible/hosts  ../getip/ansible/getallipmod.yml
