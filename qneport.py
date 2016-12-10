# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 01:08:31 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

#from qneconnection import QNEConnection

class QNEPort(QGraphicsPathItem):
    NAMEPORT = 1
    TYPEPORT = 2
    TYPE = QGraphicsItem.UserType + 1
    #puzzleCompleted = QtCore.pyqtSignal()
    
    def __init__(self, parent = None, scene = None):
        super(QNEPort, self).__init__(parent, scene)
        
        self.m_label = QGraphicsTextItem(self,scene)
        self.m_radius = 5;
        self.m_margin = 2;
        self.m_name = QString()
        self.m_isOutput = False
        self.m_ptr = 0                  #??
        

        self.m_connections = []
        
        p = QPainterPath()
        p.addEllipse(-self.m_radius, -self.m_radius, 2*self.m_radius, 2*self.m_radius)
        self.setPath(p);
        self.setPen(QPen(Qt.darkRed))
        self.setBrush(Qt.red)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.m_portFlags = 0
    
    # Setter. Gain the parent of the port
    # @param block: the existing QNEBlock
    def setQNEBlock(self, block):
        self.m_block = block
    
    # Setter. Gain the name of the port
    # @param name: the name of the port    
    def setName(self, name):
        self.m_name.append(name)
        self.m_label.setPlainText(self.m_name)
    
    # Setter. Determine the port is output or not    
    def setIsOutput(self, output):
        self.m_isOutput = output
        
        #fm = QFontMetrics(self.scene().font())
        #r = fm.boundingRect(self.m_name)
        
        if self.m_isOutput == True:
            self.m_label.setPos(-self.m_radius - self.m_margin - self.m_label.boundingRect().width(), - self.m_label.boundingRect().height()/2)
        else:
            self.m_label.setPos(self.m_radius + self.m_margin, - self.m_label.boundingRect().height()/2)
            
    # Getter
    # @Return the radius of the circulated Rect
    def radius(self):
        return self.m_radius
        
    # Getter
    # @Return Whether the port is output or not
    def isOutput(self):
        return self.m_isOutput

    # Getter
    # @Return the List of the connections
    def connections(self):
        return self.m_connections
     
    # Setter. Change the type of the port
    # @param  flag the enum of the type of the Port
    def setPortFlags(self, flag):
        self.m_portFlags = flag
        
        if (self.m_portFlags == self.TYPEPORT):
            font = QFont(self.scene().font())
            font.setItalic(True)
            self.m_label.setFont(font)
            self.setPath(QPainterPath())
        elif (self.m_portFlags == self.NAMEPORT):
            font = QFont(self.scene().font())
            font.setBold(True)
            self.m_label.setFont(font)
            self.setPath(QPainterPath())
    # Getter.
    # @Return the name of the port
    def portName(self):
        return self.m_name
    
    # Getter
    # @Return the flag of the port    
    def portFlags(self):
        return self.m_portFlags

    # Getter
    # @Return the type of the port as an integer        
    def type(self):
        return self.TYPE
    
    # Getter
    # @Return the parent block
    def block(self):
        return self.m_block
        
    # Getter
    # @Return the ptr
    def ptr(self):
        return self.m_ptr 
 
    # Setter
    # @param ptr a quint64 p ptr existed in C++       
    def setPtr(self, ptr):
        self.m_ptr = ptr

    # **Check if the port is connected to the others
    # @param other another port to be verified
    # @return True if connected, otherwise False
    def isConnected(self, other):
        for conn in self.m_connections:
            if ( conn.port1() == other or conn.port2() == other ):
                return True
        return False

    # **Change the connection shape between sender/receiver
    # @param change the type of the change
    # @param value
    # @return 
    def itemChange(self, change, value):
        if (change == self.ItemScenePositionHasChanged):
            for conn in self.m_connections:
                conn.updatePosFromPorts()
                conn.updatePath()
        return value