import argparse

parser = argparse.ArgumentParser(
    prog='at-blackboard',
    description='General working memory for AT-TECHNOLOGY components')

parser.add_argument('-u', '--url', help="RabbitMQ URL to connect", required=False, default=None)
parser.add_argument('-h', '--host', help="RabbitMQ host to connect", required=False, default=None)