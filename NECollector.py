from typing import Tuple, List, Dict
from igraph import bipartite

class NECollector():
    """
    Tool that collects all the named entities in a corpus and groups
    them together.
    TODO Final version should output a file with the named entity groupings
    """

    def __init__(self, A: object, F: object, T: object, L: object) -> None:
        """"
        Initializes the class and groups all named entities in a corpus.
        Needs an advanced Text-Fabric API as input to access the corpus. 
        """

        self.A = A
        self.F = F
        self.T = T
        self.L = L

        # make a list of all named entities and group multi word named entities together
        self.named_entity_list: List[List[int]] = []
        entity_id = ""

        for ne in F.otype.s("word"):
            if entity_id == F.entityId.v(ne):
                self.named_entity_list[-1].append(ne)
            elif F.entityId.v(ne) is not None:
                self.named_entity_list.append([ne])
                entity_id = F.entityId.v(ne)

        # create a stripped lowercase key from the node text and combine equal
        # named entities together in a dict
        self.named_entity_dict: Dict[str, List[int]] = {}

        for node_list in self.named_entity_list:
            ne_str = self.get_grouped_ne_str(node_list)
            self.named_entity_dict.setdefault(ne_str, []).append(node_list)

        # build the named entity by letter dict
        self.named_entity_letter_dict = self.build_named_entity_letter_dict()
                
        print("Finished building the Named Entity dictionary")
    
    def get_grouped_ne_str(self, node_list: List[int]) -> str:
        """
        Creates a concatenated lowercase str as a key 'hash' for a dictionary
        - Needs a list of word nodes as intergers

        Returns a str
        """

        stripped_node_list = []
        for node in node_list:
            stripped_node_str = "".join(e for e in self.T.text(node) if e.isalnum())
            stripped_node_list.append(stripped_node_str)

        ne_str = "".join(node + "." for node in stripped_node_list)
        ne_str = ne_str.lower()
        if ne_str.endswith('.'):
            ne_str = ne_str[:-1]

        return ne_str

    def build_named_entity_letter_dict(self) -> Dict[int, List[int]]:
        """
        Builds a dictionary of letters as keys and named entities as values
        """

        # TODO make a dictionary with letters as keys and their named entities as values
        named_entity_letter_dict: Dict[int, List[int]] = {}

        for ne_list in self.named_entity_dict.values():
            for word_node_list in ne_list:
                letter = self.L.u(word_node_list[0], otype="letter")[0]
                named_entity_letter_dict.setdefault(letter, []).append(word_node_list)

        return named_entity_letter_dict

    def match_named_entities_by_letter(self) -> None:
        """
        Creates a dataset of all matches that occur in the letters.
        """

        # TODO count the amount of overlap between two named entities on a letter by letter basis
        # TODO learn to use the bipartite graph from igraph

        pass

                
    def export_to_file(self) -> None:
        """
        TODO Export the named entities groupings into a file.
        """
        
        pass