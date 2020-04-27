import argparse
import yaml

parser = argparse.ArgumentParser(description='Run a single stethoscope test')
parser.add_argument('test')


def run_test(test):
    with open(test, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)

    print(config)


if __name__ == '__main__':
    args = parser.parse_args()

    run_test(args.test)
