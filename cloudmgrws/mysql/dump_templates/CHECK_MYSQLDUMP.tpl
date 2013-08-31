if [ -z "$MYSQLDUMP" ]; then
    echo "\$MYSQLDUMP not defined" 2>&1
    exit 1
fi
