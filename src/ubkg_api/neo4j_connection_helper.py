# JAS February 2024 - Added configurable timeout to allow for timeboxed queries.

import logging
import neo4j

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s:%(lineno)d: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

instance = None


class Neo4jConnectionHelper(object):
    @staticmethod
    def create(server, username, password, timeout):
        if instance is not None:
            raise Exception(
                "An instance of Neo4jConnectionHelper exists already. Use the Neo4jConnectionHelper.instance() method to retrieve it.")

        return Neo4jConnectionHelper(server, username, password, timeout)

    @staticmethod
    def instance():
        if instance is None:
            raise Exception(
                "An instance of Neo4jConnectionHelper does not yet exist. Use Neo4jConnectionHelper.create() to create a new instance")

        return instance

    @staticmethod
    def is_initialized():
        return instance is not None

    def __init__(self, server, username, password, timeout):

        global instance
        self.driver = neo4j.GraphDatabase.driver(server, auth=(username, password))
        if instance is None:
            instance = self
        self._timeout = timeout

    # https://neo4j.com/docs/api/python-driver/current/api.html
    def close(self):
        self.driver.close()

    def check_connection(self):
        record_field_name = 'result'
        query = f"RETURN 1 AS {record_field_name}"

        # Sessions will often be created and destroyed using a with block context
        with self.driver.session() as session:
            # Returned type is a Record object
            records = session.run(query)

            # When record[record_field_name] is not None (namely the cypher result is not null)
            # and the value equals 1
            for record in records:
                if record and record[record_field_name] and (record[record_field_name] == 1):
                    logger.info("Neo4j is connected :)")
                    return True

        logger.info("Neo4j is NOT connected :(")

        return False

    @property
    def timeout(self):
        """Gets the timeout of this Neo4jConnectionHelper

        :return: The timeout of this Neo4jConnectionHelper.
        :rtype: int
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Sets the timeout of this Neo4jConnectionHelper.

        :param timeout: The timeout of this Neo4jConnectionHelper.
        :type timeout: int
        """

        self._timeout = timeout