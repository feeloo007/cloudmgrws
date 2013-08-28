# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools
import 	time

import	sys

@cloudmgrws.tools.dynamic_parameters()
def rmwork( topology_params, function_params, ssh, response, *args, **kwargs ):

     return								\
         sys.modules[ __package__ ].rmwork_with_params(
             topology_params,
             ( '*', ),
             ssh,
             response,
             *args,
             **kwargs
         )
