from rdflib import Graph
from src.prompt_builder import build_validation_prompt, build_repair_fragment_prompt
from src.llm import run_llm
import logging

class OntologyBuilder:
    def __init__(self, base_uri):
        self.graph = Graph()
        self.base_uri = base_uri

    def merge_fragment(self, turtle_str):
        new_graph = Graph()
        try:
            
            new_graph.parse(data=turtle_str, format='turtle')
            
        
        except Exception as e:
            print(f"Syntax error in fragment, attempting repair: {e}")
            logging.error(f"Syntax error in fragment, attempting repair\n")
            prompt = build_repair_fragment_prompt(turtle_str)
            repaired = run_llm(prompt)
            try:
                new_graph.parse(data=repaired, format='turtle')
                
                print("Fragment repaired and merged successfully.")
                logging.info("Fragment repaired and merged successfully.\n")
               
            except Exception as e2:
                print(f"Repair failed: {e2}")
                logging.error(f"Failed to repair fragment, skipping")

                return False
            
        # conflicts = []
        # triples_to_add = []
        # for s, p, o in new_graph:
        #     existing_objects = set(self.graph.objects(s, p))
        #     if existing_objects and o not in existing_objects:
        #         conflicts.append((s, p, existing_objects, o))
        #     else:
        #         triples_to_add.append((s, p, o))

        # # Log conflicts
        # if conflicts:
        #     logging.warning("Conflicts detected during merge:")
        #     for s, p, existing_objs, new_obj in conflicts:
        #         logging.warning(f"  {s} {p} already has {existing_objs}, new: {new_obj}")

        # # Add non-conflicting triples
        # for triple in triples_to_add:
        #     self.graph.add(triple)
        self.graph += new_graph
        print("Fragment merged successfully.")
        return True

    def get_current_ontology_ttl(self):
        return self.graph.serialize(format='turtle')

    def save_to_file(self, filepath):
        self.graph.serialize(destination=filepath, format='turtle')
        print(f"Ontology saved to {filepath}")

    def clear_current_ontology(self):
        self.graph = Graph()

    def validate_ontology_llm(self):
        c = self.get_current_ontology_ttl()
        prompt = build_validation_prompt(c)
        
        ontology = run_llm(prompt)
        if ontology:
            new_graph = Graph()
            try:
                new_graph.parse(data=ontology, format='turtle')
                self.graph = new_graph
                return True
            except Exception as e:
                print(f"Error parsing ontology: {e}")
                return False



