# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

@cloudmgrws.tools.number_function_parameter( nb = 0 )
@cloudmgrws.ssh_tools.manage_ssh
def execute( topology_params, function_params, ssh, response, *args, **kwargs ):

     return cloudmgrws.ssh_tools.process_steps(
         [
         ],
         ssh,
         response,
     )     
