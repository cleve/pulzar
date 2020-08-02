import os
import sys
from core.core_jobs import CoreJobs


class Example(CoreJobs):
    """Example of job programation
    """

    def __init__(self, params):
        print(params)


def execute(arguments):
    """Point of entrance
    """
    example = Example(arguments[0])
    example.run_job()


if __name__ == '__main__':
    args = sys.argv[1]
    execute(args)
