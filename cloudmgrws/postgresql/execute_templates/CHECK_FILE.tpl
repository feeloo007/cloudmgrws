if [ ! -f $EXECUTABLE_DIR/{{function_params.executable}} ]; then
    echo "$EXECUTABLE_DIR/{{function_params.executable}} does'nt exist" >&2
    exit 1
fi
