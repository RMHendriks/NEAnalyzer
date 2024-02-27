

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

        named_entity_list = [ne for ne in F.otype.s("word") if F.entityId.v(ne) is not None]

        
        print(len(named_entity_list))

        for i, entity in enumerate(named_entity_list):
            if i > 9950 and i < 10000:
                print(T.text(entity), F.entityId.v(entity))

        # TODO named entities got a entityId I can use to combine
        # multi word named entities into one (maybe do this in the
        # original loop by appending previous words with the same id
        # to each other)
                
        # TODO group the named entities together
                
    def export_to_file(self) -> None:
        """
        TODO Export the named entities groupings into a file.
        """
        
        pass