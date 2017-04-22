#!/bin/bash
echo 'excuting send_reminder.py with args' 

echo "${@}"
venv/bin/python send_reminder.py "${@}"
