#!/bin/bash
if [[ -d venv ]]; 
then 
    echo exists; 
else
    virtualenv venv
fi
export VIRTUAL_ENV="`pwd`/venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME
echo "Entering virtual env - exit to quit"
exec bash
