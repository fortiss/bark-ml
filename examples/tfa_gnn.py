# Copyright (c) 2020 Patrick Hart, Julian Bernhard,
# Klemens Esterle, Tobias Kessler
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# TensorFlow Agents (https://github.com/tensorflow/agents) example
import gym
from absl import app
from absl import flags
import tensorflow as tf

# this will disable all BARK log messages
# import os
# os.environ['GLOG_minloglevel'] = '3' 

# BARK imports
from bark.runtime.commons.parameters import ParameterServer
from bark.runtime.viewer.matplotlib_viewer import MPViewer
from bark.runtime.viewer.video_renderer import VideoRenderer

# BARK-ML imports
from bark_ml.environments.blueprints import ContinuousHighwayBlueprint, ContinuousMergingBlueprint
from bark_ml.environments.single_agent_runtime import SingleAgentRuntime
from bark_ml.library_wrappers.lib_tf_agents.agents import BehaviorGraphSACAgent
from bark_ml.library_wrappers.lib_tf_agents.runners import SACRunner
from bark_ml.observers.graph_observer import GraphObserver
from bark_ml.library_wrappers.lib_tf_agents.networks.gnn_wrapper import GNNWrapper


# for training: bazel run //examples:tfa -- --mode=train
FLAGS = flags.FLAGS
flags.DEFINE_enum("mode",
                  "visualize",
                  ["train", "visualize", "evaluate"],
                  "Mode the configuration should be executed in.")

def run_configuration(argv):
  # File with standard parameters for spektral use:
  #filename = "examples/example_params/tfa_sac_gnn_spektral_default.json"
  # File with standard parameters for tf2_gnn use:
  filename = "examples/example_params/tfa_sac_gnn_tf2_gnn_default.json"
  params = ParameterServer(filename=filename)

  #viewer = MPViewer(
  #  params=params,
  #  x_range=[-35, 35],
  #  y_range=[-35, 35],
  #  follow_agent_id=True)
  
  #viewer = VideoRenderer(
  #  renderer=viewer,
  #  world_step_time=0.2,
  #  fig_path="/home/silvan/working_bark/training/video/")

  # create environment
  bp = ContinuousHighwayBlueprint(params,
                                  number_of_senarios=2500,
                                  random_seed=0)

  observer = GraphObserver(params=params)
  
  env = SingleAgentRuntime(
    blueprint=bp,
    observer=observer,
    render=False)

  sac_agent = BehaviorGraphSACAgent(environment=env,
                                    observer=observer,
                                    params=params)
  env.ml_behavior = sac_agent
  runner = SACRunner(params=params,
                     environment=env,
                     agent=sac_agent)
  runner.SetupSummaryWriter()

  if FLAGS.mode == "train":
    runner.Train()
  elif FLAGS.mode == "visualize":
    runner.Visualize(5)
  elif FLAGS.mode == "evaluate":
    runner.Evaluate()
  
  # store all used params of the training
  #params.Save("/home/silvan/working_bark/examples/example_params/tfa_sac_gnn_spektral_default.json")

if __name__ == '__main__':
  app.run(run_configuration)
