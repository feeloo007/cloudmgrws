# -*- encoding: utf8 -*-
from __future__ import with_statement

import 	ssh
import  functools
import	sys
import 	time
import 	pkg_resources
import 	fabric.network
import  fabric.api
import  fabric.utils
import 	exceptions
from    fabric.exceptions       import NetworkError
from    webob.exc               import HTTPOk, HTTPNotFound, HTTPServiceUnavailable

HAS_BEEN_EXECUTED			= 'has_been_executed'
STEPS					= 'steps'
STEP_NAME				= 'step_name'
SHELL_COMMAND				= 'shell_command'
SHELL_PARAMS				= 'shell_params'
TESTS					= 'tests'
TEST_NAME				= 'test_name'
TEST_STATUS				= 'test_status'
TEST_IS_IN_ERROR			= 'test_is_in_error'
TEST_ERROR_MESSAGE			= 'test_error_message'
TEST_EXIT_ON_ERROR			= 'test_exit_on_error'
TEST_EXIT_ON_NO_ERROR			= 'test_exit_on_no_erroir'
RETURN_CODE     			= 'return_code'
STDOUT					= 'stdout'
STDERR					= 'stderr'
HAVE_STDERR	 			= 'have_stderr'
IS_RETURN_CODE_INCORRECT		= 'is_return_code_incorrect'
IS_PROCESS_NUMBER_INCORRECT		= 'is_process_number_incorrect'
IS_OPEN_FILES_NUMBER_INCORRECT          = 'is_open_files_number_incorrect'

fabric.api.env[ 'abort_on_prompts' ] 	= True
fabric.api.env[ 'combine_stderr' ] 	= False

_conf 					= ssh.SSHConfig()
_conf_filename				= pkg_resources.resource_filename( __name__, 'ssh_config_cloudmgr' )


def reload_ssh_config_cloudmgr():
    try:
        with open( _conf_filename ) as fd:
            _conf.parse( fd )
    except IOError, e:
        fabric.utils.warn( "Unable to load SSH config file '%s'" % _conf_filename ) 
       

def work_on_ssh_config_cloudmgr( f ):

    reload_ssh_config_cloudmgr()

    @functools.wraps( f )
    def wrapped( *args, **kwargs ):

        return f( *args, **kwargs )

    return wrapped

@work_on_ssh_config_cloudmgr
def lookup( host_string ):

    d = fabric.network.parse_host_string( host_string )

    if not d[ 'user' ] or not d[ 'port' ]:
        host, user, port = d[ 'host' ], d[ 'user' ], d[ 'port' ]
        d = _conf.lookup( d[ 'host' ] )
        d[ 'host' ] = host
        if not d.has_key( 'user' ) or not d.has_key( 'port' ):
           if len( _conf._config ) <= 1:
               e 		= exceptions.SystemExit( 2 )
               e.message 	= "SSH config file '%s' loaded ?" % _conf_filename
               raise e
           else:
               d[ 'user' ] = d.get( 'user', fabric.api.env[ 'local_user' ] )
               d[ 'port' ] = d.get( 'port', fabric.api.env[ 'port' ] )
    return d

def connect( host_string ):
    return fabric.network.connect( **lookup( host_string ) )

def manage_ssh( f ):

    @functools.wraps( f )
    def wrapped( topology_params, function_params, ssh = None, response = None, *args, **kwargs ):

        response                    	= HTTPOk()
        response.information_message    = ''
        response.execution              = { 
                                           HAS_BEEN_EXECUTED 	: False, 
                                           STEPS		: [],
                                          }
        response.datas                  = []
        response.is_ok                  = False

    	remote_server_name          	= '%s-%s-%s-%s-%s' % (
            topology_params.appcode,
            topology_params.env,
            topology_params.appcomp,
            topology_params.num_component,
            topology_params.aera
        )

        try:

            f( 
                topology_params, 
                function_params, 
                connect( remote_server_name ),
                response, 
                *args, 
                **kwargs 
            )

        except NetworkError, e:
            # abnormal exit
            app_e = HTTPServiceUnavailable()
            app_e.information_message = e.message
            raise app_e
        except exceptions.SystemExit, e:
            # abnormal exit
            app_e = HTTPServiceUnavailable()
            if e.code == 2:
                app_e.information_message   	= e.message
            else:
                app_e.information_message 	= 'bad username (%s) or auth key issue' % lookup( remote_server_name )
            raise app_e
        except Exception, e:
            # abnormal exit
            print e.__class__
            assert( False ), 'Big Bug'
        except:
            # abnormal exit
            print sys.exc_info()
            assert( False ), 'Very Big Bug'
        finally:
            if ssh:
                try:
                    ssh.close()
                    ssh = None
                except:
                    pass

        raise response

    return wrapped


def exec_command( step_name, shell_command, ssh, response, *args, **kwargs ):

    shell_params = kwargs.get( SHELL_PARAMS, () )

    stdin, stdout, stderr = ssh.exec_command( shell_command % shell_params )
    r = { 
	STEP_NAME	: '[ STEP %s ] : %s' % ( len( response.execution[ STEPS ] ) + 1, step_name ),
        RETURN_CODE   	: stdout.channel.recv_exit_status(),
        STDOUT		: [ line.decode( 'iso8859', 'replace' ) for line in stdout.readlines() ],
	STDERR		: [ line.decode( 'iso8859', 'replace' ) for line in stderr.readlines() ],
    }
    response.execution[ STEPS ].append( r )
    return r

def process_steps( steps, ssh, response, *args, **kwargs ):

    for step in steps:

        result = exec_command(
	    step[ STEP_NAME ],
            step[ SHELL_COMMAND ],
            ssh,
            response,
            shell_params = step.get( SHELL_PARAMS, () ),
	)

        response.datas.append(
            dict(
	        [ ( t[ TEST_NAME ], ( True, 'Not tested' ) ) for t in step[ TESTS ] ]
            )
        )
        response.datas[ -1 ][ STEP_NAME ]	= step[ STEP_NAME ]

        for t in step[ TESTS ]:
            test_status 	= t[ TEST_STATUS ]( result )
            test_is_in_error 	= t[ TEST_IS_IN_ERROR ]( test_status )
            response.execution[ HAS_BEEN_EXECUTED ]	= True
            response.datas[ -1 ][ t[ TEST_NAME ] ]	= ( test_is_in_error, test_status )
            if not test_is_in_error and t.get( TEST_EXIT_ON_NO_ERROR, False ):
    		response.is_ok                          = True
                return response
            if test_is_in_error and t.get( TEST_EXIT_ON_ERROR, True ):
                response.information_message           	= t[ TEST_ERROR_MESSAGE ]( test_status )	
	    	return response

    response.execution[ HAS_BEEN_EXECUTED ]     = True
    response.is_ok                              = True
    return response
