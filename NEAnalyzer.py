import pandas as pd
import matplotlib.pyplot as plt
from seaborn import displot


class NEA():
    """
    Initializes the Named Entity Analyzer object that is used to analyze and visualize named entities.

    Currently only able to accept a string for the creation a new object. Every new string needs a new object.
    Will get expanded functionality in the future.

    TODO Find a design that makes it possible to insert multiple strings for comparisons
    """

    def __init__(self, input_string: str, text_fabric: object, F: object, T: object) -> None:
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

        # TODO tmp solution
        self.F = F
        self.T = T

        self.pd_data_frame = self.build_data_frame()
    
    def get_named_entity(self, input_string) -> list[tuple[int]]:
        """
        Gets the named entity from a query search of the corpus.
        
        Returns a list of tuples with nodes as Int.
        """

        query = f"""
letter
    word trans~{input_string} entityId entityKind*
        """

        return self.text_fabric.search(query)
    
    def build_data_frame(self) -> pd.DataFrame:
        """
        Fills a panda's dataframe with information
        - Node as an Int
        - Name name as a Str
        - Letter year as a Str
        - Letter month as a Str
        - Letter day as a Str
        - Letter title as a Str

        Returns a Panda's Dataframe with these as columns and the nodes as rows.
        TODO specify this more and expand the data being extracted
        """
        named_entity_dict = {"Node": [],
                             "Name": [],
                             "Year": [],
                             "Month": [],
                             "Day": [],
                             "Letter": []}

        for letter, node in self.named_entity_tuple:
            named_entity_dict["Node"].append(node)
            named_entity_dict["Name"].append(self.T.text(node))
            named_entity_dict["Year"].append(self.F.year.v(letter))
            named_entity_dict["Month"].append(self.F.month.v(letter))
            named_entity_dict["Day"].append(self.F.day.v(letter))
            named_entity_dict["Letter"].append(self.F.title.v(letter))

        return pd.DataFrame(named_entity_dict)

    def draw_plot(self, use_fixed_x=False) -> None:
        """
        Draws a displot in Jupyter Notebooks of the occurences by date.
        TODO Add an option to use a fixed x range
        """

        FIXED_X_AXIS = (1610, 1767)

        if use_fixed_x:
            displot(data=self.pd_data_frame["Year"])
            plt.xlim(FIXED_X_AXIS)
        else:
            displot(data=self.pd_data_frame["Year"])

        plt.show()

    def print_info(self) -> None:
        """ Prints the data in the Jupyter Notebook.
        TODO Greatly expand the data shown and functionality (Ask supervisor for advice)
        """

        print(self.pd_data_frame)