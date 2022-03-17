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

    def calculate_gain(self):
        return self.cost*self.rate/100


class Controller:

    def __init__(self):
        self.view = View()

    def import_csv(self, file: str) -> list:
        """import the file with pandas"""
        list_action = []
        df = pd.read_csv(file)
        df.drop_duplicates(inplace=True)
        for x in df.index:
            if df.loc[x, "price"] <= 0:
                df.drop(x, inplace=True)
            else:
                df.loc[x, "price"] = df.loc[x, "price"] * 100
                df.loc[x, "profit"] = df.loc[x, "profit"]
        new_df = df.sort_values(by=['price'], ascending=False)
        for x in new_df.index:
            action = Action({"name": new_df.loc[x, "name"], "cost": int(new_df.loc[x, "price"]),
                             "rate": new_df.loc[x, "profit"]})
            list_action.append(action)

        return list_action

    def knap_sack(self, list_sorted: list):
        """mis en place sac du dos dynamique"""
        budget = 500*100
        n = len(list_sorted)
        list_cost = [action.cost for action in list_sorted]
        list_benefit = [action.benefit for action in list_sorted]
        matrice = [[0 for x in range(budget + 1)] for x in range(n + 1)]
        for i in range(n + 1):
            for w in range(budget + 1):
                if i == 0 or w == 0:
                    matrice[i][w] = 0
                elif list_cost[i - 1] <= w:
                    # test si cout de l'action inferieur a budget itere de 0 a 50000
                    """prend le max entre le benefice de l'action avec l'ajout du benefice de l'action issue de
                     la difference du budget itere - cout action et le benefice de la matrice pour le budget donnee"""
                    matrice[i][w] = max(list_benefit[i - 1] + matrice[i - 1][w - list_cost[i - 1]], matrice[i - 1][w])
                else:
                    matrice[i][w] = matrice[i - 1][w]

        total_benefice = matrice[n][budget]
        budget = 500 * 100
        n = len(list_sorted)
        list_action = []
        while budget >= 0 and n >= 0:
            action = list_sorted[n-1]
            if matrice[n][budget] == matrice[n - 1][budget-action.cost] + action.benefit:
                list_action.append(action)
                budget -= action.cost
            n -= 1

        return list_action, total_benefice

    def run(self, file):
        """launch the program"""
        start = time.time()
        list_action = self.import_csv(file)
        list_choice, total = self.knap_sack(list_action)
        self.view.display_list(list_choice, total)
        end = time.time()
        duration = end - start
        self.view.display_time(duration)


class View:

    def display_list(self, data: list, total: float):
        """display a list"""
        line = 0
        total_cost = 0
        for row in data:
            print(f"{row.name :10} {row.cost/100 :4} {row.rate :4} {row.benefit/100 :6}")
            line += 1
            total_cost += row.cost/100

        print(f"cout total: {total_cost :5} total benefice: {total/100 :5} nb_action: {line :2}")

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
