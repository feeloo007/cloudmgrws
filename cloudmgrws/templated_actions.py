# -*- encoding: utf8 -*-
from 	__future__ import with_statement

import  pyinotify

import  re

import 	os

def get_template( env, template_id ):

   return 								\
       env.get_template(
           '%s.tpl' % ( template_id )
       )


def get_template_dir( env, template_name ):
    """
    Construction du nom du repertoire contenant un template
    dans un environnement jinja2 passe en parametre
    """
    try:
       return 								\
           env.get_template(
               template_name
           ).filename[ :-len( template_name ) ].rstrip( os.sep )
    except:
        return None

def get_d_template_dir_to_env( d_envs ):
    """
    Recherche des repertoires contenant des templates
    """

    def try_list_templates( env ):
        try:
            return env.list_templates()
        except:
            return []

    return 								\
        dict(
        set(
            reduce(
                list.__add__,
                map(
                    lambda ( env_name, env ):                          	\
                        map(
                            lambda ( template_name ):                   \
                                (
                                    get_template_dir(
                                        env, 
                                        template_name 
                                    ),
                                    env,
                                ),
                            filter(
                                lambda template_name:                   \
                                    re.match(
                                        '^.*\.tpl$', 
                                        template_name 
                                    ),
                                try_list_templates( env )
                            )
                        ),
                    d_envs.iteritems(),
                )                                                       \
                or [ [] ]
            )
        )
    )

def inotify_setup( d_template_dir_to_env_name ):
    """
    Mise en place de la surveillance d'un ensemble de repertoire
    (cle de d_template_dir_to_env_name) appartenant a
    un environnement (valeur)
    """

    wm 				= pyinotify.WatchManager() 
    mask 			= pyinotify.IN_MODIFY

    class TemplateEventHandler( pyinotify.ProcessEvent ):

         def process_evt( o, event ):

             if d_template_dir_to_env_name.get(
                    event.path.rstrip( os.sep ) 
                )							\
                and							\
                re.match(						\
                    '^.*\.tpl$', 					\
                    event.name						\
                ):
                d_template_dir_to_env_name[ event.path ].cache.clear()

         process_IN_MODIFY	= process_evt

    template_notifier 		=					\
        pyinotify.ThreadedNotifier(
            wm,
            TemplateEventHandler()
        )

    template_notifier.coalesce_events()

    for dir in d_template_dir_to_env_name:

        wm.add_watch(
            dir,
            mask, 
            rec			= True,
            auto_add		= True,
        )

    template_notifier.start()
