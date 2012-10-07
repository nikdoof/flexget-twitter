from flexget.plugin import register_plugin, register_parser_option, DependencyError, PluginError 

class TwitterAuth(object):
    """Provides --twitter-auth"""
    def on_process_start(self, task):
        if task.manager.options.twitter_auth:
	    task.manager.disable_tasks()
            self.twitter_auth()
    
    def twitter_auth(self):
        try:
            import tweepy
        except:
            raise PluginError
            
        print "Please input your Consumer key/secret, if you do not have one register for one on http://dev.twitter.com/"
        print ""
        consumer_key = raw_input('Consumer Key: ').strip()
        consumer_secret = raw_input('Consumer Secret: ').strip()
        print "Attepting to authenticate..."
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth_url = auth.get_authorization_url()
        
        print "Please open the following URL in a browser and autheticate Flexget to use the Twitter account you wish to output to:"
        print auth_url
        print "Once completed, please provide the PIN code that Twitter returned"
        verifier = raw_input('PIN: ').strip()
        auth.get_access_token(verifier)
        print "Please add the following to your config.yml, either under your tasks or global as required"
        print ""
        print "twitter:"
        print " consumerkey: %s" % consumer_key
        print " consumersecret: %s" % consumer_secret
        print " accesskey: %s" % auth.access_token.key
        print " accesssecret: %s" % auth.access_token.secret
        
register_plugin(TwitterAuth, '--twitter-auth', builtin=True)
register_parser_option('--twitter-auth', nargs='?', const=True, help='Authenticate with Twitter.')
