import time
import csv
import re
import sys


class Action:

    def __init__(self, dict_data: dict):
        """create a model action"""
        self.name = ""
        self.cost = 0
        self.rate = 0
        for key in dict_data:
            setattr(self, key, dict_data[key])
        self.benefit = self.calculate_gain()

    def calculate_gain(self):
        return self.cost*self.rate/100


class Controller:

    def __init__(self):
        self.view = View()

    def import_csv(self, file: str) -> list:
        """import the file in csv"""
        liste_action = []
        with open(file, newline='') as csvfile:
            spam = csv.reader(csvfile, delimiter=";")
            line = 0
            for row in spam:
                if line > 0:
                    try:
                        cost = int(row[1])
                    except ValueError:
                        self.view.injection_file_error(line, "le cout n'est pas un entier")
                        test_1 = False
                    else:
                        test_1 = True
                    try:
                        rate = int(re.findall('\d+',row[2])[0])
                    except ValueError:
                        self.view.injection_file_error(line, "le benefice n'est pas un entier")
                        test_2 = False
                    else:
                        test_2 = True

                    if test_1 and test_2:
                        action = Action({"name": row[0], "cost": cost, "rate": rate})
                        liste_action.append(action)
                line += 1
        return liste_action

    def sort_action(self, list_action: list) -> list:
        """sort collection action"""
        n = 0
        list_temp = list_action.copy()
        list_sort = []
        while n < len(list_action):
            benefit_max = 0
            action_save = None
            for action in list_temp:
                if action.benefit > benefit_max:
                    benefit_max = action.benefit
                    action_save = action
            list_temp.remove(action_save)
            list_sort.append(action_save)
            n += 1
        return list_sort

    def choice_action(self, list_sorted: list)->list:
        """choice the action budget = 500"""
        budget = 500
        list_choice = []
        for index in range(len(list_sorted)):
            if budget // list_sorted[index].cost >= 1 :
                budget = budget - list_sorted[index].cost
                list_choice.append(list_sorted[index])
        return list_choice

    def run(self, file):
        """launch the program"""
        start = time.time()
        list_action = self.import_csv(file)
        list_sorted = self.sort_action(list_action)
        list_choice = self.choice_action(list_sorted)
        self.view.display_list(list_choice)
        end = time.time()
        duration = end - start
        self.view.display_time(duration)


class View:

    def injection_file_error(self, line: int, error: str):
        """handle the error in file"""
        print("{} ligne, {}".format(line, error))

    def display_list(self, data: list):
        """display a list"""
        for row in data:
            print(f"{row.name :10} {row.cost :4} {row.rate :4} {row.benefit :6}")

    def display_time(self,duration):
        print(f"duree du script : {duration :10}")


def main(strParam):
    gestion = Controller()
    gestion.run(strParam)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Vous devez entrer un fichier en paramètre !")