'''This process should be executed in the node side
'''
from pulzarcore.core_job_discovery import JobDiscovery


def main():
    """Entrance
    """
    job_discovery = JobDiscovery()
    job_discovery.discover()


if __name__ == "__main__":
    main()
