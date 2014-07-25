echo "##############"                                                            					>&2
echo "saving new war"                                                            					>&2
cd $INSTALLER_DIR
rsync {{ function_params.installable_war }} $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR					2> /dev/null > /dev/null
if [ $? -ne 0 ]; then
    echo "rsync -v {{ function_params.installable_war }} $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR fails in SAV_NEW_WAR " 	>&2
    exit 1
fi
if [ "A$GIT" != "A" ]; then
    cd $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR
    $GIT checkout master												2> /dev/null > /dev/null
    if [ $? -ne 0 ]; then
        echo "$GIT checkout master fails in $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR"       				>&2
        exit 1
    fi
    echo $( date ) >> marker
    $GIT add -A 													2> /dev/null > /dev/null
    if [ $? -ne 0 ]; then
        echo "$GIT add -A fails in $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR"  						2> /dev/null > /dev/null
        exit 1
    fi
    $GIT commit -m "Auto creation from SAV_NEW_WAR template
	date tracer : $( date )"											2> /dev/null > /dev/null
    if [ $? -ne 0 ]; then
        echo "$GIT commit -m "..." fails in $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR"					>&2
        exit 1
    fi
    # Message envoye sur stdout, utilisable par cloudmgr
    echo { \"is_git_command_available\": true, \"new_war_commit_id\": \"$( $GIT rev-parse HEAD )\" }
fi
echo "new war saved" 													>&2
echo "#############" 													>&2
