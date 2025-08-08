from rdflib import Graph

class OntologyBuilder:
    def __init__(self, base_uri):
        self.graph = Graph()
        self.base_uri = base_uri

    def merge_fragment(self, turtle_str):
        new_graph = Graph()
        try:
            
            new_graph.parse(data=turtle_str, format='turtle')
            self.graph += new_graph
        except Exception as e:
            print(f"Error parsing fragment: {e}")

    def get_current_ontology_ttl(self):
        return self.graph.serialize(format='turtle')

    def save_to_file(self, filepath):
        self.graph.serialize(destination=filepath, format='turtle')
        print(f"Ontology saved to {filepath}")