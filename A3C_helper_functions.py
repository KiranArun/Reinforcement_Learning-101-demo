import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import scipy.signal
import cv2,time,gym,os,sys
from matplotlib import rc, animation
from google.colab import files


# helper function to get name of logdir
# model logdir will be similar to 'run_01-lr_1e-5-nw_16-tmax_50'
def get_logdir(model_logdir,learning_rate,num_workers,tmax):
    
    hparam_str = '-lr_'+str(learning_rate)+'-nw_'+str(num_workers)+'-tmax_'+str(tmax)
    previous_runs = list(f for f in os.listdir(model_logdir) if f.startswith('run'))

    if len(previous_runs) == 0:
        run_number = 1  
    else:
        run_number = max([int(s[4:6]) for s in previous_runs]) + 1

    run_logdir = '%srun_%02d' % (model_logdir, run_number)+hparam_str
    return(run_logdir)

# reshape frame to 84x84
# converts to binary image (threshold = 1)
def preprocess_frame(image):
    observation = cv2.resize(image, (84, 90))
    observation = cv2.cvtColor(observation, cv2.COLOR_BGR2GRAY)
    observation = observation[:84,:]
    ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
    observation = observation*(1.0/255.0)
    return(observation)

# weights initializer for policy and value layers
# normalized coloumns from a standard normal
def weight_initializer(std=1.0):
    def _initializer(shape, dtype=None, partition_info=None):
        out = np.random.randn(*shape).astype(np.float32)
        out *= std / np.sqrt(np.square(out).sum(axis=0, keepdims=True))
        return(tf.constant(out))
    return(_initializer)

# at the end of each worker training episode
# update any variables and show stats
# also add summaries to tensorboard
def end_training_episode(episode_history,episodes_history,worker_episode_count,worker_name,saver,sess,run_logdir,writer):
    
    episode_history_array = np.asarray(episode_history)
    episode_reward = np.sum(episode_history_array[:,2])
    episode_actions = np.zeros(6)
    
    for action in episode_history_array[:,1]:
        episode_actions[action] += 1
        
    # show episode stats
    if worker_episode_count % 10 == 0:
        print(str(worker_name), ': ',
              'episode:', worker_episode_count,
              'reward:', episode_reward,
              'actions:', np.round(100*episode_actions/episode_history_array[:,0].size,0))
                    
    worker_episode_count += 1
    episodes_history = np.append(episodes_history, [[episode_history_array[:,0].size,episode_reward]], axis=0)
                
    if str(worker_name) == 'worker_0' and worker_episode_count % 250 == 0:
        saver.save(sess, os.path.join(run_logdir, "model.ckpt"), worker_episode_count)
        print('Saved model, checkpoint:', worker_episode_count)
        
    summary = tf.Summary()
    summary.value.add(tag='episode_steps',simple_value=int(episodes_history[-1,0]))
    summary.value.add(tag='episode_reward',simple_value=int(episodes_history[-1,1]))
    writer.add_summary(summary, worker_episode_count)
    writer.flush()
    
    return(episodes_history,worker_episode_count)

# run 1 episode with the global network and return num steps and total reward
def test(sess,network):
    env = gym.make('SpaceInvaders-v4')
    init_frame = env.reset()
    raw_s = preprocess_frame(init_frame).reshape(1,-1)
    s = raw_s
    current_lstm_states = network.initial_state
    d = False
    total_reward = 0
    total_steps = 0
    while d == False:
        actions, current_lstm_states = sess.run([network.policy,network.lstm_state],
                                                   feed_dict={network.inputs:s,
                                                      network.input_state[0]:current_lstm_states[0],
                                                      network.input_state[1]:current_lstm_states[1]})

        raw_s1, r, d, info = env.step(np.argmax(actions))
        raw_s1 = preprocess_frame(raw_s1).reshape(1,-1)
        s = np.maximum(raw_s,raw_s1)
        raw_s = raw_s1
        total_reward += r
        total_steps += 1
    return(total_steps,total_reward)

# run 1 episode with the global network and plot the frames
def display_test(sess,network):
    env = gym.make('SpaceInvaders-v4')
    init_frame = env.reset()
    raw_s = preprocess_frame(init_frame).reshape(1,-1)
    s = raw_s
    unprocessed_s = init_frame
    current_lstm_states = network.initial_state
    d = False
    total_reward = 0
    total_steps = 0
    frames = np.expand_dims(unprocessed_s,axis=0)

    while d == False:

        if total_steps % 20 == 0:
            sys.stdout.write('\r'+str(total_steps)+' frames')
            sys.stdout.flush()

        actions, current_lstm_states = sess.run([network.policy,network.lstm_state],
                                                   feed_dict={network.inputs:s,
                                                          network.input_state[0]:current_lstm_states[0],
                                                          network.input_state[1]:current_lstm_states[1]})
        
        unprocessed_s1, r, d, info = env.step(np.argmax(actions))
        raw_s1 = preprocess_frame(unprocessed_s1).reshape(1,-1)
        s = np.maximum(raw_s,raw_s1)
        
        frames = np.append(frames,np.expand_dims(np.maximum(unprocessed_s,unprocessed_s1),axis=0),axis=0)

        raw_s = raw_s1
        unprocessed_s = unprocessed_s1
        total_reward += r
        total_steps += 1

    print('Steps:',total_steps,'Reward:',total_reward)

    return(frames)
    
def Display_example_frames(fig,ax):
    
    env = gym.make('SpaceInvaders-v4')
    _ = env.reset()

    for i in range(100):
        raw_frame,_,_,_ = env.step(env.action_space.sample())

    for axes in ax:
        axes.grid(False)

    ax[0].imshow(raw_frame)
    ax[1].imshow(preprocess_frame(raw_frame),cmap='binary')

    ax[0].set_title('Raw Frame (this is what the environment outputs)')
    ax[1].set_title('Processed Frame (this is what we input to our neural net)')


def create_gameplay_video(frames,figsize,save=False):
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(False)
    ax.axis('off')

    frame = ax.imshow(frames[0])

    def init():
      frame.set_data(frames[0])
      return(frame,)

    def animate(i):
        
      frame.set_data(frames[i])
      return(frame,)

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=frames.shape[0], interval=70, 
                                   blit=True)

    if save == True:
        rc('animation', embed_limit=20)
        anim.save('video.mp4', writer="ffmpeg")
        files.download('video.mp4')

    return(anim)