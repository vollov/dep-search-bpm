# -*- coding: utf-8 -*-

'''Use directed acyclic path to calculate the dependency'''
class Vertex:
    def __init__(self, name):
        self._name = name
        self.visited = True

class InValidDigraphError(RuntimeError):
    def __init__(self, arg):
        self.args = arg
      
class AdjecentListDigraph:
    '''represent a directed graph by adjacent list'''
    
    def __init__(self):
        '''use a table to store edges,
        the key is the vertex name, value is vertex list 
        '''
        self._edge_table = {}
        self._vertex_name_set = set()
        
    def __addVertex(self, vertex_name):
        self._vertex_name_set.add(vertex_name)
    
    def addEdge(self, start_vertex, end_vertex):
        if not self._edge_table.has_key(start_vertex._name):
            self._edge_table[start_vertex._name] = []
        self._edge_table[start_vertex._name].append(end_vertex)
        # populate vertex set
        self.__addVertex(start_vertex._name)
        self.__addVertex(end_vertex._name)
        
    def getNextLeaf(self, vertex_name_set, edge_table):
        '''pick up a vertex which has no end vertex. return vertex.name.
        algorithm:
        for v in vertex_set:
            get vertexes not in edge_table.keys()
            then get vertex whose end_vertex is empty  
        '''
#        print 'TODO: validate this is a connected tree'
        
        leaf_set = vertex_name_set - set(edge_table.keys())
        if len(leaf_set) == 0: 
            if len(edge_table) > 0:
                raise InValidDigraphError("Error: Cyclic directed graph")
        else:
            vertex_name = leaf_set.pop()
            vertex_name_set.remove(vertex_name)
            # remove any occurrence of vertext_name in edge_table
            for key, vertex_list in edge_table.items():
                if vertex_name in vertex_list:
                    vertex_list.remove(vertex_name)
                # remove the vertex who has no end vertex from edge_table
                if len(vertex_list) == 0:
                    del edge_table[key]
            return vertex_name
    
    def topoSort(self):
        '''topological sort, return list of vertex. Throw error if it is 
        a cyclic graph'''
        sorted_vertex = []
        edge_table = self.dumpEdges()
        vertex_name_set = set(self.dumpVertexes())
        
        while len(vertex_name_set) > 0:
            next_vertex = self.getNextLeaf(vertex_name_set, edge_table)
            sorted_vertex.append(next_vertex)
        return sorted_vertex
    
    def dumpEdges(self):
        '''return the _edge_list for debugging'''
        edge_table = {}
        for key in self._edge_table:
            if not edge_table.has_key(key): 
                edge_table[key] = []
            edge_table[key] = [v._name for v in self._edge_table[key]]
        return edge_table
    
    def dumpVertexes(self):
        return self._vertex_name_set