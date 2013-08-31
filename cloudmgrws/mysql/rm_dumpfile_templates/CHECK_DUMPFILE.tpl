if [ ! -f $DUMP_DIR/{{function_params.dumpfile}} ]; then
    echo "$DUMP_DIR/{{function_params.dumpfile}} does'nt exist" >&2
    exit 1
fi
