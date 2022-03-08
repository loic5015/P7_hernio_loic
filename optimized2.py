import time
import sys
import pandas as pd


class Action:

    def __init__(self, dict_data: dict):
        """create a model action"""
        self.name = ""
        self.cost = 0
        self.rate = 0
        for key in dict_data:
            setattr(self, key, dict_data[key])
        self.benefit = self.calculate_gain()
        self.unit_yield = self.calculate_yield()

    def calculate_gain(self):
        return self.cost*self.rate/100

    def calculate_yield(self):
        return self.benefit/self.cost


class Controller:

    def __init__(self):
        self.view = View()

    def import_csv(self, file: str) -> list:
        """import the file in csv"""
        list_action = []
        df = pd.read_csv(file)
        df.drop_duplicates(inplace=True)
        for x in df.index:
            if df.loc[x, "price"] <= 0:
                df.drop(x, inplace=True)
        new_df = df.sort_values(by=['price'], ascending=False)
        for x in new_df.index:
            action = Action({"name": new_df.loc[x, "name"], "cost": new_df.loc[x, "price"], "rate": new_df.loc[x, "profit"]})
            list_action.append(action)

        return list_action

    def choice_action(self, list_sorted: list) -> list:
        """choice the action budget = 500"""
        total_benefit_max = 0
        best_list = None
        for index in range(len(list_sorted)):
            list_choice = []
            budget = 500
            total_benefit = 0
            for nombre in list_sorted:
                unit_yield_max = 0
                action_save = None
                for action in list_sorted:
                    if action not in list_choice and action.unit_yield >= unit_yield_max and\
                            action.cost in [action.cost for action in list_sorted][0:index]\
                            and budget // action.cost >= 1:
                        unit_yield_max = action.unit_yield
                        action_save = action
                if action_save:
                    budget = budget - action_save.cost
                    total_benefit += action_save.benefit
                    list_choice.append(action_save)
            if total_benefit >= total_benefit_max:
                best_list = list_choice.copy()
                total_benefit_max = total_benefit
        return best_list

    def run(self, file):
        """launch the program"""
        start = time.time()
        list_action = self.import_csv(file)
        list_choice = self.choice_action(list_action)
        self.view.display_list(list_choice)
        end = time.time()
        duration = end - start
        self.view.display_time(duration)


class View:

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
        print(f"cout total: {total_cost :5} total benefice: {total_benefit :5} nb_action: {line :2}")

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
