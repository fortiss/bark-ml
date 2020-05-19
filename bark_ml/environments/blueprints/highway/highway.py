# Copyright (c) 2020 Patrick Hart, Julian Bernhard,
# Klemens Esterle, Tobias Kessler
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from bark_project.modules.runtime.commons.parameters import ParameterServer
from bark_project.modules.runtime.viewer.matplotlib_viewer import MPViewer
from bark_project.modules.runtime.scenario.scenario_generation.config_with_ease import \
  LaneCorridorConfig, ConfigWithEase
from bark.models.dynamic import SingleTrackModel
from bark.world.opendrive import XodrDrivingDirection
from bark.world.goal_definition import GoalDefinitionStateLimitsFrenet

from bark_ml.environments.blueprints.blueprint import Blueprint
from bark_ml.evaluators.goal_reached import GoalReached
from bark_ml.observers.nearest_state_observer import NearestAgentsObserver
from bark_ml.behaviors.cont_behavior import BehaviorContinuousML
from bark_ml.behaviors.discrete_behavior import BehaviorDiscreteML


class HighwayLaneCorridorConfig(LaneCorridorConfig):
  def __init__(self,
               params=None,
               **kwargs):
    super(HighwayLaneCorridorConfig, self).__init__(params, **kwargs)
  
  def goal(self, world):
    road_corr = world.map.GetRoadCorridor(
      self._road_ids, XodrDrivingDirection.forward)
    lane_corr = self._road_corridor.lane_corridors[0]
    return GoalDefinitionStateLimitsFrenet(lane_corr.center_line,
                                           (0.4, 0.4),
                                           (0.1, 0.1),
                                           (25., 35.))


class HighwayBlueprint(Blueprint):
  def __init__(self,
               params=None,
               number_of_senarios=250,
               random_seed=0,
               ml_behavior=None):

    params["BehaviorIDMClassic"]["DesiredVelocity"] = 30.
    left_lane = HighwayLaneCorridorConfig(params=params,
                                          road_ids=[16],
                                          lane_corridor_id=0,
                                          min_vel=25.0,
                                          max_vel=30.0,
                                          controlled_ids=None)
    right_lane = HighwayLaneCorridorConfig(params=params,
                                           road_ids=[16],
                                           lane_corridor_id=1,
                                           min_vel=25.0,
                                           max_vel=30.0,
                                           controlled_ids=True)
    scenario_generation = \
      ConfigWithEase(
        num_scenarios=number_of_senarios,
        map_file_name="bark_ml/environments/blueprints/highway/city_highway_straight.xodr",  # NOLINT
        random_seed=random_seed,
        params=params,
        lane_corridor_configs=[left_lane, right_lane])
    viewer = MPViewer(params=params,
                      x_range=[-35, 35],
                      y_range=[-35, 35],
                      follow_agent_id=True)
    dt = 0.2
    evaluator = GoalReached(params)
    observer = NearestAgentsObserver(params)
    ml_behavior = ml_behavior

    super().__init__(
      scenario_generation=scenario_generation,
      viewer=viewer,
      dt=dt,
      evaluator=evaluator,
      observer=observer,
      ml_behavior=ml_behavior)


class ContinuousHighwayBlueprint(HighwayBlueprint):
  def __init__(self,
               params=None,
               number_of_senarios=25,
               random_seed=0):
    ml_behavior = BehaviorContinuousML(params)
    HighwayBlueprint.__init__(self,
                              params=params,
                              number_of_senarios=number_of_senarios,
                              random_seed=random_seed,
                              ml_behavior=ml_behavior)


class DiscreteHighwayBlueprint(HighwayBlueprint):
  def __init__(self,
               params=None,
               number_of_senarios=25,
               random_seed=0):
    dynamic_model = SingleTrackModel(params)
    ml_behavior = BehaviorDiscreteML(dynamic_model, params)
    HighwayBlueprint.__init__(self,
                              params=params,
                              number_of_senarios=number_of_senarios,
                              random_seed=random_seed,
                              ml_behavior=ml_behavior)