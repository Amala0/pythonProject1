from model import Model
from view import View
from controller import Controller

# Author: Hyun Ju Jang

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.loadData()
    controller.startWindow()
