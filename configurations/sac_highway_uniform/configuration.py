import os
import matplotlib as mpl
if os.environ.get('DISPLAY') == ':0':
  print('No display found. Using non-interactive Agg backend')
  mpl.use('Agg')

from absl import app
from absl import flags
import tensorflow as tf
from tf_agents.environments import tf_py_environment

from modules.runtime.scenario.scenario_generation.uniform_vehicle_distribution \
  import UniformVehicleDistribution
from modules.runtime.scenario.scenario_generation.deterministic \
  import DeterministicScenarioGeneration
from modules.runtime.commons.parameters import ParameterServer
from modules.runtime.viewer.matplotlib_viewer import MPViewer
from modules.runtime.viewer.video_renderer import VideoRenderer


from src.rl_runtime import RuntimeRL
from src.observers.nearest_state_observer import ClosestAgentsObserver
from src.wrappers.dynamic_model import DynamicModel
from src.wrappers.tfa_wrapper import TFAWrapper
from src.evaluators.goal_reached import GoalReached
from src.agents.sac_agent import SACAgent
from src.runners.sac_runner import SACRunner
from configurations.base_configuration import BaseConfiguration

# configuration specific evaluator
from configurations.sac_highway_uniform.custom_evaluator import CustomEvaluator

FLAGS = flags.FLAGS
flags.DEFINE_enum('mode',
                  'train',
                  ['train', 'visualize', 'evaluate'],
                  'Mode the configuration should be executed in.')
flags.DEFINE_string('base_dir',
                    os.path.dirname(
                      os.path.dirname(os.path.dirname(__file__))),
                    'Base directory of bark-ml.')


class SACHighwayConfiguration(BaseConfiguration):
  """Hermetic and reproducible configuration class
  """
  def __init__(self,
               params):
    BaseConfiguration.__init__(
      self,
      params)

  def _build_configuration(self):
    """Builds a configuration using an SAC agent
    """
    self._scenario_generator = \
      UniformVehicleDistribution(num_scenarios=20,
                                 random_seed=0,
                                 params=self._params)
    self._observer = ClosestAgentsObserver(params=self._params)
    self._behavior_model = DynamicModel(params=self._params)
    self._evaluator = CustomEvaluator(params=self._params)

    self._viewer  = MPViewer(params=self._params,
                             use_world_bounds=True)
                            # x_range=[-20,20],
                            # y_range=[-20,20],
                            # follow_agent_id=True)
    #self._viewer = VideoRenderer(renderer=viewer, world_step_time=0.2)
    self._runtime = RuntimeRL(action_wrapper=self._behavior_model,
                              observer=self._observer,
                              evaluator=self._evaluator,
                              step_time=0.2,
                              viewer=self._viewer,
                              scenario_generator=self._scenario_generator)

    tfa_env = tf_py_environment.TFPyEnvironment(TFAWrapper(self._runtime))
    self._agent = SACAgent(tfa_env, params=self._params)
    self._runner = SACRunner(tfa_env,
                             self._agent,
                             params=self._params,
                             unwrapped_runtime=self._runtime)

def run_configuration(argv):
  params = ParameterServer(filename=FLAGS.base_dir + "/configurations/sac_highway_uniform/config.json")
  scenario_generation = params["Scenario"]["Generation"]["UniformVehicleDistribution"]
  map_filename = scenario_generation["MapFilename"]
  scenario_generation["MapFilename"] = FLAGS.base_dir + "/" + map_filename
  params["BaseDir"] = FLAGS.base_dir
  configuration = SACHighwayConfiguration(params)
  
  if FLAGS.mode == 'train':
    configuration.train()
  elif FLAGS.mode == 'visualize':
    configuration.visualize(10)
    # configuration._viewer.export_video("/home/hart/Dokumente/2019/bark-ml/configurations/sac_highway_uniform/video/lane_merge")
  elif FLAGS.mode == 'evaluate':
    configuration.evaluate()

if __name__ == '__main__':
  app.run(run_configuration)