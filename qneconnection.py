# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 10:25:05 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class QNEConnection(QGraphicsPathItem):
    TYPE = QGraphicsItem.UserType + 2
    
    def __init__(self, parent = None, scene = None):
        super(QNEConnection, self).__init__(parent, scene)
        

        self.m_pos1 = QPointF()
        self.m_pos2 = QPointF()
        self.m_port1 = None
        self.m_port2 = None

        self.setPen(QPen(Qt.black, 2))
        self.setBrush(QBrush(Qt.NoBrush))
        self.setZValue(-1)
        
    # Define the start point of the connection path
    # @param p the pos of the start point
    def setPos1(self, p):
        self.m_pos1 = p
    
    # Define the end point of the connection path
    # @param p the pos of the end point        
    def setPos2(self, p):        
        self.m_pos2 = p
    
    # Define the port 1 of the connection path
    # param p the start port of the connection 
    def setPort1(self, p):
        #from qneport import QNEPort
        self.m_port1 = p
        self.m_port1.m_connections.append(self)
    
    # Define the port 2 of the connection path
    # param p the start port of the connection 
    def setPort2(self, p):
        #from qneport import QNEPort
        self.m_port2 = p
        self.m_port2.m_connections.append(self)
    
    # Internal Function
    # Update the data after the pos of points changed
    def updatePosFromPorts(self):
        self.m_pos1 = self.m_port1.scenePos()
        self.m_pos2 = self.m_port2.secnePos()
    
    # Internal Function
    # Update the path curve after the data is updated
    def updatePath(self):    
        p = QPainterPath()
        p.moveTo(self.m_pos1)
        
        dx = self.m_pos2.x() - self.m_pos1.x()
        dy = self.m_pos2.y() - self.m_pos2.y()
        
        #control point
        ctr1 = QPointF(self.m_pos1.x() + dx * 0.25, self.m_pos1.y() + dy * 0.1)
        ctr2 = QPointF(self.m_pos1.x() + dx * 0.75, self.m_pos2.y() + dy * 0.9)
        
        p.cubicTo(ctr1, ctr2, self.m_pos2)   #cublic curve
        self.setPath(p)
    
    # Getter
    # @Return the port1 of the connection
    def port1(self):
        return self.m_port1
        
    # Getter
    # @Return the port2 of the connection    
    def port2(self):
        return self.m_port1   
    # record the connection info
    # @param ds output: transfer the port1 and port2 key
    def save(self, ds):
        ds << self.m_port1
        ds << self.m_port2
    
    # load the connection info and update the path
    # @param ds input: transfer the port1 and port2 key
    # @param portMap: the relating connection maps
    def load(self, ds, portMap):
        ds >> ptr1
        ds >> ptr2
        
        self.setPort1(portMap[ptr1])
        self.setPort2(portMap[ptr2])
        self.updatePosFromPorts()
        self.updatePath()
        
    # Getter
    # @Return the type of the connection as an integer        
    def type(self):
        return self.TYPE