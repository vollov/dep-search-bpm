# -*- coding: utf-8 -*-

#from datetime import datetime
# import time
# DateTime
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, joinedload, lazyload


engine = create_engine('mysql://user:pass@abc.com/newrecoverydb', echo=True,\
                        convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


#from orm.database import Base

class Task(Base):
    """
    select t.name_ from jbpm_processdefinition d left join jbpm_task t on d.id_=t.PROCESSDEFINITION_ where d.id_=3655;
    """
    __tablename__ = 'jbpm_task'
    
    id = Column('id_', Integer, Sequence('id_'), primary_key=True)
    name = Column('NAME_',String(255))
    flow_definition_id = Column('PROCESSDEFINITION_', Integer, ForeignKey('jbpm_processdefinition.id_'))
    
    def __repr__(self):
        return "<Task('%d','%s')>" % (self.id, self.name)
    
class FlowDefinition(Base):
    __tablename__ = 'jbpm_processdefinition'
    
    id = Column('id_', Integer, Sequence('id_'), primary_key=True)
    name = Column('NAME_',String(255))
    version = Column('VERSION_', Integer)
    
    def __repr__(self):
        return "<FlowDefinition('%d','%s')>" % (self.id, self.name)
    
class Node(Base):
    """
    select n.name_ from jbpm_processdefinition d left join jbpm_node n on d.id_=n.PROCESSDEFINITION_ where d.id_=3655;
    """
    __tablename__ = 'jbpm_node'
    
    id = Column('id_', Integer, Sequence('id_'), primary_key=True)
    name = Column('NAME_',String(255))
    flow_definition_id = Column('PROCESSDEFINITION_', Integer, ForeignKey('jbpm_processdefinition.id_'))
    
    def __repr__(self):
        return "<Node('%d','%s')>" % (self.id, self.name)
    
class Transition(Base):
    """
    select t.id_, t.name_, n1.id_ as start_id, n1.name_ as start,n2.id_ as end_id,  n2.name_ as end from jbpm_processdefinition d left join jbpm_transition t on d.id_=t.PROCESSDEFINITION_ left join jbpm_node n1 on t.from_=n1.id_ left join jbpm_node n2 on t.to_=n2.id_ where d.id_=3655;
    """
    
    __tablename__ = 'jbpm_transition'
    
    id = Column('id_', Integer, Sequence('id_'), primary_key=True)
    name = Column('NAME_',String(255))
    flow_definition_id = Column('PROCESSDEFINITION_', Integer, ForeignKey('jbpm_processdefinition.id_'))
    start_node_id = Column('FROM_', Integer, ForeignKey('jbpm_node.id_'))
    end_node_id = Column('TO_', Integer, ForeignKey('jbpm_node.id_'))
    
    flow_definition = relationship("FlowDefinition")
    start = relationship("Node", foreign_keys=[start_node_id],lazy='joined')
    end = relationship("Node", foreign_keys=[end_node_id], lazy='joined')
    
    def __repr__(self):
        return "<Transition('%d','%s','%s','%s')>" % (self.id, self.name, self.start.name, self.end.name)

tasks = Task.query.filter(Task.flow_definition_id == 3655)
 
# for task in tasks:
#     print task
    #print task.id, task.name

transitions = Transition.query.filter(Transition.flow_definition_id == 3655)
 
for t in transitions:
    if t.start.name == 'biddingMemo' or t.end.name=='mortgageSale':
        print t