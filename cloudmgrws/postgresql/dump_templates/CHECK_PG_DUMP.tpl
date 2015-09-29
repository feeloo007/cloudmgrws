if [ -z "$PGHOME" ]; then
    echo "\$PGHOME not defined" 2>&1
    exit 1
else
    export PG_DUMP=$PGHOME/bin/pg_dump
    export PG_DUMP_ALL=$PGHOME/bin/pg_dumpall
fi
