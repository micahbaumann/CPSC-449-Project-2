import boto3

# Create a DynamoDB resource



# Delete tables if exists
class Dynamodbmodel:

    def __init__(self) -> None:
        self.dynamodb_resource = boto3.resource('dynamodb',
            aws_access_key_id='fakeMyKeyId',
            aws_secret_access_key='fakeSecretAccessKey',
            endpoint_url='http://localhost:8000',
            region_name='us-west-2'
        )

    def delete_table_if_exists(self):
        
        table_list = ['Users', 'Classes', 'Students', 'Enrollments', 'Instructors', 'InstructorClasses', 'Freeze']
        
        # Get all the existing tables
        table_names = [table.name for table in self.dynamodb_resource.tables.all()]

        for table in table_list:
            if table in table_names:
                t = self.dynamodb_resource.Table(table)
                t.delete()
                print(f"Deleting {t.name}...")
                t.wait_until_not_exists()
        return

    # Create Users table
    def create_tables(self):
        users_table = self.dynamodb_resource.create_table(
            TableName='Users',
            KeySchema=[
                {'AttributeName': 'UserId', 'KeyType': 'HASH'}
            ],

            AttributeDefinitions=[
                {'AttributeName': 'UserId', 'AttributeType': 'N'},
                {'AttributeName': 'Username', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'UsersIndex',
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'KeySchema': [
                        {
                            'AttributeName': 'Username',
                            'KeyType': 'HASH'
                        }
                    ],
                    "ProvisionedThroughput": { 
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        users_table.wait_until_exists()
        users_table.put_item(Item={'UserId': 100,'Username':"ornella","Fullname":"Ornella Dsouza","Email":"o@gmail.com"})
        
        #response = users_table.query(KeyConditionExpression=Key("UserId").eq(100))
        
        # Create Classes table
        classes_table = self.dynamodb_resource.create_table(
            TableName='Classes',
            KeySchema=[
                {'AttributeName': 'ClassID', 'KeyType': 'HASH'},
                {'AttributeName': 'SectionNumber', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'ClassID', 'AttributeType': 'N'},
                {'AttributeName': 'SectionNumber', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        classes_table.wait_until_exists()

        # Create Students table
        students_table = self.dynamodb_resource.create_table(
            TableName='Students',
            KeySchema=[
                {'AttributeName': 'StudentID', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'StudentID', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        students_table.wait_until_exists()

        # Create Enrollments table
        enrollments_table = self.dynamodb_resource.create_table(
            TableName='Enrollments',
            KeySchema=[
                {'AttributeName': 'EnrollmentID', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'EnrollmentID', 'AttributeType': 'N'},
                {'AttributeName': 'StudentID', 'AttributeType': 'N'},
                {'AttributeName': 'ClassID', 'AttributeType': 'N'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'EnrollmentsIndex',
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'KeySchema': [
                        {
                            'AttributeName': 'StudentID',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'ClassID',
                            'KeyType': 'RANGE'
                        }
                    ],
                    "ProvisionedThroughput": { 
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        enrollments_table.wait_until_exists()

        # Create Instructors table
        instructors_table = self.dynamodb_resource.create_table(
            TableName='Instructors',
            KeySchema=[
                {'AttributeName': 'InstructorID', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'InstructorID', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        instructors_table.wait_until_exists()

        # Create InstructorClasses table
        instructor_classes_table = self.dynamodb_resource.create_table(
            TableName='InstructorClasses',
            KeySchema=[
                {'AttributeName': 'InstructorClassesID', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'InstructorClassesID', 'AttributeType': 'N'},
                {'AttributeName': 'InstructorID', 'AttributeType': 'N'},
                {'AttributeName': 'ClassID', 'AttributeType': 'N'}
            ],
            GlobalSecondaryIndexes=[
                {
                    
                    'IndexName': 'InstructorClassesIndex',
                    'Projection': {
                        'ProjectionType': 'ALL'
                        },
                    'KeySchema': [
                        {
                            'AttributeName': 'InstructorID',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'ClassID',
                            'KeyType': 'RANGE'
                        }
                    ],
                    "ProvisionedThroughput": { 
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        instructor_classes_table.wait_until_exists()

        # Create Freeze table
        freeze_table = self.dynamodb_resource.create_table(
            TableName='Freeze',
            KeySchema=[
                {'AttributeName': 'IsFrozen', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'IsFrozen', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        freeze_table.wait_until_exists()

        # Insert initial data into Freeze table
        freeze_table.put_item(Item={'IsFrozen': 0})

if __name__ == "__main__":
    obj = Dynamodbmodel()
    obj.delete_table_if_exists()
    obj.create_tables()
    print("Dynamodb tables created")