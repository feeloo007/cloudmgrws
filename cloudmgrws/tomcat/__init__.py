# -*- encoding: utf8 -*-
from cloudmgrws.tomcat.status 			import 	status
from cloudmgrws.tomcat.startup 			import 	startup
from cloudmgrws.tomcat.shutdown			import 	shutdown
from cloudmgrws.tomcat.rmwork			import 	rmwork
from cloudmgrws.tomcat.jstack			import 	jstack
from cloudmgrws.tomcat.rmwork_with_params	import 	rmwork as rmwork_with_params
from cloudmgrws.tomcat.war_installer		import 	war_installer

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
            )
        ,
        'war_installer'	:
            Environment(
                loader =						\
                    PackageLoader(
                        __name__,
                        'war_installer_templates'
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
