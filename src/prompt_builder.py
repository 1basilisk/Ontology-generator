def build_prompt(text_chunk, current_ontology_ttl):
    return f"""
You are an ontology engineer. Convert the following text into an OWL ontology fragment using Turtle syntax.

TEXT:
"{text_chunk}"

CURRENT ONTOLOGY:
{current_ontology_ttl}

TASK:
Your task is to generate a turtle fragment that represents the concepts, relationships, and properties described in the text. Ensure that the fragment is consistent with the current ontology.
Make sure to use appropriate prefixes and URIs for the ontology elements. The fragment should be valid Turtle syntax and should not include any extraneous information.
Return only the Turtle fragment without any additional explanations or comments. directly return the Turtle fragment as a string. do not use any markers like ```turtle or ```json etc.

here are some possible mistakes that you might make:
1- forgetting to add prefixes at the beginning of the code.
2- forgetting to write pivot classes at the beginning before starting to code.
3- your output would be concatenated to the previous output rdf, so don't write repetitive words, classes, or ...
4- in your output put all of the previous RDF classes, relations, and restrictions and add yours. your output will be passed to the next stage so don't remove previous code (it is going to replace the previous rdf)
5- you usually forget to write the name of the reification (pivot) that you want to create at the beginning of the output
6- In reification, the reification node (pivot class) is connected to all related classes by object properties, not by the subclassof. it can be a subclass of something, but for reification, it needs object properties.
common mistakes in extracting classes:
1- mistake: not extracting all classes and missing many of them. classes can be found in the story, or in the competency question number and restrictions.
2- Returning empty answer
3- Providing comments or explanations
4- Extracint classes like 'Date', and 'integer' are wrong since they are data properties.
5- not using RDF reification: not extracting pivot classes for modeling relation between classes (more than one class and one data property, or more than two classes)
6- extracting individuals in the text as a class
7- The pivot class is not a sublcass of its components.
common mistakes in the hierarchy extraction:
1- creating an ontology for non-existing classes: creating a new leaf and expanding it into the root
2- returning empty answer or very short
3- Providing comments or explanations
4- Extracting attributes such as date, time, and string names that are related to data properties
5- Forget to add "" around the strings in the tuples
Common mistakes in the object_properties:
1- returning new variables with anything except object_properties
2- returning empty answer or very short
3- providing comments or explanations
4- when the pivot class is created, all of the related classes should point to it (direction of relation is from the classes (domains) 'to'  pivot class (range))
Common mistakes in the data_properties:
1- returning new variables with anything except data_properties
2- returning empty answer or very short
3- providing comments or explanations


"""

