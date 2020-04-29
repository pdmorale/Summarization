from cube.api import Cube
def create_pickle():
    cube=Cube(verbose=True)
    cube.load("ja")
    with open('cube.pickle', mode='wb') as wh:
        pickle.dump(cube, wh)

def load_pickle():
    with open('cube.pickle', mode='rb') as rh:
        cube = pickle.load(rh)
    return cube
