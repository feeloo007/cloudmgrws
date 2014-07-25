# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

import  os

import 	sys

import 	json

def get_l_installables_warfiles( topology_params, function_params, ssh, response, *args, **kwargs ):

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
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'common',
                        'CHECK_TOMCAT',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'CHECK_AND_SET_INSTALLER_DIR',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'GET_FILES',
                    )
                    ,
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
                        cloudmgrws.ssh_tools.STEP_NAME         : get_l_installables_warfiles.__name__,
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
            'installable_war',
            get_l_installables_warfiles
        ),
    ],
)
def war_installer( topology_params, function_params, ssh, response, *args, **kwargs ):

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
                        'common',
                        'CHECK_TOMCAT',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'CHECK_AND_SET_WEBAPPS_DIR',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'CHECK_AND_SET_INSTALLER_DIR',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'CHECK_AND_SET_Z00_WAR_INSTALLER_SAVER_DIRS',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'CHECK_GIT',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'CHECK_AND_SET_OLD_WEBAPP_PATH',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'CHECK_AND_SET_INSTALLABLE_WAR',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'GIT_SQUASH_Z00_WAR_INSTALLER_SAVER_DIRS',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'SAV_OLD_WEBAPP',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'SAV_NEW_WAR',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'RM_OLD_WEBAPP',
                    )
                    ,
                    sys.modules[
                        __package__
                    ].get_template(
                        'war_installer',
                        'INSTALL_NEW_WAR',
                    )
                    ,
                ],
            )
        )

    def decode( s ):
        try:
            return json.loads( s )
        except Exception, e:
            return s

    # Seul 2 lignes de stdout sont attendus
    # Les 2 lignes sont une chaine contenant un object JSON
    # l'objet JSON contient 2 éléments.
    # pour les 2 objets, is_git_command_available, booleen. true, la commande git était dispo sur le serveur distant, false, la commnde git n'était pas dispo
    # pour le premier objet, old_webapp_commit_id, le commit id de la sauvegarde de l'ancienne webapp
    # pour le second objet, new_war_commit_id, le commit id de la sauvegarde du nouveau war

    return cloudmgrws.ssh_tools.process_steps(
        [
            {
                cloudmgrws.ssh_tools.STEP_NAME         : war_installer.__name__,
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
                              cloudmgrws.ssh_tools.TEST_NAME              : "has_old_wepapp_commit_id_failed"
                              ,
                              cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: decode( result[ cloudmgrws.ssh_tools.STDOUT ][ 0 ] )
                              ,
                              cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status.__class__ is not dict
                              ,
                              cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: '%s is not JSON' % ( status )
                              ,
                         }
                         ,
                         {
                              cloudmgrws.ssh_tools.TEST_NAME              : "has_new_war_commit_id_failed"
                              ,
                              cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: decode( result[ cloudmgrws.ssh_tools.STDOUT ][ 1 ] )
                              ,
                              cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status.__class__ is not dict
                              ,
                              cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: '%s is not JSON' % ( status )
                              ,
                         }
                         ,
                    ]
            }
        ],
        ssh,
        response,
    )
