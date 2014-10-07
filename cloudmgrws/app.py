# -*- encoding: utf8 -*-
import	generate_config_ssh
import 	tools
import 	ssh_tools
import 	tomcat
import  jboss
import 	mysql
import	httpd
import 	ftp_installer
import 	os
from 	nagare 			import presentation
import 	json
import 	pkg_resources
from 	webob.exc 		import HTTPOk, HTTPNotFound, HTTPServiceUnavailable, HTTPConflict
import 	functools
from 	collections 		import namedtuple
from    fabric.exceptions	import NetworkError

@tools.catch_not_found
def match_default( cmgrws, url ):
    return { 'appcodes': cmgrws.d.keys() }

@tools.catch_not_found
def match_appcode( cmgrws, url ):
        return { 
                'aeras': cmgrws.d[ 
                              url[ Cloudmgrws._APPCODE ] 
                          ]  
               }

@tools.catch_not_found
def match_aera( cmgrws, url ):
        return { 
                'envs': cmgrws.d[ 
                            url[ Cloudmgrws._APPCODE ] ][ 
                            url[ Cloudmgrws._AERA ] 
                        ] 
               }

@tools.catch_not_found
def match_env( cmgrws, url ):
        return { 
                'appcomps': cmgrws.d[ 
                                url[ Cloudmgrws._APPCODE ] ][ 
                                url[ Cloudmgrws._AERA ] ][ 
                                url[ Cloudmgrws._ENV ] 
                            ] 
               }

@tools.catch_not_found
def match_appcomp( cmgrws, url ):
        return {
                'num_components': cmgrws.d[
                                      url[ Cloudmgrws._APPCODE ] ][
                                      url[ Cloudmgrws._AERA ] ][
                                      url[ Cloudmgrws._ENV ] ][
                                      url[ Cloudmgrws._APPCOMP ]
                            ]
               }

@tools.catch_not_found
def match_num_component( cmgrws, url ):
        cmgrws.d[
            url[ Cloudmgrws._APPCODE ] ][
            url[ Cloudmgrws._AERA ] ][
            url[ Cloudmgrws._ENV ] ][
            url[ Cloudmgrws._APPCOMP ] ][
            url[ Cloudmgrws._NUM_COMPONENT ]
        ]
        return {} 

class Cloudmgrws(object):
    def __init__( self ):
        self._d 		= json.loads( pkg_resources.resource_string( __name__, 'virtual_map.json' ) )

    def get_d( self ):
        return self._d
    d = property( get_d, None, None, None )

    _DEFAULT		= -1
    _APPCODE 		= 0
    _AERA 		= 1
    _ENV 		= 2
    _APPCOMP 		= 3
    _NUM_COMPONENT 	= 4

    _TOPOLOGY_PARAMS_NAME = [ 'appcode', 'aera', 'env', 'appcomp', 'num_component' ]

    _EXISTS		= 'EXISTS'
    _CHILDS		= 'CHILDS'

    _d_accepted_commands = {
        () 		: {},
        ( 'ROOT' ) 	: {
                           'FTP_STARTUP'	: ftp_installer.startup,
                           'FTP_SHUTDOWN'	: ftp_installer.shutdown,
                          },
        ( 'HTP' )	: {
                           'STATUS'	: httpd.status,
                           'STARTUP'	: httpd.startup,
                           'SHUTDOWN'	: httpd.shutdown,
                          },
        ( 'HTTPD' )	: {
                           'STATUS'	: httpd.status,
                           'STARTUP'	: httpd.startup,
                           'SHUTDOWN'	: httpd.shutdown,
                          },
        ( 'TOMCAT' )	: { 
                           'STATUS'		: tomcat.status, 
                           'STARTUP'		: tomcat.startup,
                           'SHUTDOWN'		: tomcat.shutdown,
                           'RMWORK'		: tomcat.rmwork,
                           'JSTACK'		: tomcat.jstack,
                           'RMWORK_WITH_PARAMS'	: tomcat.rmwork_with_params,
                           'WAR_INSTALLER'	: tomcat.war_installer,
                          },
        ( 'TOM' )	: {
                           'STATUS'		: tomcat.status,
                           'STARTUP'		: tomcat.startup,
                           'SHUTDOWN'		: tomcat.shutdown,
                           'RMWORK'		: tomcat.rmwork,
                           'JSTACK'		: tomcat.jstack,
                           'RMWORK_WITH_PARAMS'	: tomcat.rmwork_with_params,
                           'WAR_INSTALLER'	: tomcat.war_installer,
                          },
        ( 'JBOSS' )    : {
                           'STATUS'             : jboss.status,
                           'STARTUP'            : jboss.startup,
                           'SHUTDOWN'           : jboss.shutdown,
                          },
        ( 'MYSQL' )	: {
                           'STATUS'	: mysql.status,
                           'STARTUP'	: mysql.startup,
                           'SHUTDOWN'	: mysql.shutdown,
                           'EXECUTE'	: mysql.execute,
                           'DUMP'	: mysql.dump,
			   'RM_DUMPFILE'				\
                                        : mysql.rm_dumpfile,
                           'CHECK_ENV'	: mysql.check_env,
                          },
        ( 'MYS' )	: {
                           'STATUS'	: mysql.status,
                           'STARTUP'	: mysql.startup,
                           'SHUTDOWN'	: mysql.shutdown,
                           'EXECUTE'	: mysql.execute,
                           'DUMP'	: mysql.dump,
			   'RM_DUMPFILE'				\
                                        : mysql.rm_dumpfile,
                           'CHECK_ENV'	: mysql.check_env,
                          },
    }

    _d_keys_accepted_commands = {
        _DEFAULT	: lambda url: ( 'ROOT' ),
        _APPCODE 	: lambda url: (),
        _AERA 		: lambda url: (),
        _ENV 		: lambda url: (),
        _APPCOMP 	: lambda url: (),
        _NUM_COMPONENT 	: lambda url: ( url[ Cloudmgrws._APPCOMP ] ),
    }

    _d_keys_next = {
        _DEFAULT        : match_default,
        _APPCODE        : match_appcode,
        _AERA	        : match_aera,
        _ENV	        : match_env,
        _APPCOMP        : match_appcomp,
        _NUM_COMPONENT  : match_num_component,
    }

    @staticmethod
    def get_parent_key( url ):
        return Cloudmgrws._d_keys_accepted_commands.get( len( url ) - 1, lambda *args: {} )( url )

    @staticmethod
    def get_accepted_commands_for( url ):
        return dict( 
                ( '@%s' % command, callable_function )
                for command, callable_function
                in Cloudmgrws._d_accepted_commands.get( 
                       Cloudmgrws.get_parent_key( url )
                   ).items() 
               )

    def get_next( self, url ):
        #print url
        #print Cloudmgrws._d_keys_next.get( len( url ) - 1, lambda *args: {} )
        return Cloudmgrws._d_keys_next.get( len( url ) - 1, lambda *args: {} )( self, url )

def format_response( 
    is_ok, 
    information_message, 
    has_been_executed, 
    steps,
    next, 
    datas, 
    accepted_commands 
    ):

    information_message 	= '' if not information_message		else information_message
    steps 			= [] if not steps 			else steps
    next 			= {} if not next 			else next
    datas 			= [] if not datas 			else datas
    accepted_commands 		= [] if not accepted_commands 		else accepted_commands

    return json.dumps( 
        {
        	'is_ok'         	: is_ok,
        	'information_message'   : information_message,
       	 	'execution'     	: { 
                                   	   'has_been_executed'	: has_been_executed,
        			           'steps'        	: steps,
                                          },
        	'next'         		: next,
        	'datas'         	: datas,
        	'accepted_commands'     : accepted_commands,
        }
    )

def check_resource( f ):

    @functools.wraps( f )
    def wrapped( self, url, comp, http_method, request ):

        e	= None
        result 	= f( self, url, comp, http_method, request )

        if not result.get( Cloudmgrws._EXISTS ) :

            e              	= HTTPNotFound()
            e.content_type 	= 'application/json'
            e.body         	= format_response(
                                      is_ok            		= False,
				      information_message	= u'''/%s does not exist''' % '/'.join( url ),
                                      has_been_executed		= False,
                                      steps			= [],
                                      next            		= [],
                                      datas          		= [],
                                      accepted_commands		= [],
                          )
        else:

            e              	= HTTPOk()
            e.content_type      = 'application/json'
            e.body              = format_response(
                                      is_ok            		= True,
				      information_message	= '',
                                      has_been_executed		= False,
                                      steps			= [],
                                      next            		= result[ Cloudmgrws._CHILDS ],
                                      datas          		= [],
                                      accepted_commands		= Cloudmgrws.get_accepted_commands_for( url ).keys(),
                          	  )

        raise e

    return wrapped

def parse_command( f ):

    @functools.wraps( f )
    def wrapped( self, url, comp, http_method, request ):

        result = None

        if url:

            for i, u in enumerate( url ):

                if u in Cloudmgrws.get_accepted_commands_for( url[ :i ] ).keys():

                    try:

                        f( self, url[ :i ], comp, http_method, request )

                    except HTTPOk, e:
                        
                        ParamsTopology = namedtuple( 'ParamsTopology', Cloudmgrws._TOPOLOGY_PARAMS_NAME[ :i ] )

                        try:

                            Cloudmgrws.get_accepted_commands_for( url[ :i ] )[ u ]( 
                                ParamsTopology( *url[ :i ] ), 
                                url[ i+1: ]
                            )
                        except HTTPConflict, e:
                            e.content_type      = 'application/json'
                            e.body		= format_response(
                                                      is_ok                     = False,
                                                      information_message	= u'''%s not valid on /%s for %s''' % ( '/'.join( url[ i+1: ] ) , '/'.join( url[ :i ] ), u ),
                                                      has_been_executed         = False,
                                       		      steps			= [],
                                                      next                      = [],
                                                      datas                     = [],
                                                      accepted_commands         = [],
                                              )
                            raise e

                        except HTTPServiceUnavailable, e:
                            e.content_type      = 'application/json'
                            e.body              = format_response(
                                                      is_ok                     = False,
                                                      information_message	= u'''/%s not available\n%s''' % ( '/'.join( url ), e.information_message ),
                                                      has_been_executed         = False,
                                       		      steps			= [],
                                                      next                      = [],
                                                      datas                     = [],
                                                      accepted_commands         = [],
                                              )

                            del( e.information_message )

                            raise e

                        except HTTPOk, e:

                            e.content_type      = 'application/json'
                            e.body              = 			\
                                format_response(
                                    is_ok             	= e.is_ok,
                                    information_message	= e.information_message,
                                    has_been_executed 	= e.execution[ ssh_tools.HAS_BEEN_EXECUTED ],
                                    steps		= e.execution[ ssh_tools.STEPS ],
                                    next              	= e.next,
                                    datas               = e.datas,
                                    accepted_commands 	= e.accepted_commands
                                )

                            del( e.is_ok )
                            del( e.information_message )
                            del( e.execution )
                            del( e.next  )
                            del( e.datas )
                            del( e.accepted_commands )


                            raise e

                    except HTTPNotFound, e:
                        raise e
                    except Exception, e:
                        assert( False ), u'Big Bug %s' % f.__name__
            f( self, url, comp, http_method, request )
        else:
            f( self, url, comp, http_method, request )
    

    return wrapped
    

@presentation.render_for(Cloudmgrws)
def render(self, h, *args):
    return init( self, (), None, None, None )
    

@presentation.init_for(Cloudmgrws)
@parse_command
@check_resource
def init(self, url, comp, http_method, request):

    return self.get_next( url )

# ---------------------------------------------------------------

app = Cloudmgrws
#generate_config_ssh.generate_ssh_config_cloudmgr()
