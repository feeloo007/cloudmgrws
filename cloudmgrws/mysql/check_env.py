# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

import  os

import 	sys

@cloudmgrws.tools.dynamic_parameters(
)
def check_env( topology_params, function_params, ssh, response, *args, **kwargs ):

     shell_executable_dir 			=			\
         os.linesep.join(
             map(
                 lambda env:						\
                     env.render(
                         topology_params	= topology_params,
                         function_params	= function_params,
                         mysql			= 			\
                             {
                                 'my_print_defaults_for_section':	\
                                     'Z00_EXECUTE',
                             }
                     ),
                 [
                     sys.modules[
                         __package__
                     ].get_template(
                         'common',
                         'LOAD_ENV',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'execute',
                         'CHECK_AND_SET_EXECUTABLE_DIR',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'check_env',
                         'GET_EXECUTABLE_DIR',
                     ),
                 ],
             )
         )

     shell_dump_dir	 			=			\
         os.linesep.join(
             map(
                 lambda env:						\
                     env.render(
                         topology_params	= topology_params,
                         function_params	= function_params,
                         mysql			= 			\
                             {
                                 'my_print_defaults_for_section':	\
                                     'Z00_EXECUTE',
                             }
                     ),
                 [
                     sys.modules[
                         __package__
                     ].get_template(
                         'common',
                         'LOAD_ENV',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'dump',
                         'CHECK_AND_SET_DUMP_DIR',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'check_env',
                         'GET_DUMP_DIR',
                     ),
                 ],
             )
         )

     return cloudmgrws.ssh_tools.process_steps(
         [
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : '%s_executable_dir' % ( check_env.__name__ ),
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : shell_executable_dir,
                 cloudmgrws.ssh_tools.TESTS             : 		\
                     [
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s' % shell,
                          },
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : 'executable_dir_incorrect',
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.STDOUT ][ 0 ] if result[ cloudmgrws.ssh_tools.STDOUT ] else '',
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: len( status ) == 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: '''executable_dir doesn't exist''',
                          },
                     ]
             },
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : '%s_dump_dir' % ( check_env.__name__ ),
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : shell_dump_dir,
                 cloudmgrws.ssh_tools.TESTS             : 		\
                     [
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s' % shell,
                          },
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : 'dump_dir_incorrect',
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.STDOUT ][ 0 ] if result[ cloudmgrws.ssh_tools.STDOUT ] else '',
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: len( status ) == 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: '''dump_dir doesn't exist''',
                          },
                     ]
             },
         ],
         ssh,
         response,
     )
