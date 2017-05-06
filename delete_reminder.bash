#!/bin/bash
# just calls a py script...

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#$DIR/venv/bin/python $DIR/send_reminder.py "${@}"
echo "executing delete_reminder.py"
python $DIR/delete_reminder.py "${@}"
