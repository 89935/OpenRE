# -*- coding: utf-8 -*-
from graphviz import Digraph
import datetime
from graphviz import render
def outputAsGraphForSet(resultSet):
      now = str(datetime.datetime.now().year)+""+str(datetime.datetime.now().month)\
            +str(datetime.datetime.now().day)+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)+str(datetime.datetime.now().second)\
      +str(datetime.datetime.now().microsecond)
      fontname = "FangSong"
      g = Digraph(now)
      for result in resultSet:
            g.node(name=result[0],fontname = "FangSong")
            g.node(name=result[2],fontname = "FangSong")
            g.edge(result[0], result[2],fontname = "FangSong", label=result[1])
            print(result)
      # g.format = 'png'
      # g.engine = 'fdp'
      """
      neato
      circo
      twopi
      fdp 
      """
      g.render('test-output/'+str(now)+'.gv', view=True)

def outputAsGraphForList(resultList):
      now = str(datetime.datetime.now().year)+""+str(datetime.datetime.now().month)\
            +str(datetime.datetime.now().day)+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)+str(datetime.datetime.now().second)\
      +str(datetime.datetime.now().microsecond)
      fontname = "FangSong"
      g = Digraph(now)
      for result in resultList:
            for resultSet in result:
                  g.node(name=resultSet[0],fontname = "FangSong")
                  g.node(name=resultSet[2],fontname = "FangSong")
                  g.edge(resultSet[0], resultSet[2],fontname = "FangSong", label=resultSet[1])
      g.render('test-output/'+str(now)+'.gv', view=True)


def existGVFile(source):
      render('dot', 'pdf', source)

if __name__ == "__main__":
      existGVFile("test-output/20202262195621562.gv")