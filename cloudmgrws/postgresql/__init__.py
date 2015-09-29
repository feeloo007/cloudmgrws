# -*- encoding: utf8 -*-
from 	cloudmgrws.postgresql.status   	import  status
from 	cloudmgrws.postgresql.startup  	import  startup
from 	cloudmgrws.postgresql.shutdown 	import  shutdown
from 	cloudmgrws.postgresql.execute 	import  execute
from 	cloudmgrws.postgresql.dump 	import  dump
#from 	cloudmgrws.postgresql.rm_dumpfile 	import  rm_dumpfile
#from 	cloudmgrws.mysql.check_env 	import  check_env

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
        'rm_dumpfile'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'rm_dumpfile_templates'
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
