import numpy as np
import tensorflow as tf
import time
start_time = time.time()
from mongoengine import *

connect('grbg', host='localhost', port=27017)

dbObjects = Measurements.objects()
x_input= dbObjects.only("takenAt")
y_input = dbObjects.only("percentageFull")

#model parameters
#order of polynomial
n=10
W = tf.Variable(tf.random_normal([n,1]), name='weight')
#bias
b = tf.Variable(tf.random_normal([1]), name='bias')

X=tf.placeholder(tf.float32,shape=[None,n])
Y=tf.placeholder(tf.float32,shape=[None, 1])


# preparing the data
def modify_input(x,x_size,n_value):
   x_new=np.zeros([x_size,n_value])
   for i in range(n):
      x_new[:,i]=np.power(x,(i+1))
      x_new[:,i]=x_new[:,i]/np.max(x_new[:,i])
   return x_new


#model
x_modified=modify_input(x_input,x_input.size,n)
Y_pred=tf.add(tf.matmul(X,W),b)

loss = tf.reduce_mean(tf.square(Y_pred -Y ))
#training algorithm
optimizer = tf.train.GradientDescentOptimizer(0.05).minimize(loss)
init = tf.initialize_all_variables()

#starting the session session
sess = tf.Session()
sess.run(init)

epoch=12000
for step in xrange(epoch):
     _, c=sess.run([optimizer, loss], feed_dict={X: x_modified, Y: y_input})


# Predict for next hour
new_input = modify_input(time.time()+3600,1,n)
print (sess.run(Y_pred, feed_dict={X:new_input}))
