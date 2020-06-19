from simulation.schelling import *
import json


def parameters(filename):
    with open(filename, "r+") as config_file:
        config = json.loads(config_file.read())
    return config


def main():
    # JSON (JavaScript Object Notation)
    filename = "config.json"
    kwargs = parameters(filename)
    city = City(**kwargs)
    city.plot('before.png')
    city.simulation()
    city.plot('after.png')


if __name__ == '__main__':
    main()
