class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0


    def moveUp(self,i):
        while i // 2 > 0:
          if self.heapList[i].getF() < self.heapList[i // 2].getF():
            temp = self.heapList[i // 2];
            self.heapList[i // 2] = self.heapList[i];
            self.heapList[i] = temp;
          i = i // 2

    def insert(self,k):
      self.heapList.append(k)
      self.currentSize = self.currentSize + 1
      self.moveUp(self.currentSize)

    def moveDown(self,i):
      while (i * 2) <= self.currentSize:
          mc = self.minChild(i)
          if self.heapList[i].getF() > self.heapList[mc].getF():
              self.heapList[mc], self.heapList[i] = self.heapList[i], self.heapList[mc]
          i = mc

    def minChild(self,i):
      if i * 2 + 1 > self.currentSize:
          return i * 2
      else:
          if self.heapList[i*2].getF() < self.heapList[i*2+1].getF():
              return i * 2
          else:
              return i * 2 + 1

    def delMin(self):
      retval = self.heapList[1]
      self.heapList[1] = self.heapList[self.currentSize]
      self.currentSize = self.currentSize - 1
      self.heapList.pop()
      self.moveDown(1)
      return retval

    def buildHeap(self,alist):
      i = len(alist) // 2
      self.currentSize = len(alist)
      self.heapList = [0] + alist[:]
      while (i > 0):
          self.moveDown(i)
          i = i - 1

    def getRoot(self):
        return self.heapList[1];
