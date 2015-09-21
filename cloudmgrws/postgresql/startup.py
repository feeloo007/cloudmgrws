# -*- encoding: utf8 -*-
import	cloudmgrws.tools
import	cloudmgrws.ssh_tools

STARTUP_COMMAND					= 'startup'
CHECK_STATUS_COMMAND 				= 'check_status'

checks = {
    STARTUP_COMMAND				: 'source $HOME/.bash_profile ; pg_ctl -l $PGDATA/pg_log/postgresql.log -w start',
    CHECK_STATUS_COMMAND			: 'source $HOME/.bash_profile ; pg_ctl status'
}

@cloudmgrws.tools.dynamic_parameters()
def startup( topology_params, function_params, ssh, response, *args, **kwargs ):

     return cloudmgrws.ssh_tools.process_steps(
         [
	     # Verification du statut du serveur
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : CHECK_STATUS_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ CHECK_STATUS_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status == 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Startup aborted.' % checks[ CHECK_STATUS_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Startup aborted',
                                                           },
                                                          ]
             },
	     {
                 cloudmgrws.ssh_tools.STEP_NAME         : STARTUP_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ STARTUP_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Startup aborted.' % checks[ STARTUP_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Startup aborted',
                                                           },
                                                          ]

	     }
         ],
         ssh,
         response,
     )     
