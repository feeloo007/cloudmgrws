# -*- encoding: utf8 -*-
import	cloudmgrws.tools
import	cloudmgrws.ssh_tools

SHUTDOWN_COMMAND					= 'shutdown'
CHECK_STATUS_COMMAND 				= 'check_status'

checks = {
    SHUTDOWN_COMMAND				: 'source $HOME/.bash_profile ; pg_ctl -w stop',
    CHECK_STATUS_COMMAND			: 'source $HOME/.bash_profile ; pg_ctl status'
}

@cloudmgrws.tools.dynamic_parameters()
def shutdown( topology_params, function_params, ssh, response, *args, **kwargs ):

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
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Shutdown aborted.' % checks[ CHECK_STATUS_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Shutdown aborted',
                                                           },
                                                          ]
             },
	     {
                 cloudmgrws.ssh_tools.STEP_NAME         : SHUTDOWN_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ SHUTDOWN_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Shutdown aborted.' % checks[ SHUTDOWN_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Shutdown aborted',
                                                           },
                                                          ]

	     }
         ],
         ssh,
         response,
     )     
