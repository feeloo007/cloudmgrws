echo "##############"                                          		>&2
echo "installing war"                                               	>&2
mkdir $OLD_WEBAPP_PATH
cd $OLD_WEBAPP_PATH
$JAVA_HOME/bin/jar xf $INSTALLABLE_WAR					1>&2	> /dev/null
if [ $? -ne 0 ]; then
    echo "error extracting $INSTALLABLE_WAR in $OLD_WEBAPP_PATH" 	>&2
    exit 1
fi
echo "end war installation"						>&2
echo "####################"                                         	>&2
