if [ -d $OLD_WEBAPP_PATH ]; then
    if [ ! -d $OLD_SAV_WEBAPP_PATH ]; then
        mkdir $OLD_SAV_WEBAPP_PATH
    fi
    echo "#################"									>&2
    echo "saving old webapp"									>&2
    rsync -Hauro --delete $OLD_WEBAPP_PATH/ $OLD_SAV_WEBAPP_PATH/				2> /dev/null > /dev/null
    if [ $? -ne 0 ]; then
         echo "rsync -Haurov --delete $OLD_WEBAPP_PATH $OLD_SAV_WEBAPP_PATH fails" 		>&2
         exit 1
    fi
    if [ "A$GIT" != "A" ]; then
        cd $OLD_SAV_WEBAPP_PATH
        $GIT checkout master									2> /dev/null > /dev/null
        if [ $? -ne 0 ]; then
            echo "$GIT checkout master fails in $OLD_SAV_WEBAPP_PATH" 				>&2
            exit 1
        fi
        echo $( date ) >> marker
        $GIT add -A 										2> /dev/null > /dev/null
        if [ $? -ne 0 ]; then
            echo "$GIT add -A fails in $OLD_SAV_WEBAPP_PATH" 					>&2
            exit 1
        fi
        $GIT commit -m "Auto creation from SAV_OLD_WEBAPP template
	date tracer : $( date )" 								2> /dev/null > /dev/null
        if [ $? -ne 0 ]; then
            echo "$GIT commit -m "..." fails in $OLD_SAV_WEBAPP_PATH" 				>&2
            exit 1
        fi
        echo { \"is_git_command_available\": true, \"old_webapp_commit_id\": \"$( $GIT rev-parse HEAD )\" }
    fi
    echo "old webapp saved"									>&2
    echo "################"									>&2
fi
