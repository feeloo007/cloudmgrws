GIT=$( which git 2> /dev/null )
if [ "A$GIT" != "A" ]; then
    for d in $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR $Z00_OLD_WEBAPP_WAR_INSTALLER_SAVER_DIR; do
            cd $d
            GIT_FILES="$( $GIT ls-files 2> /dev/null )"
            if [ $? -ne 0 ]; then
                echo "$d not a git repository"			>&2
                echo "auto creation"				>&2
                $GIT init 1>&2 > /dev/null
                if [ $? -ne 0 ]; then
                   echo "$GIT init fails in $dir" 		>&2
                   exit 1
                fi
            fi
            $GIT config user.name  "Auto creator from CHECK_GIT template"
            $GIT config user.email "auto-creator@z00.apps.paris.mdp"
            if [ "A$GIT_FILES" == "A" ]; then
                echo "$d not initialized"			>&2
                echo "auto creation"				>&2
                echo $( date ) > marker
                $GIT add marker 				1>&2 > /dev/null
                if [ $? -ne 0 ]; then
                   echo "$GIT add marker fails in $dir" 	>&2
                   exit 1
                fi
                $GIT commit -m "Auto creation from CHECK_GIT template" 1>&2 > /dev/null
                if [ $? -ne 0 ]; then
                   echo "$GIT commit -m "..." fails in $dir" 	>&2
                   exit 1
                fi
            fi
    done
else
    # On envoit 2 objets JSON vide pour signifier que la commande
    # git n'existe pas
    echo "no git command"					>&2
    echo { \"is_git_command_available\": false, \"old_webapp_commit_id\": \"\" }
    echo { \"is_git_command_available\": false, \"new_war_commit_id\": \"\" }
fi
