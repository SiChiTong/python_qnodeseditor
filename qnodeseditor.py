# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 23:10:05 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class QNodesEditor(QObject):
    def __init__(self, parent = None):
        super(QNodesEditor, self).__init__(parent)
        self.m_scene = QGraphicsScene()   #Segmentation Fault
        self.m_connection = None
        
    def install(self, scene):
        scene.installEventFilter(self)
        self.m_scene = scene

    
    def eventFilter(self, object, event):
        from qneport import QNEPort
        from qneconnection import QNEConnection        
        from qneblock import QNEBlock
        if (event.type() == QEvent.GraphicsSceneMousePress):
            print "Mouse Pressed!"
            if (event.button() == Qt.LeftButton):
                print "Left Button pressed!"
                item = self.itemAt(event.scenePos())
                if ( item != None and item.type() == QNEPort.TYPE):
                    print "Port pressed!"
                    self.m_connection = QNEConnection(None, self.m_scene)
                    self.m_connection.setPort1(item)
                    self.m_connection.setPos1(item.scenePos())
                    print "Pos1 : "
                    print self.m_connection.m_pos1
                    self.m_connection.setPos2(event.scenePos())
                    print "Updating Path"
                    self.m_connection.updatePath()
                    
                    return True
                elif (item != None and item.type() == QNEBlock.TYPE):
                    pass
            elif (event.button() == Qt.RightButton):
                item = self.itemAt(event.scenePos())
                if ( item != None and item.type() == QNEBlock.TYPE):
                    item.hide()
                    del item #wild reference ??
        elif (event.type() == QEvent.GraphicsSceneMouseMove):
            if (self.m_connection != None):
                print "Mouse Moving"
                self.m_connection.setPos2(event.scenePos())
                print "Pos2 : "
                print self.m_connection.m_pos2            
                print "Updating Path"
                self.m_connection.updatePath()
                return True
        elif (event.type() == QEvent.GraphicsSceneMouseRelease):
            if (self.m_connection != None and event.button() == Qt.LeftButton):
                item = self.itemAt(event.scenePos())
                if(item != None and item.type() == QNEPort.TYPE):
                    port1 = self.m_connection.port1()
                    port2 = item
                    
                    if (port1.block() != port2.block and port1.isOutput() != port2.isOutput() and port1.isConnected(port2) == False):
                        self.m_connection.setPos2(port2.scenePos())
                        self.m_connection.setPort2(port2)
                        self.m_connection.updatePath()
                else:
                    self.m_connection.hide()
                del self.m_connection      #invalid linking deleted!!
                self.m_connection = None
                return True
        return QObject.eventFilter(self, object, event)
         
    def save(self, ds):
        from qneblock import QNEBlock
        from qneconnection import QNEConnection
        
        for item in self.m_scene.childItems():
            if (item.type() == QNEBlock.TYPE):
                ds << item.type()
                item.save(ds)
        for item in self.m_scene.childItems():      #eccessary for depart?
            if (item.type() == QNEConnection.TYPE):
                ds << item.type()
                item.save(ds)
                
                
    def load(self, ds):
        pass
    
    #internal usage
    def itemAt(self, pos):
        items = self.m_scene.items(QRectF(pos - QPointF(1,1), pos + QPointF(2,2)))
        
        for item in items:
            if (item.type() > QGraphicsItem.UserType):
                return item
        return None
        

class QNEMainWindow(QMainWindow):
    def __init__(self):
        from qneblock import QNEBlock
        from qneport import QNEPort
        super(QNEMainWindow, self).__init__()
        
        self.m_scene = QGraphicsScene()
        self.m_view = QGraphicsView(self.m_scene)
        self.m_view.setRenderHint(QPainter.Antialiasing)
        
        self.m_block1 = QNEBlock(None, self.m_scene)
        self.m_block1.addPort("test", False, QNEPort.NAMEPORT)
        self.m_block1.addPort("TestBlock", False, QNEPort.TYPEPORT)
        self.m_block1.addInputPort("in1")
        self.m_block1.addInputPort("in2")
        self.m_block1.addInputPort("in3")
        self.m_block1.addOutputPort("out1")
        self.m_block1.addOutputPort("out2")
        self.m_block1.addOutputPort("out3")
        self.m_block1.setPos(self.m_view.sceneRect().center().toPoint())
        
        self.m_block2 = QNEBlock(None, self.m_scene)
        self.m_block2.addPort("test", False, QNEPort.NAMEPORT)
        self.m_block2.addPort("TestBlock", False, QNEPort.TYPEPORT)
        self.m_block2.addInputPort("in1")
        self.m_block2.addInputPort("in2")
        self.m_block2.addInputPort("in3")
        self.m_block2.addOutputPort("out1")
        self.m_block2.addOutputPort("out2")
        self.m_block2.addOutputPort("out3")
        self.m_block2.setPos(self.m_view.sceneRect().center().toPoint())
        
        self.m_nodesEditor = QNodesEditor(self)
        self.m_nodesEditor.install(self.m_scene)
        
        layout = QHBoxLayout()
        layout.addWidget(self.m_view)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("QNEMainWindow")
        
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    mainWindow = QNEMainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.show()

    sys.exit(app.exec_())
   
        