#!/bin/bash

setup () {
    echo  ------- SETUP -------
    apt-get update
    apt-get install -y zip
    pip install virtualenv
    virtualenv --python=python3 env
    source env/bin/activate
    pip install -r requirements.txt
    return $?
}

deploy() {
    echo ------- DEPLOY -------
    echo $1
    zappa update $1 || zappa deploy $1
    zappa certify $1 --yes
    return $?
}

setup && deploy $1
