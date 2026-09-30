from core.models import GrafcetSystem

class AWLTranslator:
    """Translates mathematical Boolean equations into Siemens STEP 7 / TIA Portal AWL (STL) code."""
    
    def __init__(self, system: GrafcetSystem):
        self.system = system

    def generate_source_code(self) -> str:
        """Generates the full .awl source file content compatible with Siemens PLCs."""
        awl_code = [
            "FUNCTION_BLOCK FB_LOGISTEP_SEQ",
            "TITLE = 'Auto-Generated GRAFCET System Logic'",
            "AUTHOR : 'LogiStep'",
            "VERSION : 1.0",
            ""
        ]
        
        for step in self.system.steps:
            step_id = step.step_id
            
            awl_code.append("NETWORK")
            awl_code.append(f"TITLE = Step {step_id} (State and Actions)")
            
            # Recherche des transitions entrantes (Activation)
            ac_transitions = [t for t in self.system.transitions if t.to_step == step_id]
            # Recherche des transitions sortantes (Désactivation)
            dc_transitions = [t for t in self.system.transitions if t.from_step == step_id]
            
            if step.is_initial:
                # Injection de l'impulsion de démarrage (First Scan) pour les automates
                awl_code.append(f"      // Initial Step Startup Logic")
                awl_code.append(f"      A     \"First_Scan_Bit\"")
                awl_code.append(f"      S     \"{step_id}\"")
                awl_code.append(f"      // Standard Cyclic Logic")

           # 1. Condition d'activation (Gestion des convergences et de la logique ET/OU)
            if ac_transitions:
                # S'il y a plusieurs transitions entrantes, on ouvre une parenthèse globale
                if len(ac_transitions) > 1:
                    awl_code.append(f"      O(")
                    
                for idx, t in enumerate(ac_transitions):
                    if len(ac_transitions) > 1 and idx > 0:
                        awl_code.append(f"      ) ")
                        awl_code.append(f"      O(")
                        
                    awl_code.append(f"      A     \"{t.from_step}\"")
                    
                    condition_string = t.condition 
                    if " OR " in condition_string:
                        sub_conditions = [c.strip() for c in condition_string.split(" OR ")]
                        awl_code.append(f"      A(")
                        for i, sub_c in enumerate(sub_conditions):
                            instruction = "O" if i > 0 else "A"
                            awl_code.append(f"      {instruction}     \"{sub_c}\"")
                        awl_code.append(f"      )")
                    else:
                        sub_conditions = [c.strip() for c in condition_string.split(" AND ")]
                        for sub_c in sub_conditions:
                            awl_code.append(f"      A     \"{sub_c}\"")
                            
                if len(ac_transitions) > 1:
                    awl_code.append(f"      )")
            
            # 2. Auto-maintien
            awl_code.append(f"      O     \"{step_id}\"")
            
            # 3. Condition de désactivation
            for t in dc_transitions:
                awl_code.append(f"      AN    \"{t.to_step}\"")
                
            # 4. Affectation de l'état
            awl_code.append(f"      =     \"{step_id}\"")

           # 5. Gestion des actions physiques simultanées
            if step.action:
                # Sépare la chaîne de caractères par les virgules et enlève les espaces
                actions_list = [act.strip() for act in step.action.split(',')]
                
                for act in actions_list:
                    if act:  # Vérifie que l'action n'est pas vide
                        awl_code.append(f"      A     \"{step_id}\"")
                        awl_code.append(f"      =     \"{act}\"")
                
            awl_code.append("")
            
        awl_code.append("END_FUNCTION_BLOCK")
        
        return "\n".join(awl_code)