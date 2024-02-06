import pandas as pd
import matplotlib.pyplot as plt
from seaborn import displot, barplot
from typing import Union


class NEA():
    """
    Initializes the Named Entity Analyzer object that is used to analyze and visualize named entities.

    Currently only able to accept a string for the creation a new object. Every new string needs a new object.
    Will get expanded functionality in the future.

    TODO Find a design that makes it possible to insert multiple strings for comparisons
    """

    def __init__(self, input_list: Union[list[str], list[int]],
                 A: object, F: object, T: object, L: object) -> None:
        """
        Needs an input as a list with strings or intergers (nodes). Will be checked if it is a valid named entity.
        TODO add entityKind optional parameter and check
        """

        self.A = A
        self.named_entity = input_list
        self.named_entity_list = self.get_named_entity(input_list)

        if not self.named_entity_list:
            print("Entity list is empty")
        else:
            print("Succes!")

        # TODO tmp solution
        self.F = F
        self.T = T
        self.L = L

        self.pd_data_frame = self.build_data_frame()
    
    def get_named_entity(self, input_list) -> list[list[tuple[int]]]:
        """
        Gets the named entity from a query search of the corpus.
        
        Returns a list of tuples with nodes as Int.
        """

        node_list: list[list[tuple[int]]] = []

        # convert a str list
        if input_list and all(isinstance(s, str) for s in input_list):

            for s in input_list:
                query = f"""
letter
    word trans~{s} entityId entityKind*
        """
                result = self.A.search(query)
                if not result:
                    print(f"\"{s}\" does not exist as a named entity")
                else:
                    node_list.append(result)

        # convert an int (node) list
        # TODO node inputs need more checks if valid
        elif input_list and all(isinstance(i, int) for i in input_list):
            for i in node_list:
                if self.F.entityId.v(i) is not None:
                    letter = self.L.u(i, otype="letter")
                    self.node_list.append([i, letter])
        
        else:
            print("Input list is not valid")
        
        
        return node_list
    
    def build_data_frame(self) -> list[pd.DataFrame]:
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
        TODO add entityKind 
        """
        data_frame_list: list[pd.DataFrame] = []

        for named_entity in self.named_entity_list:
            named_entity_dict = {"Node": [],
                                "Name": [],
                                "Year": [],
                                "Month": [],
                                "Day": [],
                                "EntityKind": [],
                                "EntityId":  [],
                                "Letter": []}

            for letter, node in named_entity:
                named_entity_dict["Node"].append(node)
                named_entity_dict["Name"].append(self.T.text(node))
                named_entity_dict["Year"].append(self.F.year.v(letter))
                named_entity_dict["Month"].append(self.F.month.v(letter))
                named_entity_dict["Day"].append(self.F.day.v(letter))
                named_entity_dict["EntityKind"].append(self.F.entityKind.v(node))
                named_entity_dict["EntityId"].append(self.F.entityId.v(node))
                named_entity_dict["Letter"].append(self.F.title.v(letter))

            data_frame_list.append(pd.DataFrame(named_entity_dict))

        return data_frame_list

    def draw_plot(self, use_fixed_x=False) -> None:
        """
        Draws a displot in Jupyter Notebooks of the occurences by date.
        TODO Add an option to use a fixed x range
        """

        FIXED_X_AXIS = (1610, 1767)

        data: list[pd.DataFrame] = []

        for data_frame in self.pd_data_frame:
            year_list = data_frame["Year"]
            year_list.name = data_frame["Name"][0]
            data.append(year_list)

        if use_fixed_x:
            displot(data=data, multiple='stack')
            plt.xlim(FIXED_X_AXIS)
        else:
            displot(data=data, x="Year", multiple='stack')

        plt.show()

    def detect_overlap(self) -> None:
        """
        TODO Detect if NE overlap in the same letter
        """

        pass

    def print_info(self) -> None:
        """
        Prints the data in the Jupyter Notebook.
        TODO Greatly expand the data shown and functionality (Ask supervisor for advice)
        """

        print(self.pd_data_frame)