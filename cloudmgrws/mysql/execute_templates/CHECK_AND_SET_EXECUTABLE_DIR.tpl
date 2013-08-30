if [ ! -d $HOME/executables ]; then
    echo "$HOME/executables does'nt exist" >&2
    exit 1
fi
EXECUTABLE_DIR=$HOME/executables
