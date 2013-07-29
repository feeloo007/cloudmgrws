# -*- encoding: utf8 -*-
from __future__ import with_statement

import  app
import 	sys
import 	pkg_resources
from    webob.exc               import HTTPConflict
import  functools

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


def number_function_parameter( nb = 0, function_params_accessors = [] ):
    def wrapper( f ):
        assert( nb == len( function_params_accessors ) ), 'Big Bug'
        f._nb_optional_params 		= nb
        f._function_params_accessors	= function_params_accessors
        @functools.wraps( f )
        def wrapped( topology_params, function_params, *args, **kwargs ):
            if nb != len( function_params ):
               raise HTTPConflict()
            return f( topology_params, function_params, *args, **kwargs )
        return wrapped
    return wrapper
