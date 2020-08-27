import simulation.schelling as schelling
import json


def parameters(filename):
    with open(filename, "r+") as config_file:
        config = json.loads(config_file.read())
    return config


def main():
    # JSON (JavaScript Object Notation)
    filename = "config.json"
    kwargs = parameters(filename)
    city = schelling.City(**kwargs)
    print(city)
    city.simulation()
    city.plot('afterSimulation.png')


if __name__ == '__main__':
    main()
