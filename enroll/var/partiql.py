from datetime import datetime
from decimal import Decimal
import logging
from pprint import pprint
#import dynamodb_dummy_data
import boto3
from botocore.exceptions import ClientError

#from scaffold import Scaffold
#from dynamodb_dummy_data import DynamodbData
#from catalog import Dynamodbmodel
logger = logging.getLogger(__name__)

class PartiQLWrapper:
    """
    Encapsulates a DynamoDB resource to run PartiQL statements.
    """

    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource


    def run_partiql(self, statement, params):
        """
        Runs a PartiQL statement. A Boto3 resource is used even though
        `execute_statement` is called on the underlying `client` object because the
        resource transforms input and output from plain old Python objects (POPOs) to
        the DynamoDB format. If you create the client directly, you must do these
        transforms yourself.

        :param statement: The PartiQL statement.
        :param params: The list of PartiQL parameters. These are applied to the
                       statement in the order they are listed.
        :return: The items returned from the statement, if any.
        """
        try:
            output = self.dyn_resource.meta.client.execute_statement(
                Statement=statement, Parameters=params
            )
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                logger.error(
                    "Couldn't execute PartiQL '%s' because the table does not exist.",
                    statement,
                )
            else:
                logger.error(
                    "Couldn't execute PartiQL '%s'. Here's why: %s: %s",
                    statement,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
            raise
        else:
            return output



def run_scenario(catalog, wrapper, table_name):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("-" * 88)
    print("Welcome to the Amazon DynamoDB PartiQL single statement demo.")
    print("-" * 88)


    print(f"Getting data for Users")
    output = wrapper.run_partiql(
        f'SELECT * FROM "{table_name}" ',["Users"],
    )
    for item in output["Items"]:
        print(f"\n{item['UserId']}, {item['FullName']}")#{item('Username')}") # replace appropriate keys
        #pprint(output["Items"])
    print("-" * 88)

  
    print("Success!")
    print("-" * 88)

    print(f"Getting data again to verify our update.")
   
    print("-" * 88)

    print("\nThanks for watching!")
    print("-" * 88)


if __name__ == "__main__":
    try:
        dynamodb_resource = boto3.resource('dynamodb',
            aws_access_key_id='fakeMyKeyId',
            aws_secret_access_key='fakeSecretAccessKey',
            endpoint_url='http://localhost:8000',
            region_name='us-west-2')
        catalog= Dynamodbmodel(dynamodb_resource)
        Users = PartiQLWrapper(dynamodb_resource)
        run_scenario(catalog, Users, "Users")
    except Exception as e:
        print(f"Something went wrong with the demo! Here's what: {e}")

