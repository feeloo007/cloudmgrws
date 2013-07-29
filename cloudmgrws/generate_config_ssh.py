# -*- encoding: utf8 -*-
import 	app
from 	collections 	import namedtuple
import 	json
import 	pkg_resources


def template_username_default( pt ):
     return _d_template_username_appcomp[ pt.appcomp ]

def template_username_mairie( pt ):
     return '%s_%s_%s' % ( pt.appcode.lower(), _d_template_username_mairie[ ( pt.env, pt.num_component ) ], _d_template_username_appcomp[ pt.appcomp ] )

def template_username_d60( pt ):
     return '%s_%s_%s' % ( pt.appcode.lower(), _d_template_username_d60[ pt.num_component ], _d_template_username_appcomp[ pt.appcomp ] )

def get_username( pt ):
     return _d_template_username.get( pt.appcode, template_username_default )( pt )

_d_template_username = {
    'D60':      template_username_d60,
    'X01': 	template_username_mairie,
    'X02': 	template_username_mairie,
    'X03': 	template_username_mairie,
    'X04': 	template_username_mairie,
    'X05': 	template_username_mairie,
    'X06': 	template_username_mairie,
    'X07': 	template_username_mairie,
    'X08': 	template_username_mairie,
    'X09': 	template_username_mairie,
    'X10': 	template_username_mairie,
    'X11': 	template_username_mairie,
    'X12': 	template_username_mairie,
    'X13': 	template_username_mairie,
    'X14': 	template_username_mairie,
    'X15': 	template_username_mairie,
    'X16': 	template_username_mairie,
    'X17': 	template_username_mairie,
    'X18': 	template_username_mairie,
    'X19': 	template_username_mairie,
    'X20': 	template_username_mairie,
}

_d_template_username_mairie = {
    ( 'PR', '0001' ): 	'pr',
    ( 'PR', 'FO' ): 	'pr',
    ( 'PR', '0002' ): 	'pp',
    ( 'PR', 'BO' ): 	'pp',
    ( 'R7', '0001' ): 	'fo',
    ( 'R7', '0002' ):	'bo',
}

_d_template_username_d60 = {
    '0001'	: 'billetterie',
}

_d_template_username_appcomp = {
    'HTTPD'	: 'httpd',
    'TOMCAT'	: 'tomcat',
    'MYSQL'	: 'mysql',
}

def browse( d, level_max ):
    for k in iter( sorted( d ) ):
        for next_k in _browse( d[ k ], level_max, 0 ):
            yield ( k, ) + next_k

def _browse( d, level_max, level ):
    if level < level_max:
        for k in iter( sorted( d ) ):
            for next_k in _browse( d[ k ], level_max, level + 1 ):
                yield ( k, ) + next_k
    else:
        yield ()

def generate_host_block( d ):

    ParamsTopology = namedtuple( 'ParamsTopology', app.Cloudmgrws._TOPOLOGY_PARAMS_NAME )

    for k in browse( d, 4 ):
        pt = ParamsTopology( *k )
        yield '''Host %s-%s-%s-%s-%s
	User %s
        Port 22

''' % ( pt.appcode, pt.env, pt.appcomp, pt.num_component, pt.aera, get_username( pt ) )

def generate_ssh_config_cloudmgr():


    d = json.loads( pkg_resources.resource_string( __name__, 'virtual_map.json' ) )

    f = open( pkg_resources.resource_filename( __name__, 'ssh_config_cloudmgr' ), 'w' )

    for host_block in generate_host_block( d ):

        f.writelines( host_block )

    f.writelines( '''Host ???-??-HTTPD-????-*
        User httpd
	Port 22

Host ???-??-TOMCAT-????-*
        User tomcat
	Port 22

Host ???-??-MYSQL-????-*
        User mysql
	Port 22''')

    f.close()

if __name__ == '__main__':
   generate_ssh_config_cloudmgr()
