# core/analyzer.py
from core.models import GrafcetSystem

class SystemAnalyzer:
    """Analytical engine for GRAFCET mathematical system transformations."""
    
    def __init__(self, system: GrafcetSystem):
        self.system = system

    def extract_boolean_equations(self) -> dict:
        """
        Iterates through the system graph to generate Boolean logic equations.
        Returns a dictionary containing AC and DC equations for each step.
        """
        equations = {}
        
        for step in self.system.steps:
            ac_terms = []
            dc_terms = []
            
            # 1. Activation Equation (AC) : Upstream Step AND Receptivity Condition
            for transition in self.system.transitions:
                if transition.to_step == step.step_id:
                    # Mathematical logic: X_{upstream} * Condition
                    ac_terms.append(f"({transition.from_step} AND {transition.condition})")
            
            # 2. Deactivation Equation (DC) : Downstream Steps
            for transition in self.system.transitions:
                if transition.from_step == step.step_id:
                    # Mathematical logic: Sum of X_{downstream}
                    dc_terms.append(transition.to_step)
            
            # Formatting the boolean expressions
            ac_equation = " OR ".join(ac_terms) if ac_terms else "None (Initial Step Logic)"
            dc_equation = " OR ".join(dc_terms) if dc_terms else "None (End of Sequence)"
            
            equations[step.step_id] = {
                "Activation_AC": ac_equation,
                "Deactivation_DC": dc_equation
            }
            
        return equations