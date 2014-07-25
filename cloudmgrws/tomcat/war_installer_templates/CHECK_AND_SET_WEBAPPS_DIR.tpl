WEBAPPS_DIR=$TOMCAT_HOME/webapps
if [ ! -d $WEBAPPS_DIR ]; then
    echo "$WEBAPPS_DIR not found" >&2
    exit 1
fi
