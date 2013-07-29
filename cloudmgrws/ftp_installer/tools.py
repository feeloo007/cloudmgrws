# -*- encoding: utf8 -*-
from 	collections		import namedtuple
import	functools

FTPInstallerParamsTopology      = namedtuple( 'FTPInstallerParamsTopology', [ 'appcode', 'aera', 'env', 'appcomp', 'num_component' ] )
ftp_installer_topology_params   = FTPInstallerParamsTopology( *( 'Z00', 'VILLE', 'PR', 'FTP', '0001' ) )

def topology_params( f ):
    @functools.wraps( f )
    def wrapped( topology_params, *args, **kwargs ):
        return f( ftp_installer_topology_params, *args, **kwargs )
    return wrapped
