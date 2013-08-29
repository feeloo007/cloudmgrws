if [ -d $HOME/executables ]; then
    if [ ! -f $HOME/executables/{{function_params.executable}} ]; then
        echo "$HOME/executables/{{function_params.executable}} does'nt exist" >&2
        exit 1
    fi
else
    echo "$HOME/executables does'nt exist" >&2
    exit 1
fi
