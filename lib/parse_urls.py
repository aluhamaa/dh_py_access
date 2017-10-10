# -*- coding: utf-8 -*-


import requests


class parse_urls:
    def __init__(self,host,version,endpoint,apikey):
        """
        host: like api.planetos.com/
        """
        reqstr="https://{0}/{1}/{2}?apikey={3}".format(host,version,endpoint,apikey)
        print(reqstr)
        self.r = requests.get("https://{0}/{1}/{2}?apikey={3}".format(host,version,endpoint,apikey))
        
