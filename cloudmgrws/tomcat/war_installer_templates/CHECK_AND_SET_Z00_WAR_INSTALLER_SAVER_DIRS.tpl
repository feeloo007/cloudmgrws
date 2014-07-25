Z00_WAR_INSTALLER_SAVER_DIR=$HOME/z00/savers
if [ ! -d "$Z00_WAR_INSTALLER_SAVER_DIR" ]; then
   echo "$Z00_WAR_INSTALLER_SAVER_DIR not found" 		>&2
   echo "auto creation"				 		>&2
   mkdir -p $Z00_WAR_INSTALLER_SAVER_DIR
fi
Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR=$Z00_WAR_INSTALLER_SAVER_DIR/new_war
if [ ! -d "$Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR" ]; then
   echo "$Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR not found" 	>&2
   echo "auto creation"						>&2
   mkdir $Z00_NEW_WAR_WAR_INSTALLER_SAVER_DIR
fi
Z00_OLD_WEBAPP_WAR_INSTALLER_SAVER_DIR=$Z00_WAR_INSTALLER_SAVER_DIR/old_webapp
if [ ! -d "$Z00_OLD_WEBAPP_WAR_INSTALLER_SAVER_DIR" ]; then
   echo "$Z00_OLD_WEBAPP_WAR_INSTALLER_SAVER_DIR not found"	>&2
   echo "auto creation"						>&2
   mkdir $Z00_OLD_WEBAPP_WAR_INSTALLER_SAVER_DIR
fi
