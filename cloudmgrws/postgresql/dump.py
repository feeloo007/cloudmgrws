# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

import  os

import 	sys

import 	execute

def get_l_tables( topology_params, function_params, ssh, response, *args, **kwargs ):


    if function_params.database == '*':
        return [ '*', ]

    shell                                               =               \
        os.linesep.join(
            map(
                lambda env:                                             \
                    env.render(
                        topology_params = topology_params,
                        function_params = function_params
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
                        'common',
                        'CHECK_PSQL',
                    ),
                    sys.modules[
                        __package__
                    ].get_template(
                        'dump',
                        'GET_TABLES_FOR_DATABASE',
                    ),
                ],
            )
        )

    return                                                              \
        [ '*' ]								\
        +								\
        map(
            lambda e:                                                   \
                e.lstrip( '.' + os.sep ),
            cloudmgrws.ssh_tools.process_steps(
                [
                    {
                        cloudmgrws.ssh_tools.STEP_NAME         : get_l_tables.__name__,
                        cloudmgrws.ssh_tools.SHELL_COMMAND     : shell,
                        cloudmgrws.ssh_tools.TESTS             :        \
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
            ).execution[
                cloudmgrws.ssh_tools.STEPS
            ][
                -1
            ][
                cloudmgrws.ssh_tools.STDOUT
            ]
        )


@cloudmgrws.tools.dynamic_parameters(
    [
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'database',
            execute.get_l_databases
        ),
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'table',
            get_l_tables
        ),
    ],
)
def dump( topology_params, function_params, ssh, response, *args, **kwargs ):

     shell 						=		\
         os.linesep.join(
             map(
                 lambda env:						\
                     env.render(
                         topology_params	= topology_params,
                         function_params	= function_params
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
                          'common',
                          'CHECK_PSQL',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'dump',
                         'CHECK_PG_DUMP',
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
                         'dump',
                         'PG_DUMP',
                     ),
                 ],
             )
         )

     return cloudmgrws.ssh_tools.process_steps(
         [
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : dump.__name__,
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

