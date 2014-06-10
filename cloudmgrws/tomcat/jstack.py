# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

JSTACK_COMMAND                    		= 'jstack'

checks = {
    JSTACK_COMMAND                        	: '''source $HOME/.bash_profile ; jstack -l $( jps | grep -v Jps | cut -f 1 -d ' ' )''',
}

@cloudmgrws.tools.number_function_parameter( nb = 0 )
@cloudmgrws.ssh_tools.manage_ssh
def jstack( topology_params, function_params, ssh, response, *args, **kwargs ):

     return cloudmgrws.ssh_tools.process_steps(
         [
             # Demande d'arret via une commande standard
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : JSTACK_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ JSTACK_COMMAND ],
                 cloudmgrws.ssh_tools.SHELL_PARAMS      : (),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
							    cloudmgrws.ssh_tools.TEST_EXIT_ON_ERROR	: False,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Startup aborted.' % checks[ CHECK_PID_COMMAND ],
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
         ],
         ssh,
         response,
     )
