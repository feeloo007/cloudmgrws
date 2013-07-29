# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools
import 	time

RM_WORK_COMMAND         = 'rm_work'

commands = {
    RM_WORK_COMMAND	: 'source $HOME/.bash_profile ; rm -Rf $TOMCAT_HOME/work/Catalina/localhost/%s',
}

@cloudmgrws.tools.number_function_parameter( nb = 0 )
@cloudmgrws.ssh_tools.manage_ssh
def rmwork( topology_params, function_params, ssh, response, *args, **kwargs ):

     return cloudmgrws.ssh_tools.process_steps(
         [
             { 
                 cloudmgrws.ssh_tools.STEP_NAME		: RM_WORK_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND	: commands[ RM_WORK_COMMAND ],
                 cloudmgrws.ssh_tools.SHELL_PARAMS	: ( '*' ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s.' % checks[ RM_WORK_COMMAND ],
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr.',
                                                           },
                                                          ]
             },
         ],
         ssh,
         response,
     )     
