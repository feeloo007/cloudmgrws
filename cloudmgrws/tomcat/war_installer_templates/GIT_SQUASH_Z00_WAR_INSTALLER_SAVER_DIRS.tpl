if [ "A$GIT" != "A" ]; then
    for d in $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR $Z00_OLD_WEBAPP_WAR_INSTALLER_SAVER_DIR; do
        cd $d
        $GIT checkout master												2> /dev/null > /dev/null
        REVLIST="$( git rev-list HEAD 2> /dev/null )"
        SIZE=$( echo "$REVLIST" | wc -l )
        FIRST_COMMIT=$( echo "$REVLIST" | tail -n 1 )
        if [ $SIZE -gt 15 ]; then
            echo "##############"                                                                                       >&2
            echo "squashing $d"												>&2
            EDITOR="sed -i \"2,$( expr $SIZE - 9 )s/^pick\b/s/\"" $GIT rebase -i $FIRST_COMMIT				2> /dev/null > /dev/null
            if [ $? -ne 0 ]; then
                echo "$GIT rebase -i ... fails in $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR"                                 2> /dev/null > /dev/null
                exit 1
            fi
            $GIT gc													>&2
            if [ $? -ne 0 ]; then
                echo "$GIT gc fails in $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR"                                 		2> /dev/null > /dev/null
                exit 1
            fi
            echo "$d squashed"												>&2
            echo "###########"	  	                                                                                >&2
        fi
    done
fi
