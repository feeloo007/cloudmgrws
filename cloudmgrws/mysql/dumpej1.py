# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

import  os

import 	sys

import 	execute
import  dump

@cloudmgrws.tools.dynamic_parameters(
    [
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'database',
            execute.get_l_databases
        ),
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'table',
            dump.get_l_tables
        ),
    ],
)
def dumpej1( topology_params, function_params, ssh, response, *args, **kwargs ):

     shell 						=		\
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
                         'CHECK_MYSQLDUMP',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'common',
                         'CHECK_MY_PRINT_DEFAULTS',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'common',
                         'CHECK_AND_SET_MY_PRINT_DEFAULTS_FOR_SECTION',
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
                         'dump',
                         'CHECK_AND_SET_DATABASE_OPTION',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'dump',
                         'CHECK_AND_SET_TABLE_OPTION',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'dumpej1',
                         'MYSQLDUMP',
                     ),
                 ],
             )
         )

     return cloudmgrws.ssh_tools.process_steps(
         [
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : dumpej1.__name__,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : shell,
                 cloudmgrws.ssh_tools.TESTS             : 		\
                     [
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s' % shell,
                          },
                     ]
             }
         ],
         ssh,
         response,
     )
