# -*- coding: utf-8 -*-
from graphviz import Digraph
import time
import datetime
now = str(datetime.datetime.now().year)+""+str(datetime.datetime.now().month)\
      +str(datetime.datetime.now().day)+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)+str(datetime.datetime.now().second)\
+str(datetime.datetime.now().microsecond)
fontname = "FangSong"
g = Digraph(now)
g.node(name='a',color='red',fontname = "FangSong",label="恭王府")
g.node(name='a',color='red',fontname = "FangSong",label="恭王府")
g.node(name='e',color='red',fontname = "FangSong",label="南京")
g.edge('a','e',label='123abc',color='green')
g.node(name='b',color='blue')
g.node(name='c',color='red',fontname = "FangSong",label="北京")
g.node(name='d',color='blue')
g.edge('a','b',label='abc',color='green')
g.edge('c','d',label='123',color='green')
g.edge('b','d',label='123',color='green')
# g.view()
g.render('test-output/'+str(now)+'.gv', view=True)