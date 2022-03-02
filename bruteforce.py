import time
import csv
import re
import sys
from itertools import combinations


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
                        self.view.injection_file_error(line,"le cout n'est pas un entier")
                        test_1 = False
                    else:
                        test_1 = True
                    try:
                        rate = int(re.findall('\d+',row[2])[0])
                    except ValueError:
                        self.view.injection_file_error(line,"le benefice n'est pas un entier")
                        test_2 = False
                    else:
                        test_2 = True

                    if test_1 and test_2:
                        action = Action({"name": row[0], "cost": cost, "rate": rate})
                        liste_action.append(action)
                line += 1
        return liste_action


    def number_list(self, list_action : list):
        """explore toutes les combinaisons possibles"""
        max_benefit = 0
        best_list = ""
        for longueur in range(1, len(list_action)+1):
            comb = combinations(list_action, longueur)
            liste_500 = []
            for list_index in comb:
                liste_500.append(self.choice_action(list_index))

            for list_cost in liste_500:
                somme = 0
                for action in list_cost:
                    somme = action.benefit + somme
                if somme > max_benefit:
                    max_benefit = somme
                    best_list = list_cost
        return best_list




    def choice_action(self,list_sorted):
        """choice the action budget = 500"""
        budget = 500
        list_choice = []
        for action in list_sorted:
            if budget // action.cost >= 1:
                budget = budget - action.cost
                list_choice.append(action)
        return list_choice

    def run(self, file):
        """launch the program"""
        start = time.time()
        list_action = self.import_csv(file)
        list_sorted = self.number_list(list_action)
        self.view.display_list(list_sorted)
        end = time.time()
        duration = end - start
        self.view.display_time(duration)


class View:

    def injection_file_error(self, line: int, error: str):
        """handle the error in file"""
        print("{} ligne, {}".format(line, error))

    def display_list(self, data: list):
        """display a list"""
        line = 0
        total_cost = 0
        total_benefit = 0
        for row in data:
            print(f"{row.name :10} {row.cost :4} {row.rate :4} {row.benefit :6}")
            line += 1
            total_cost += row.cost
            total_benefit += row.benefit
        print(f"cout total: {total_cost :5} total benefice: {total_benefit :5.5} nb_action: {line :2}")

    def display_time(self, duration: float):
        print(f"duree du script : {duration :10}")


def main(str_param: str):
    gestion = Controller()
    gestion.run(str_param)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Vous devez entrer un fichier en paramètre !")