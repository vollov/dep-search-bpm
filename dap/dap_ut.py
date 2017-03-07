# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
from dap.dap_graph import AdjecentListDigraph, Vertex

class AdjecentListDigraphUt(unittest.TestCase):
    '''complex query test driver for user DAO'''
    def setUp(self):
        self._digraph = AdjecentListDigraph()
        self._digraph.addEdge(Vertex('H'), Vertex('G'))
        self._digraph.addEdge(Vertex('H'), Vertex('F'))
        self._digraph.addEdge(Vertex('F'), Vertex('C'))
        self._digraph.addEdge(Vertex('G'), Vertex('D'))
        self._digraph.addEdge(Vertex('G'), Vertex('E'))
        self._digraph.addEdge(Vertex('E'), Vertex('A'))
        self._digraph.addEdge(Vertex('D'), Vertex('A'))
        self._digraph.addEdge(Vertex('E'), Vertex('B'))
        self._digraph.addEdge(Vertex('I'), Vertex('J'))
        self._digraph.addEdge(Vertex('J'), Vertex('A'))
        self._digraph.addEdge(Vertex('J'), Vertex('B'))
        
    def test_dumpEdges(self):
        expected = {'E': ['A', 'B'], 'D': ['A'], 'G': ['D', 'E'], 'F': ['C'], 'I': ['J'], 'H': ['G', 'F'], 'J': ['A', 'B']}
        print 'dumpEdges()=>', self._digraph.dumpEdges()
        self.assertEquals(self._digraph.dumpEdges(), expected, 'failed')
        
    def test_dumpVertexes(self):
        expected = set(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'J'])
        print 'dumpVertexes()=>', self._digraph.dumpVertexes()
        self.assertEquals(self._digraph.dumpVertexes(), expected, 'failed')
        
    def test_topoSort(self):
        expected = ['A', 'C', 'B', 'J', 'I', 'E', 'D', 'G', 'F', 'H']
        print 'topoSort()=>',self._digraph.topoSort()
        self.assertEquals(self._digraph.topoSort(), expected, 'failed')