'''
Created on Apr 9, 2017

@author: satya
'''
from sklearn import tree

X=[[234,456,234],[33,454,323],[554,55,33],[234,456,234],[234,456,234]]
Y=['female','male','female','male','male']

clf=tree.DecisionTreeClassifier()
clf=clf.fit(X, Y)

pred=clf.predict([[234,456,234],[554,55,33]])

print pred