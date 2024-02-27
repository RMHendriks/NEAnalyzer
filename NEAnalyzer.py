import pandas as pd
import matplotlib.pyplot as plt
from seaborn import displot, barplot
from numpy import transpose
from copy import deepcopy
from collections import Counter
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

        # TODO tmp solution
        self.F = F
        self.T = T
        self.L = L

        self.named_entity = input_list
        self.named_entity_list = self.get_named_entity(input_list)

        if not self.named_entity_list:
            print("Entity list is empty")
        else:
            print("Success!")

        self.pd_data_frame = self.build_data_frame()
    
    def get_named_entity(self, input_list) -> list[list[tuple[int]]]:
        """
        Gets the named entity from a query search of the corpus.
        
        Returns a list of tuples with nodes as Int.
        """

        node_list: list[list[tuple[int]]] = []

        for element in input_list:
            
            # convert a str list
            if element and isinstance(element, str):

                query_search_list = []

                for char in element:
                    if char == " ":
                        query_search_list.append("\\ ")
                    else:
                        query_search_list.append(char)

                query_search = ''.join(query_search_list)

            # convert an int (node) list
            # TODO node inputs need more checks if valid search all other named entities
            elif element and isinstance(element, int) and self.F.entityId.v(element) is not None:
                query_search = self.T.text(element)

            else:
                print(f"Input \"{element}\" is not valid")
                continue

            query = f"""
letter
    word trans~{query_search} entityId entityKind*
                    """
            result = self.A.search(query)
            if not result:
                print(f"\"{element}\" does not exist as a named entity")
            else:
                node_list.append(result)
    
        
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
    
    def normalize_corpus(self) -> dict[int, float]:
        """ 
        Calculates the amount of words in the corpus per year and give back a dict
        of ratios per year that can be used to normalize the corpus.
        """

        # Sort the letters by year in a dict
        letter_by_year_dict = {}

        for letter in self.F.otype.s("letter"):
            year = self.F.year.v(letter)
            words = len(self.L.d(letter, otype="word"))
            if year in letter_by_year_dict:
                letter_by_year_dict[year] += words
            elif year is None:
                continue
            else:
                letter_by_year_dict[year] = words

        # Normalize the years
        noralized_year_dict = {}
        total_words = sum(letter_by_year_dict.values())

        for year, words in letter_by_year_dict.items():
            noralized_year_dict[year] = words / total_words

        return noralized_year_dict

    def draw_plot(self, use_fixed_x=False, normalize=False) -> None:
        """
        Draws a displot in Jupyter Notebooks of the occurences by date.
        """

        FIXED_X_AXIS = (1610, 1767)

        data = []

        for data_frame in self.pd_data_frame:
            year_list = data_frame["Year"]
            year_list.name = data_frame["Name"][0]
            data.append(year_list)

        if normalize:
            normalized_year_dict = self.normalize_corpus()
            tmp_data_dict = []

            for year_list in data:
                tmp_data_dict.append(Counter(year_list))

            data = []

            for year_dict_list in tmp_data_dict:
                for year in year_dict_list:
                    year_dict_list[year] *= normalized_year_dict[year]

                data.append(pd.DataFrame(year_dict_list.items(), columns=['year', 'value']))

            print(data)

        if use_fixed_x:
            displot(data=data, multiple='stack')
            plt.xlim(FIXED_X_AXIS)
        else:
            displot(data=data, multiple='stack')

        plt.show()

    def detect_overlap_index(self) -> None:
        """
        TODO See if it is possible to detect overlap on more than 2 nodes (x nodes of overlap)
        """

        overlap_list: list[list(int, int, int)] = []

        for letter_node_list in self.named_entity_list:
            for letter, node in letter_node_list:
                for lst in self.named_entity_list:
                    if lst == letter_node_list:
                        continue
                    for letter2, node2 in lst:
                        if letter == letter2 and [letter, node2, node] not in overlap_list:
                            overlap_list.append([letter, node, node2])

        # Shuffles the nodes back into order
        for overlap in overlap_list:
            if overlap[1] > overlap[2]:
                overlap[1], overlap[2] = overlap[2], overlap[1]

        self.print_overlap(overlap_list)

    def detect_overlap_letter(self, print_letters=False) -> None:
        """ Detects overlap of named entities in a letter"""

        copied_named_entities_list = deepcopy(self.named_entity_list)
        letter_list: list(tuple(int)) = []

        for named_entity in copied_named_entities_list:
            letter_list.append(tuple(transpose(named_entity)[0]))

        # uses the first list of letters as a base to compare to
        intersecting_elements = set(letter_list[0])

        # itarates over the remaining letter lists to see if any intersections remain
        for lst in letter_list[1:]:
            intersecting_elements.intersection_update(lst)

        print(f"Overlap of the {len(self.named_entity)} named entities in {len(intersecting_elements)} letters.\n")

        if print_letters:
            for letter in intersecting_elements:
                self.A.plain(letter)

    def print_overlap(self, overlap_list) -> None:
        """
        Prints overlap information
        TODO redesign the information shown after starting work on the showing of better
        formated text 
        TODO Highlight the overlap in the letter if shown
        """

        print(f"{len(overlap_list)} overlap(s)")

        for n, overlap in enumerate(overlap_list):
            print(f"Overlap {n + 1}: ", end="")
            for node in overlap[1:]:
                print(self.T.text(node), end="")
                if node != overlap[-1]:
                    print("- ", end="")
            self.A.plain(overlap[0])
            for node in overlap[1:]:
                self.A.plain(node)
                self.A.plain(self.L.u(node, otype="line")[0])

    def print_info(self) -> None:
        """
        Prints the data in the Jupyter Notebook.
        TODO Greatly expand the data shown and functionality (Ask supervisor for advice)
        """

        print(self.pd_data_frame)