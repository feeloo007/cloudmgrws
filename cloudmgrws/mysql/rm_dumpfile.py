# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

import  os

import 	sys

def get_l_dumpfiles( topology_params, function_params, ssh, response, *args, **kwargs ):

    shell                                               =               \
        os.linesep.join(
            map(
                lambda env:                                             \
                    env.render(
                        topology_params = topology_params,
                        function_params = function_params,
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
                        'rm_dumpfile',
                       'GET_FILES',
                    ),
                ],
            )
        )

    return                                                              \
        map(
            lambda e:                                                   \
                e.lstrip( '.' + os.sep ),
            cloudmgrws.ssh_tools.process_steps(
                [
                    {
                        cloudmgrws.ssh_tools.STEP_NAME         : get_l_dumpfiles.__name__,
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
            'dumpfile',
            get_l_dumpfiles
        ),
    ],
)
def rm_dumpfile( topology_params, function_params, ssh, response, *args, **kwargs ):

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
                         'CHECK_AND_SET_DUMP_DIR',
                     ),
                     sys.modules[
                         __package__
                     ].get_template(
                         'rm_dumpfile',
                         'RM_DUMPFILE',
                     ),
                 ],
             )
         )

     return cloudmgrws.ssh_tools.process_steps(
         [
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : rm_dumpfile.__name__,
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
