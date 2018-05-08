# Reinforcement Learning 101

An example of an A3C model playing [Atari Space Invaders](https://gym.openai.com/envs/SpaceInvaders-v0/) using Tensorflow.

These notebooks are designed for a workshop and to work inside [google colaboratory](https://colab.research.google.com).

#### Documented notebooks:
- A3C_workshop_part1.ipynb will load a model from a checkpoint, then run and display it playing a game
    - the documentation will teach the NN structure and RL basics (eg. environments, agents, rewards)
- A3C_workshop_part2.ipynb will train a model, saving checkpoints and logging to tensorboard
    - the documentation will teach how updating the model works and more about RL
   
### Instructions for running:
1. Download or clone the repository
    - if you downloaded the ZIP, extract on your local machine
2. Go to google drive, and upload this folder from your local machine
3. From Drive, open a notebook with Colaboratory (double-click then choose Connected apps Colaboratory)
    - If Colaboratory is not shown, you'll have to first add it from Open With, then search Colab, then connect.
    - https://colab.research.google.com
4. Select runtime, change runtime type, and set hardware accelerator to GPU
    - if it doesn't let you, that's fine (it'll just be a bit slower)
    - if are using the GPU on the Conv examples, the GPU may run out of memory so you'll have to use CPU
5. if you dont have any model checkpoints, you will have to run A3C_workshop_part2.ipynb first
    - colab isn't optimal to train as the vm stops at 12 hours
    - it's also hard to get the checkpoints off into your local machine or drive
    - if you're are taking part in my workshop, I will provide checkpoints from a training session I did locally
