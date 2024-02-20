from bark.core.world.evaluation.ltl import EvaluatorLTL
from bark_ml.evaluators.stl.base_label_function import BaseQuantizedLabelFunction

class EvaluatorSTL(EvaluatorLTL):
    def __init__(self, agent_id: int, ltl_formula: str, 
                 label_functions, eval_return_without_robustness: bool = True):
        super().__init__(agent_id, ltl_formula, label_functions)
        self.robustness = float('inf')
        self.label_functions_stl = label_functions
        self.eval_return_without_robustness = eval_return_without_robustness

    def GetRuleViolationPenalty(self):
        robutness_val = self.ComputeRobustness()
        # print(f"Robustness in GetRuleViolationPenalty={robutness_val}")
        penalty = super().GetRuleViolationPenalty() - robutness_val
        return penalty

    def ComputeRobustness(self):
        self.robustness = float('inf')
        for le in self.label_functions:
            try:
                self.robustness = min(self.robustness, le.GetCurrentRobustness())
            except AttributeError as e:
                print(f"AttributeError: {e}")
                
        if self.robustness == float('inf') or self.robustness == float('-inf'):
           self.robustness = 0.0
        return self.robustness
    
    def Evaluate(self, observed_world):
        ltl_result = super().Evaluate(observed_world)
        double_value = float('inf')
        if isinstance(ltl_result, float):
            double_value = ltl_result
        else:
            print("EvaluatorLTL return in STL DOES NOT hold a double value.")

        robutness_val = self.ComputeRobustness()    
        if self.eval_return_without_robustness:
            return ltl_result
        else:            
            stl_result = str(double_value) + ";" + str(robutness_val)
            return stl_result