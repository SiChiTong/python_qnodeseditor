# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 10:11:00 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QNEBlock(QGraphicsPathItem):
    TYPE = QGraphicsItem.UserType + 3

    def __init__(self, parent = None, scene = None):
        super(QNEBlock, self).__init__(parent, scene)
        
        self.m_ports = []
        self.m_horzMargin = 0
        self.m_vertMargin = 0
        self.m_width = 0
        self.m_height = 0
        
        p = QPainterPath()
        p.addRoundedRect(-50, -15, 100, 30, 5, 5)
        self.setPath(p)
        self.setPen(QPen(Qt.darkGreen))
        self.setBrush(Qt.green)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.m_horzMargin = 20
        self.m_vertMargin = 5
        self.m_width = self.m_horzMargin
        self.m_height = self.m_vertMargin
        
        
    def addPort(self, name, isOutput, flags = 0, ptr = 0):
        from qneport import QNEPort
        port = QNEPort(self, None) #*** parent--children
        port.setName(name)
        port.setIsOutput(isOutput)
        port.setQNEBlock(self)
        port.setPortFlags(flags)
        port.setPtr(ptr)
        
        fm = QFontMetrics(self.scene().font())
        w = fm.width(name)
        h = fm.height()
        
        if (w > self.m_width - self.m_horzMargin):
            self.m_width = w + self.m_horzMargin
        self.m_height += h*2
        p = QPainterPath()
        p.addRoundedRect(-self.m_width / 2, -self.m_height / 2, self.m_width, self.m_height, 5, 5)
        self.setPath(p)
        
        y = -self.m_height / 2 + self.m_vertMargin + port.radius()
        

        if port.isOutput():
            port.setPos( self.m_width /2 + port.radius(), y)
        else:
            port.setPos( -self.m_width /2 - port.radius(), y)
#        for port_ in self.childItems():
#            if (port_.type() !=  QNEPort.TYPE):
#                continue
#            if port_.isOutput():
#                print "Output!"
#                print "y: %f"%y
#                print
#                port_.setPos( self.m_width /2 + port_.radius(), y)
#            else:
#                print "Input!"
#                print "y: %f"%y
#                print
#                port_.setPos( -self.m_width /2 - port_.radius(), y)
                
        return port
    
    def addInputPort(self, name):
        self.addPort(name, False)
    
    def addOutputPort(self, name):
        self.addPort(name, True)
    
    def addInputPorts(self, *args):
        for name in args:
            self.addInputPort(name)
    
    def addOutputPorts(self, *args):
        for name in args:
            self.addOutputPort(name)
    
    def save(self, ds):
        from qneport import QNEPort
        
        ds << self.pos()
        
        count = 0
        for port_ in self.childItems():
            if (port_.type() !=  QNEPort.TYPE):
                continue
            count += 1
        ds << count
        
        for port_ in self.childItems():
            if (port_.type() !=  QNEPort.TYPE):
                continue
            ds << port_.m_ptr
            ds << port_.portName()
            ds << port_.isOutput()
            ds << port_.portFlags()
            
    def load(self, ds, portMap):
        p = QPointF()
        ds >> p
        self.setPos(p)
        ds >> count
        for i in range(count):
            name = QString()
            ds >> ptr
            ds >> name
            ds >> output
            ds >> flags
            portMap[ptr] = self.addPort(name, output, flags, ptr)
            
    
    def paint(self, painter, option, widget):
        if (self.isSelected()):
            painter.setPen(QPen(Qt.darkYellow))
            painter.setBrush(Qt.yellow)
        else:
            painter.setPen(QPen(Qt.darkGreen))
            painter.setBrush(Qt.green)
        
        painter.drawPath(self.path())
        
    def clone(self):
        pass
    
    def ports(self):
        from qneport import QNEPort
        res = []
        for port_ in self.childItems():
            if (port_.type() ==  QNEPort.TYPE): 
                res.append(port_)
        return res
        
    def type(self):
        return self.TYPE
        
    # **??Change the connection shape between sender/receiver
    # @param change the type of the change
    # @param value
    # @return 
    def itemChange(self, change, value):
        return value