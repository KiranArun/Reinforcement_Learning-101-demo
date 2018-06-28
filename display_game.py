import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

import gym
import cv2
import time,os,sys,argparse

import A3C_helper_functions as helper

parser = argparse.ArgumentParser(description='Play and display game')
parser.add_argument('-g','--gap', type=float, default=0.0)
args = parser.parse_args()

state_size = 84**2
num_actions = 6

model_root_dir = '/content/'
model_logdir = os.path.join(model_root_dir,'logdir/')

run = 'run_01-lr_0.0001-nw_24-tmax_50'
checkpoint = 'final_model.ckpt'

model_checkpoint = os.path.join(model_logdir,run+'/'+checkpoint)

class AC_Network():
    def __init__(self, state_size, num_actions, scope):
        with tf.variable_scope(scope):
            
            self.inputs = tf.placeholder(shape=[None, state_size], dtype=tf.float32)
            self.inputs_reshaped = tf.reshape(self.inputs, shape=[-1, 84, 84, 1])
            
            
            self.conv1 = tf.layers.conv2d(inputs=self.inputs_reshaped,
                                          filters=16,
                                          kernel_size=[8, 8],
                                          strides=[4, 4],
                                          activation=tf.nn.elu,
                                          padding='SAME')
            self.conv2 = tf.layers.conv2d(inputs=self.conv1,
                                          filters=32,
                                          kernel_size=[4, 4],
                                          strides=[2, 2],
                                          activation=tf.nn.elu,
                                          padding='SAME')
            
            self.fc1 = tf.layers.dense(inputs=tf.layers.flatten(self.conv2),
                                       units=256,
                                       activation=tf.nn.elu)
            

            lstm_state_size = 256
            lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_units=lstm_state_size, state_is_tuple=True)

            self.initial_state = (np.zeros([1,lstm_state_size]),np.zeros([1,lstm_state_size]))

            c_input_state = tf.placeholder(shape=[1,lstm_state_size], dtype=tf.float32)
            h_input_state = tf.placeholder(shape=[1,lstm_state_size], dtype=tf.float32)
            self.input_state = tf.nn.rnn_cell.LSTMStateTuple(c_input_state,h_input_state)
            
            rnn_in = tf.expand_dims(self.fc1, [0])
            
            lstm_outputs, self.lstm_state = tf.nn.dynamic_rnn(cell=lstm_cell,
                                                              inputs=rnn_in,
                                                              initial_state=self.input_state,
                                                             )
            rnn_out = tf.reshape(lstm_outputs, [-1, lstm_state_size])
            
                        
            self.policy = tf.layers.dense(inputs=rnn_out,
                                          units=num_actions,
                                          activation=tf.nn.softmax)

network = AC_Network(state_size, num_actions, 'global')

saver = tf.train.Saver()

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())
saver.restore(sess, model_checkpoint)

env = gym.make('SpaceInvaders-v4')
initial_state = env.reset()
processed_state = helper.preprocess_frame(initial_state).reshape(1,-1)
input_state = processed_state
env.render()

current_lstm_states = network.initial_state
done = False
total_reward = 0
total_steps = 0

while done == False:
    
    actions, current_lstm_states = sess.run([network.policy,network.lstm_state],
                                            feed_dict={network.inputs:input_state,
                                                       network.input_state[0]:current_lstm_states[0],
                                                       network.input_state[1]:current_lstm_states[1]})
    
    unprocessed_state1, reward, done, info = env.step(np.argmax(actions))
    processed_state1 = helper.preprocess_frame(unprocessed_state1).reshape(1,-1)
    input_state = np.maximum(processed_state,processed_state1)
    
    env.render()

    processed_state = processed_state1
    
    total_reward += reward
    total_steps += 1
    time.sleep(args.gap)
    
print('\nsteps:',total_steps,'reward:',total_reward)