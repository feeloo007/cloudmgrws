# -*- encoding: utf8 -*-
from 	cloudmgrws.mysql.status   	import  status
from 	cloudmgrws.mysql.startup  	import  startup
from 	cloudmgrws.mysql.shutdown 	import  shutdown
from 	cloudmgrws.mysql.execute 	import  execute,dexecute
from 	cloudmgrws.mysql.dump 		import  dump,ddump
from 	cloudmgrws.mysql.dumphex 	import  dumphex
from 	cloudmgrws.mysql.dumpej1 	import  dumpej1
from 	cloudmgrws.mysql.rm_dumpfile 	import  rm_dumpfile
from 	cloudmgrws.mysql.check_env 	import  check_env

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
        'dumphex'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'dumphex_templates'
                )
           ),
        'dumpej1'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'dumpej1_templates'
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
        'check_env'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'check_env_templates'
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
