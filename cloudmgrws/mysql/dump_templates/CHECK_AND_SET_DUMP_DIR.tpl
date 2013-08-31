if [ ! -d $HOME/dumps ]; then
    echo "$HOME/dumps does'nt exist" >&2
    exit 1
fi
DUMP_DIR=$HOME/dumps
