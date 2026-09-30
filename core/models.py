from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Step:
    """Représente une étape du GRAFCET (Nœud du système)."""
    step_id: str
    is_initial: bool = False
    action: Optional[str] = None

@dataclass
class Transition:
    """Représente une transition (Arc directionnel et condition de réceptivité)."""
    transition_id: str
    from_step: str
    to_step: str
    condition: str

@dataclass
class GrafcetSystem:
    """Encapsule le système complet et prépare le terrain pour l'analyse mathématique."""
    steps: List[Step] = field(default_factory=list)
    transitions: List[Transition] = field(default_factory=list)

    def add_step(self, step_id: str, is_initial: bool = False, action: str = None):
        self.steps.append(Step(step_id=step_id, is_initial=is_initial, action=action))

    def add_transition(self, transition_id: str, from_step: str, to_step: str, condition: str):
        self.transitions.append(Transition(transition_id=transition_id, from_step=from_step, to_step=to_step, condition=condition))
        
    def get_step_by_id(self, step_id: str) -> Optional[Step]:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None