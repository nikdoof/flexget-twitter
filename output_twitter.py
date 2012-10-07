import sys, logging
from flexget.utils.tools import MergeException, merge_dict_from_to 
from flexget.plugin import PluginError, register_plugin 
from flexget import manager 
from flexget.event import event 
from flexget.utils.template import render_from_task, get_template, RenderError 
from flexget import validator 

log = logging.getLogger('twitter') 

def options_validator():
    twitter = validator.factory('dict')
    twitter.accept('boolean', key='active')
    twitter.accept('text', key='template')
    twitter.accept('text', key='consumerkey', required=True)
    twitter.accept('text', key='consumersecret', required=True)
    twitter.accept('text', key='accesskey', required=True)
    twitter.accept('text', key='accesssecret', required=True)
    return twitter 


def prepare_config(config):
    config.setdefault('active', True)
    config.setdefault('template', "Flexget: {{ title }} accepted")
    return config 

@event('manager.execute.started') 
def setup(manager):
    if not 'twitter' in manager.config:
        return
        
    try:
        import tweepy
    except ImportError:
        raise PluginError('The Twtter plugin requires the tweepy module to be installed, please install it before using.')
        
    config = prepare_config(manager.config['twitter'])
    config['global'] = True
    global task_content
    task_content = {}
    print config
    for task in manager.tasks.itervalues():
        task.config.setdefault('twitter', {})
        try:
            merge_dict_from_to(config, task.config['twitter'])
        except MergeException, exc:
            raise PluginError('Failed to merge twitter config to task %s due to %s' % (task.name, exc))
        task.config.setdefault('twitter', config) 


class OutputTwitter(object):
    def validator(self):
        v = options_validator()
        v.accept('boolean', key='global')
        return v

    def on_task_output(self, task, config):

        config = prepare_config(config)

        # Initialize twitter client
        import tweepy
        auth = tweepy.OAuthHandler(config['consumerkey'], config['consumersecret'])
        auth.set_access_token(config['accesskey'], config['accesssecret'])
        api = tweepy.API(auth)
        
        for entry in task.accepted:
        
            try:
                content = entry.render(config['template'])
            except RenderError, e:
                log.error('Error rendering message: %s' % e)
                return
        
            if task.manager.options.test:
                log.info('Would update twitter with: %s' % content)
                continue
            try:
                api.update_status(content)
            except Exception, e:
                log.warning('Unable to post tweet: %s' % e) 

register_plugin(OutputTwitter, 'twitter', api_ver=2) 
manager.register_config_key('twitter', options_validator)
