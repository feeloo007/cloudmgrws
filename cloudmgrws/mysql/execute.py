# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

import  os

import 	sys

# Ajouté pour définir dexecute, version de dump utilisant
# des paramètres extra issue de fichier au format my.cnf
import  my_extra_cnf

def get_l_databases( topology_params, function_params, ssh, response, *args, **kwargs ):

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
                        'common',
                        'CHECK_MYSQL',
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
                        'execute',
                        'GET_DATABASES',
                    ),
                ],
            )
        )

    cloudmgrws.ssh_tools.process_steps(
        [
            {
                cloudmgrws.ssh_tools.STEP_NAME         : get_l_databases.__name__,
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
            },
        ],
        ssh,
        response,
    )

    return 								\
        [ '*' ] + 							\
        response.execution[
            cloudmgrws.ssh_tools.STEPS
        ][
            -1
        ][
            cloudmgrws.ssh_tools.STDOUT
        ]


def get_l_executables( topology_params, function_params, ssh, response, *args, **kwargs ):

    shell 						=		\
        os.linesep.join(
            map(
                lambda env:						\
                    env.render(
                        topology_params	= topology_params,
                        function_params	= function_params,
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
                        'execute',
                       'GET_FILES',
                    ),
                ],
            )
        )

    return 								\
        map(
            lambda e:							\
                e.lstrip( '.' + os.sep ),
            cloudmgrws.ssh_tools.process_steps(
                [
                    {
                        cloudmgrws.ssh_tools.STEP_NAME         : get_l_executables.__name__,
                        cloudmgrws.ssh_tools.SHELL_COMMAND     : shell,
                        cloudmgrws.ssh_tools.TESTS             : 	\
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
            get_l_databases
        ),
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'executable',
            get_l_executables
        ),
    ],
)
def execute( topology_params, function_params, ssh, response, *args, **kwargs ):

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
                         'common',
                         'CHECK_MYSQL',
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
                        'execute',
                       'CHECK_AND_SET_EXECUTABLE_DIR',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'execute',
                         'CHECK_FILE',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'execute',
                         'CHECK_AND_SET_DATABASE',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'execute',
                         'EXECUTE_SCRIPT_FROM_EXECUTABLE',
                     ),
                 ],
             )
         )

     return cloudmgrws.ssh_tools.process_steps(
         [
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : execute.__name__,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : shell,
                 cloudmgrws.ssh_tools.TESTS             : 		\
                     [
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s' % shell,
                          },
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Potential error',
                          },
                     ]
             }
         ],
         ssh,
         response,
     )     


@cloudmgrws.tools.dynamic_parameters(
    [
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'my_extra_cnf',
            my_extra_cnf.get_l_my_extra_cnfs
        ),
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'section',
            my_extra_cnf.get_l_sections
        ),
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'database',
            get_l_databases
        ),
        cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
            'executable',
            get_l_executables
        ),
    ],
)
def dexecute( topology_params, function_params, ssh, response, *args, **kwargs ):

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
                         'common',
                         'CHECK_MYSQL',
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
                        'execute',
                       'CHECK_AND_SET_EXECUTABLE_DIR',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                        'common',
                        'CHECK_AND_SET_MY_EXTRA_CNF_DIR',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                        'common',
                        'CHECK_AND_SET_MY_EXTRA_CNF_FILEPATH',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'common',
                         'CHECK_AND_SET_MY_PRINT_DEFAULTS_FOR_EXTRA_SECTION',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'execute',
                         'CHECK_FILE',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'execute',
                         'CHECK_AND_SET_DATABASE',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'execute',
                         'DEXECUTE_SCRIPT_FROM_EXECUTABLE',
                     ),
                 ],
             )
         )

     return cloudmgrws.ssh_tools.process_steps(
         [
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : execute.__name__,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : shell,
                 cloudmgrws.ssh_tools.TESTS             : 		\
                     [
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s' % shell,
                          },
                          {
                               cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                               cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                               cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                               cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Potential error',
                          },
                     ]
             }
         ],
         ssh,
         response,
     )
