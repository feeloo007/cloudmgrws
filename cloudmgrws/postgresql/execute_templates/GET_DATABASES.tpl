$PSQL --list --tuples-only | cut -d ' ' -f 2 | grep .
if [ $? -ne 0 ]; then
    echo "error accessing databases list" >&2
    exit 1
fi
