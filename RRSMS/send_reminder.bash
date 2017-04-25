#!/bin/bash
echo 'excuting send_reminder.py with args' 
#sorry
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "${@}"
$DIR/venv/bin/python $DIR/send_reminder.py "${@}"
