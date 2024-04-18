# Copyright (c) 2020 fortiss GmbH
#
# Authors: Patrick Hart, Julian Bernhard, Klemens Esterle, and
# Tobias Kessler
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from bark.runtime.viewer.matplotlib_viewer import MPViewer
from bark.runtime.scenario.scenario_generation.interaction_dataset_scenario_generation_full \
    import InteractionDatasetScenarioGenerationFull

from bark_ml.environments.blueprints.blueprint import Blueprint
from bark_ml.evaluators.evaluator_configs import GoalReached
from bark_ml.behaviors.discrete_behavior import *
from bark_ml.observers.nearest_state_observer import NearestAgentsObserver
from bark_ml.behaviors.cont_behavior import BehaviorContinuousML
from bark_ml.evaluators.general_evaluator import GeneralEvaluator

class InteractionDatasetScenarioFullBlueprint(Blueprint):
  """Blueprint using the Interaction dataset scenario (full) generation of BARK.
  """
  def __init__(self,
               params=None,
               ml_behavior=None,
               num_scenarios=1,
               viewer=True):
    # params["BehaviorIDMClassic"]["BrakeForLaneEnd"] = True
    # params["BehaviorIDMClassic"]["BrakeForLaneEndEnabledDistance"] = 100.
    # params["BehaviorIDMClassic"]["BrakeForLaneEndDistanceOffset"] = 30.
    # params["BehaviorIDMClassic"]["DesiredVelocity"] = 10.
    # params["World"]["remove_agents_out_of_map"] = False

    scenario_generation = InteractionDatasetScenarioGenerationFull(
      params=params, 
      num_scenarios=num_scenarios)
    print("InteractionDatasetScenarioFullBlueprint, num_scenarios::", num_scenarios)
    print("InteractionDatasetScenarioFullBlueprint, viewer::", viewer)

    if viewer:
      viewer = MPViewer(params=params,
                        x_range=[-150, 150],
                        y_range=[-150, 150],
                        follow_agent_id=True)
    dt = 0.2
    # NOTE: evaluator and observer could be overwritten
    evaluator = GeneralEvaluator(params)
    observer = NearestAgentsObserver(params)
    ml_behavior = ml_behavior
    print("InteractionDatasetScenarioFullBlueprint, ml_behavior::", ml_behavior)
    super().__init__(
      scenario_generation=scenario_generation,
      viewer=viewer,
      dt=dt,
      evaluator=evaluator,
      observer=observer,
      ml_behavior=ml_behavior)
    

class ContinuousInteractionDatasetScenarioFullBlueprint(InteractionDatasetScenarioFullBlueprint):
  """Blueprint using the Interaction dataset scenario (full) generation of BARK.
  """
  def __init__(self,
               params=None,
               ml_behavior=None,
               num_scenarios=1,
               viewer=True):
    print("ContinuousInteractionDatasetScenarioFullBlueprint, BEFORE ml_behavior::", ml_behavior)
    ml_behavior = BehaviorContinuousML(params)
    print("ContinuousInteractionDatasetScenarioFullBlueprint, AFTER ml_behavior::", ml_behavior)
    
    super().__init__(
      params=params,
      num_scenarios=num_scenarios,
      ml_behavior=ml_behavior,
      viewer=viewer)