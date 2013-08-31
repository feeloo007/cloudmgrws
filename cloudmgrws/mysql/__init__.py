# -*- encoding: utf8 -*-
from 	cloudmgrws.mysql.status   	import  status
from 	cloudmgrws.mysql.startup  	import  startup
from 	cloudmgrws.mysql.shutdown 	import  shutdown
from 	cloudmgrws.mysql.execute 	import  execute
from 	cloudmgrws.mysql.dump 		import  dump

from    jinja2                          import  			\
            Environment, 						\
            PackageLoader

import 	cloudmgrws.templated_actions

d_envs    		=						\
    {
        'common'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'templates'
                    )
            ),
        'status'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'status_templates'
                )
            ),
        'startup'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'startup_templates'
                ),
            ),
        'shutdown'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'shutdown_templates'
                    )
                ),
        'execute'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'execute_templates'
                )
           ),
        'dump'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'dump_templates'
                )
           ),
    }




get_template	= 							\
   lambda env_name, template_id:					\
       cloudmgrws.templated_actions.get_template(			\
          d_envs[ env_name ],
          template_id
   )




d_template_dir_to_env_name	=					\
    cloudmgrws.templated_actions.get_d_template_dir_to_env(
        d_envs
    )

print									\
    'templates dirs for %s : ' % ( __name__ ) + 			\
    ' '.join( d_template_dir_to_env_name.keys() )

cloudmgrws.templated_actions.inotify_setup(
    d_template_dir_to_env_name
)
