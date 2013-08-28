# -*- encoding: utf8 -*-
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools

def get_l_databases( topology_params, function_params, ssh, response, *args, **kwargs ):
    return [ '*' ]

def get_l_executables( topology_params, function_params, ssh, response, *args, **kwargs ):
    return [ 'script.sql' ]

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

     return cloudmgrws.ssh_tools.process_steps(
         [
         ],
         ssh,
         response,
     )     
