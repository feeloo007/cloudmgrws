# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

CHECK_PID_COMMAND                               = 'check_pid'
STARTUP_COMMAND                    		= 'startup'
SLEEP_COMMAND					= 'sleep'

checks = {
    CHECK_PID_COMMAND                         	: 'pgrep -u $LOGNAME java',
    STARTUP_COMMAND                        	: 'source $HOME/.bash_profile ; jboss_init_redhat.sh start',
    SLEEP_COMMAND				: 'sleep 2',
}

@cloudmgrws.tools.dynamic_parameters()
def startup( topology_params, function_params, ssh, response, *args, **kwargs ):

     return cloudmgrws.ssh_tools.process_steps(
         [
             # Verification de la presence du processus
             # Si le proceccus n'existe pas l'arret est annule
             { 
                 cloudmgrws.ssh_tools.STEP_NAME		: CHECK_PID_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND	: checks[ CHECK_PID_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS		: [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_PROCESS_NUMBER_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDOUT ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Process number incorrect (%s). Startup aborted.' % status,
                                                           },
							   {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status == 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Startup aborted.' % checks[ CHECK_PID_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Startup aborted.',
                                                           },
                                                          ]
             },
             # Demande d'arret via une commande standard
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : STARTUP_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ STARTUP_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
							    cloudmgrws.ssh_tools.TEST_EXIT_ON_ERROR	: False,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Startup aborted.' % checks[ CHECK_PID_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
							    cloudmgrws.ssh_tools.TEST_EXIT_ON_ERROR	: False,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Startup aborted.',
                                                           },
                                                          ]
             },
             # Attente avant test
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : SLEEP_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ SLEEP_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Startup aborted.' % checks[ CHECK_PID_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Startup aborted.',
                                                           },
                                                          ]
             },
             # Test si le processus est mort
             # Si le processus n'est pas mort
             # les tests continuent
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : CHECK_PID_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ CHECK_PID_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_PROCESS_NUMBER_INCORRECT,
							    cloudmgrws.ssh_tools.TEST_EXIT_ON_ERROR	: False,
							    cloudmgrws.ssh_tools.TEST_EXIT_ON_NO_ERROR	: True,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDOUT ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 1,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Process number incorrect (%s). Startup aborted.' % status,
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_EXIT_ON_ERROR     : False,
                                                            cloudmgrws.ssh_tools.TEST_EXIT_ON_NO_ERROR  : True,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Startup aborted.' % checks[ CHECK_PID_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_EXIT_ON_ERROR     : False,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Startup aborted.',
                                                           },
                                                          ]
             },
         ],
         ssh,
         response,
     )     
