# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

import  os

import 	sys

import 	execute

import	re

import 	json

from 	contextlib	import closing

import 	ConfigParser

import 	StringIO

#####################################################################################
# Module permettant de manipuler
# des fichiers de format my.cnf
# pour pouvoir ajouter des paramètres
# aux function ajoutant ces fonctions dans leur décorant.
# La première implémentation sera pour une verison avec paramètres
# my.cnf # pour dump. Une version pour execute est envisageable.
#
# Contraintes :
# *
#  les contraintes pour le module
#  execute
#  doivent être respectées, c'est à dire
#  que le répertoire vérifié dans
#  execute_templates/CHECK_AND_SET_EXECUTABLE_DIR.tpl
#  doit exister, car on stocke les configurations
#  spécifiques sont stockés dans le sous-répertoire
#  .my.cnf de ce répertoire
#
# *
#  les templates associées sont stockés en tant que
#  common
#  pour fonctionner, les noms de function_params doivent être :
#  my_extra_cnf
#  section
#  Par exemple :
#  @cloudmgrws.tools.dynamic_parameters(
#     [
#          cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
#              'my_extra_cnf',
#              get_l_my_extra_cnfs
#          ),
#          cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
#              'section',
#              get_l_sections
#          ),
#          cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
#              'database',
#              execute.get_l_databases
#          ),
#          cloudmgrws.tools.DynamicParamNameAndDynamicAccessor(
#              'table',
#              get_l_tables
#          ),
#      ],
#  )
#  def ddump( topology_params, function_params, ssh, response, *args, **kwargs ): ...
#####################################################################################


def get_l_my_extra_cnfs( topology_params, function_params, ssh, response, *args, **kwargs ):
    """
    Renvoit la liste des fichiers (de premier niveau) du répertoire de configuration des extras au format my.cnf.
    """

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
                        'GET_MY_CNF_EXTRA_FILES',
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
                        cloudmgrws.ssh_tools.STEP_NAME         : get_l_my_extra_cnfs.__name__,
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


def get_l_sections( topology_params, function_params, ssh, response, *args, **kwargs ):
    """
    Renvoit la liste des sections dans le fichier selectionné via function_params.my_extra_cnf
    """

    shell                                               =               \
        os.linesep.join(
            map(
                lambda env:                                             \
                    env.render(
                        topology_params = topology_params,
                        function_params = function_params,
                        mysql                   =                       \
                            {
                                'my_print_defaults_for_section':        \
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
                        'common',
                        'EXTRACT_MY_EXTRA_CNF',
                    ),
                ],
            )
        )

    def decode( s ):
        try:
            return json.loads( s )
        except Exception, e:
            print e
            return s

    def parse_sections( d ):
        config		=						\
            ConfigParser.SafeConfigParser( allow_no_value = True )
        with closing(
            StringIO.StringIO(
                os.linesep.join(
                    d[ 'content' ]
                )

            )
        ) as fd:
            config.readfp(
                fd
            )
        return config.sections()

    return                                                              \
        (
            lambda d:							\
                parse_sections(
                    d
                )
        )(
            json.loads(
                re.sub(
                    r'(\r\n|\r|\n)'
                    ,
                    ''
                    ,
                    ''.join(
                        cloudmgrws.ssh_tools.process_steps(
                            [
                                {
                                    cloudmgrws.ssh_tools.STEP_NAME         : get_l_sections.__name__,
                                    cloudmgrws.ssh_tools.SHELL_COMMAND     : shell,
                                    cloudmgrws.ssh_tools.TESTS             :        \
                                        [
                                             {
                                                  cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                  cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                  cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                  cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s' % shell,
                                             },
                                             {
                                                  cloudmgrws.ssh_tools.TEST_NAME              : "is_not_json"
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_STATUS            : lambda result:	\
                                                                                                    decode(
                                                                                                        re.sub(
                                                                                                            r'(\r\n|\r|\n)'
                                                                                                            ,
                                                                                                            ''
                                                                                                            ,
                                                                                                            ''.join(
                                                                                                                result[
                                                                                                                    cloudmgrws.ssh_tools.STDOUT
                                                                                                                ]
                                                                                                            )
                                                                                                        )
                                                                                                    )
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status.__class__ is not dict
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: '%s is not JSON' % ( status )
                                                  ,
                                             }
                                             ,
                                             {
                                                  cloudmgrws.ssh_tools.TEST_NAME              : "have_not_version"
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_STATUS            : lambda result:	\
                                                                                                    decode(
                                                                                                        re.sub(
                                                                                                            r'(\r\n|\r|\n)'
                                                                                                            ,
                                                                                                            ''
                                                                                                            ,
                                                                                                            ''.join(
                                                                                                                result[
                                                                                                                    cloudmgrws.ssh_tools.STDOUT
                                                                                                                ]
                                                                                                            )
                                                                                                        )
                                                                                                    )
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: not status.has_key( 'version' )
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: '%r has no key version' % ( status )
                                                  ,
                                             }
                                             ,
                                             {
                                                  cloudmgrws.ssh_tools.TEST_NAME              : "have_not_content"
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_STATUS            : lambda result:      \
                                                                                                    decode(
                                                                                                        re.sub(
                                                                                                            r'(\r\n|\r|\n)'
                                                                                                            ,
                                                                                                            ''
                                                                                                            ,
                                                                                                            ''.join(
                                                                                                                result[
                                                                                                                    cloudmgrws.ssh_tools.STDOUT
                                                                                                                ]
                                                                                                            )
                                                                                                        )
                                                                                                    )
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: not status.has_key( 'content' )
                                                  ,
                                                  cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: '%r has no key content' % ( status )
                                                  ,
                                             }
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
                )
            )
        )
