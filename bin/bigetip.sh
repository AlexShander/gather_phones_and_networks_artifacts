#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
OUTPUTDIR=$(echo $DIR| rev| cut -d '/' -f2-| rev)"/outputinfo/"
echo $OUTPUTDIR
ansible-playbook -i /etc/ansible/hosts  ../getip/ansible/getbiipmod.yml --extra-vars "outputdir=/usr/local/asterisk-automation/outputinfo/ipaddresses/"
