if [ -z "$PGHOME" ]; then
    echo "\$PGHOME not defined" 2>&1
    exit 1
else
    export PSQL=$PGHOME/bin/psql
fi
