# -*- coding: utf-8 -*-

import requests
from netCDF4 import Dataset

from lib.parse_urls import parse_urls

class dataset:
    def __init__(self,datasetkey,datahub):
        self.datasetkey = datasetkey
        self.datahub=datahub

    def variables(self):
        variables=parse_urls(self.datahub.server,self.datahub.version,"datasets/"+self.datasetkey+"/variables",self.datahub.apikey)
        
        return variables.r.json()['variables']

    def variable_names(self):
        return list(map(lambda x: x['variableKey'], self.variables()))

    def standard_names(self):
        """
        return list of standard names of variables
        """
        return self.return_names('standard_name')

    def return_names(self,nameversion):
        """
        return list of variables by name type
        """
        stdnames=[]
        for k in self.variables():
            for j in k:
                if j == 'attributes':
                    for i in k[j]:
                        if i['attributeKey']==nameversion:
                            stdnames.append(i['attributeValue'])
        return stdnames

    def get_standard_name_from_variable_name(self,varname):
        for i in self.variables():
            if i['variableKey'] == varname:
                for j in i['attributes']:
                    if j['attributeKey']=='long_name':
                        return j['attributeValue']
        

    def long_names(self):
        """
        return list of long names of variables
        """
        return self.return_names('long_name')

    def get_tds_file(self,variable):
        """
        Until something better found ...
        return first file tds path that contains variable name, should work with either standard or long name!
        """

        tdaddr="http://{0}/{1}/data/dataset_physical_contents/fmi_hirlam_surface?apikey={2}".format(self.datahub.server,self.datahub.version,self.datahub.apikey)
        r=requests.get(tdaddr).json()
        for htt in r:
            found_vars=[j for j in htt['variables'] for i in j if j[i]==variable]
            if len(found_vars)>0:
                return htt['planetosOpenDAPVariables']

    def get_tds_field(self,variable):
        tdsfile=self.get_tds_file(self.get_standard_name_from_variable_name(variable))
        ds = Dataset(tdsfile)
        vari = ds.variables[variable]
        dimlen = len(vari.dimensions)
        if dimlen==4:
            return vari[0,0,:,:]
        elif dimlen==3:
            return vari[0,:,:]
        elif dimlen==2:
            return vari[:,:]
        else:
            raise ValueError("Cannot return 2D array for {0}".format(variable))
