# -*- encoding: utf8 -*-
from __future__ import with_statement

import  app
import 	sys
import 	pkg_resources
from    webob.exc               import HTTPConflict, HTTPOk
import  functools

from	collections		import namedtuple
from	collections		import OrderedDict

from  	cloudmgrws.ssh_tools	import	manage_ssh

def catch_not_found( f ):
    @functools.wraps( f )
    def wrapped( cmgrws, url ):
        try:
            return {
                app.Cloudmgrws._EXISTS      : True,
                app.Cloudmgrws._CHILDS      : dict(
                                                         ( k, sorted( list ( set ( v ) ) ) )
                                                         for k, v
                                                         in f( cmgrws, url ).items()
                                                     )
           }
        except KeyError, ke:
            return {
                app.Cloudmgrws._EXISTS : False,
                app.Cloudmgrws._CHILDS : {},
            }
        except Exception, e:
            assert( False ), u'Big Bug %s' % f.__name__
    return wrapped


DynamicParamNameAndDynamicAccessor = 					\
    namedtuple( 'DynamicParamNameAndDynamicAccessor', [ 'param_name', 'param_accessor' ] )

def dynamic_parameters(
    l_dynamic_param_name_and_dynamic_accessor = [],
    ):
    def wrapper( f ):

        assert								\
            isinstance(							\
                l_dynamic_param_name_and_dynamic_accessor,		\
                list,							\
            ), 'Big Bug'						\

        for k_v in 							\
            l_dynamic_param_name_and_dynamic_accessor:			\
                assert							\
                    isinstance(						\
                        k_v,						\
                        DynamicParamNameAndDynamicAccessor,		\
                    ), 'Big Bug'					\

        d_dynamic_param_name_and_dynamic_accessor =			\
            OrderedDict(
                l_dynamic_param_name_and_dynamic_accessor
            )

        @manage_ssh
        @functools.wraps( f )
        def wrapped( topology_params, function_params, ssh, response, *args, **kwargs ):

            if len( function_params ) > len( d_dynamic_param_name_and_dynamic_accessor ):
                raise HTTPConflict()

            if len( d_dynamic_param_name_and_dynamic_accessor ) > 0:

                l_valid_params			=			\
                    d_dynamic_param_name_and_dynamic_accessor.values()[ 0 ](
                        topology_params,
                        function_params,
                        ssh,
                        response,
                        *args,
                        **kwargs
                    )

                if len( function_params ) > 0:

                    # Check validity for dynamic param
                    for i, param in enumerate( function_params ):

                        if param not in l_valid_params:

                            # error on invalid dynamic param
                            # dealed on ssh_tools
                            raise HTTPConflict()

                        if i + 1 < len( d_dynamic_param_name_and_dynamic_accessor ):
                            l_valid_params              =                       \
                                 d_dynamic_param_name_and_dynamic_accessor.values()[ i + 1 ](
                                     topology_params,
                                     function_params,
                                     ssh,
                                     response,
                                     *args,
                                     **kwargs
                                )

                if len( function_params ) < len( d_dynamic_param_name_and_dynamic_accessor ):

                    e                           = HTTPOk()
                    e.next                      =                               \
                       {
                           d_dynamic_param_name_and_dynamic_accessor.keys()[
                               len( function_params )
                           ]:                                                   \
                               l_valid_params
                       }

                    raise e

            return f( topology_params, function_params, ssh, response, *args, **kwargs )

        return wrapped
    return wrapper
