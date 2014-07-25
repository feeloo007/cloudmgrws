if [ -z "$JAVA_HOME" ]; then
    echo "\$JAVA_HOME not defined" >&2
    exit 1
fi
if [ -z "$TOMCAT_HOME" ]; then
    echo "\$TOMCAT_HOME not defined" >&2
    exit 1
fi
