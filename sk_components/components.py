import json


class Menu:
    """
    A class that can design a custom menu and menu options in a
    CLI Application

    Attributes:
        title(str): The title of the Main Menu.
        action_handler(function): the excutable function for the Menu.

    Methods:
        add_option:
            A method to add an option to the menu.
            Attributes:
                option(str): the name of the option.

        deactivate:
            A method to disable the currently active menu.

        activate:
            A method to activate the chosen Menu class object and
            display its options.
    """

    def __init__(self, title, action_handler):
        self.options = list()
        self.title = title
        self.handler = action_handler
        self.active = False

    def add_option(self, option):
        """
        It adds options to the menu.

        Attributes:
            option(str): the name of the option.
        """
        self.options.append(option)

    def deactivate(self):
        """
        It disables the currently active Menu.
        """
        self.active = False

    def activate(self):
        """
        It activates the chosen Menu object and displays its options.
        """
        self.active = True
        print("-" * len(self.title))
        print(self.title)
        print("-" * len(self.title))
        while self.active:
            x = 1
            for option in self.options:
                print(f"{x}. {option}")
                x += 1
            choice = input("Enter your choice : ")
            try:
                choice = int(choice)
            except:
                print(f"Invalid Choice : {choice}")
                continue
            if choice < 1 or choice > len(self.options):
                print(f"Invalid Choice : {choice}")
                continue
            self.handler(self, choice)


class Wrapper:
    """
    A class that provides features for the conversion of primitive class
    objects to JSON Strings and vise-versa.

    Attributes:
        value: the primitive class type object that is to be converted
        to JSON String.

    Methods:
        to_json: converts the active Wrapper object into a JSON String.
        from_json: converts the given JSON String into it's primitive
        datatype(class).
    """

    def __init__(self, value):
        self.value = value
        self.class_name = type(value).__name__  # str of type str

    def to_json(self):
        """
        Converts the active Wrapper object into a JSON String.

        Return Value: returns a JSON String.
        """
        if ("str" in self.class_name):
            return json.dumps(self.value)
        return json.dumps(self.__dict__, indent=4)

    def from_json(json_string):
        """
        Converts the given JSON String into it's primitive
        datatype(class).

        Attributes:
            json_string(str): the JSON String that is to be converted.

        Return Value: returns a premitive data type(class).
        """
        new_dict = json.loads(json_string)
        to_eval = f"{new_dict['class_name']}({new_dict['value']})"
        return eval(to_eval)
