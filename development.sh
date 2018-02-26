#!/bin/bash
if [[ -d venv ]]; 
then 
    echo Virtual env venv exists
else
    echo Creating virtual env 
    virtualenv venv
fi
echo Entering virtual env venv  - use exit to leave
export VIRTUAL_ENV="`pwd`/venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME
exec "bash"
