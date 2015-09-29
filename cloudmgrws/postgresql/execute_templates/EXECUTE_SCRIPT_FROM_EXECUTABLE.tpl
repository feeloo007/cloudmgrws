$PSQL -d $DATABASE --file=$EXECUTABLE_DIR/{{function_params.executable}}
if [ $? -ne 0 ]; then
    echo "error executing $EXECUTABLE_DIR/{{function_params.executable}}" >&2
    exit 1
fi
