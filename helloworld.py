import tensorflow as tf
import numpy as np
b = tf.Variable(tf.ones((100,)))
W = tf.Variable(tf.random_uniform((784,100),-1,1))

x = tf.Variable(tf.random_uniform((100,784),-1,1))

sess = tf.Session()
sess.run(tf.initialize_all_variables())
print('_-----------------------------------------')

print(sess.run(b))
print('-----------------------------------------')
print(sess.run(tf.matmul(x,W)))
print('_-----------------------------------------')
print(sess.run(tf.matmul(x,W)+b))