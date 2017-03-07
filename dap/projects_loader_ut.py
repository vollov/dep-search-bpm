# -*- coding: utf-8 -*-
import unittest,os
from dap.projects_loader import ProjectsLoader
from common import TestConfig

class ProjectsLoaderUt(unittest.TestCase):
    def setUp(self):
        self.loader = ProjectsLoader('EDocs')
        test_config = TestConfig()
        self.data_path = os.path.join(test_config.get_data_path(),'dap')
        
    def test_readProjectFile(self):
        project_file_path = os.path.join(self.data_path, '.project')
        actual = set([u'AdvisorIdentityEJB', u'AdvisorIdentityEJBClient', \
                  u'AdvisorIdentity', u'AdvisorIdentityUtil', \
                  u'IWMBrokerPattern', u'IWMSharedCode'])
        expected = self.loader.readProjectFile(project_file_path)
        self.assertEqual(expected,actual,'read projects not match')
    
    def test_readClasspathFile(self):
        classpath_file_path = os.path.join(self.data_path, '.classpath')
        actual = self.loader.readClasspathFile(classpath_file_path)
        expected = set([u'IWMBrokerPattern', u'IWMPreferenceDataStoreUtil',\
                     u'IWMSharedCode', u'IWMUtil'])
        self.assertEqual(expected,actual,'read classpath not match')
        
    def test_readProjectDependency(self):
        '''Test Sample
        IWMPreferenceDataStoreEJBEAR -> IWMPreferenceDataStoreEJB,
                                    IWMPreferenceDataStoreEJBClient,
                                    IWMPreferenceDataStore,
                                    IWMPreferenceDataStoreUtil,
                                    IWMUtil,
                                    IWMSharedCode
                                    IWMBrokerPattern
                                     
        IWMPreferenceDataStoreEJB -> []
        IWMPreferenceDataStoreEJBClient -> [IWMPreferenceDataStoreUtil*]
        IWMPreferenceDataStore -> IWMBrokerPattern,IWMPreferenceDataStoreUtil,
                                    IWMSharedCode,IWMUtil
        IWMPreferenceDataStoreUtil -> []
        IWMUtil->[]
        IWMSharedCode -> [IWMSharedObjects]
        IWMBrokerPattern -> []
        * - dependency come form class path
        '''
        self.loader.readProjectDependency('IWMPreferenceDataStoreEJBEAR')
        dep_map = self.loader.getDependencyMap()
        expected = set([u'IWMUtil', u'IWMPreferenceDataStore',u'IWMPreferenceDataStoreUtil',u'IWMPreferenceDataStoreEJB', u'IWMSharedCode',u'IWMBrokerPattern',u'IWMPreferenceDataStoreEJBClient'])

        actual = dep_map['IWMPreferenceDataStoreEJBEAR']
        self.assertEqual(expected,actual,'project dependency not match')