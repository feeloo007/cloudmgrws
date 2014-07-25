INSTALLABLE_WAR=$INSTALLER_DIR/{{function_params.installable_war}}
if [ ! -f $INSTALLABLE_WAR ]; then
    echo "$INSTALLABLE_WAR not found" >&2
    exit 1
fi
$JAVA_HOME/bin/jar tf $INSTALLABLE_WAR > /dev/null
if [ $? -ne 0 ]; then
    echo "$INSTALLABLE_WAR not a valid war" >&2
    exit 1
fi
