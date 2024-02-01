import pandas as pd
from tf.app import use
from seaborn import displot


class NEA():
    """
    Initializes the Named Entity Analyzer object that is used to analyze and visualize named entities.

    Currently only able to accept a string for the creation a new object. Every new string needs a new object.
    Will get expanded functionality in the future.
    """

    def __init__(self, input_string: str, text_fabric: object, F: object) -> None:
        """
        Needs an input as a string. Will be checked if it is a valid named entity.
        TODO add entityKind optional parameter and check
        """

        self.text_fabric = text_fabric
        self.named_entity = input_string
        self.named_entity_tuple = self.get_named_entity(input_string)
        if not self.named_entity_tuple:
            print("Entity does not exist in this corpus")
        else:
            print("Succes!")

        self.pd_data_frame = self.build_data_frame()

        # TODO tmp solution
        self.years = [F.year.v(node[0]) for node in self.named_entity_tuple]
    
    def get_named_entity(self, input_string) -> tuple[tuple[int]]:

        # A = use("CLARIAH/wp6-missieven", version="1.0",
        #         mod="CLARIAH/wp6-missieven/voc-missives/export/tf", hoist=globals())
        
        query = f"""
letter
    word trans~{input_string} entityId entityKind*
        """

        return self.text_fabric.search(query)
    
    def build_data_frame(self) -> pd.DataFrame:
        """
        Fills a panda's dataframe with information
        TODO specify this more
        """
        pass


    def draw_plot(self) -> None:
        """
        Draws a displot in Jupyter Notebooks of the occurences by date.
        """

        displot(data=self.years)

    def print_info(self) -> None:
        print(self.named_entity_tuple)