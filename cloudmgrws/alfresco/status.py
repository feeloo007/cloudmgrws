# -*- encoding: utf8 -*-
import	cloudmgrws.tools
import	cloudmgrws.ssh_tools

CHECK_PID_COMMAND 				= 'check_pid'
CHECK_LSOF_COMMAND 				= 'check_lsof'

checks = {
    CHECK_PID_COMMAND				: 'pgrep -u $LOGNAME java',
    CHECK_LSOF_COMMAND 				: '/usr/sbin/lsof -w -a -u $LOGNAME -d ^mem -d ^cwd -d ^txt -d ^rtd -p $( pgrep -u $LOGNAME java )'
}

@cloudmgrws.tools.dynamic_parameters()
def status( topology_params, function_params, ssh, response, *args, **kwargs ):

     return cloudmgrws.ssh_tools.process_steps(
         [
             { 
                 cloudmgrws.ssh_tools.STEP_NAME		: CHECK_PID_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND	: checks[ CHECK_PID_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS		: [ 
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_PROCESS_NUMBER_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDOUT ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 1,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Process number incorrect (%s).' % status,
                                                           },
                                                           { 
                                                            cloudmgrws.ssh_tools.TEST_NAME		: cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS		: lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR	: lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE	: lambda status: 'Error executing %s' % checks[ CHECK_PID_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           { 
                                                            cloudmgrws.ssh_tools.TEST_NAME		: cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS		: lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR	: lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE	: lambda status: 'Look at stderr',
                                                           },
                                                          ]
             },
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : CHECK_LSOF_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ CHECK_LSOF_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_OPEN_FILES_NUMBER_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDOUT ] ) - 1,
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 768,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Open files number incorrect (%s).' % status,
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s' % checks[ CHECK_LSOF_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr',
                                                           },
                                                          ]
             },
         ],
         ssh,
         response,
     )     
