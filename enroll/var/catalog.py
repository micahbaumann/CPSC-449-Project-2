import boto3


# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb', aws_access_key_id='hello',
    aws_secret_access_key='hello123',
    region_name='us-west-2')

# Create Users table
users_table = dynamodb.create_table(
    TableName='Users',
    KeySchema=[
        {'AttributeName': 'UserId', 'KeyType': 'HASH'}
    ],

    AttributeDefinitions=[
        {'AttributeName': 'UserId', 'AttributeType': 'N'},
        {'AttributeName': 'Username', 'AttributeType': 'S'},
        {'AttributeName': 'FullName', 'AttributeType': 'S'},
        {'AttributeName': 'Email', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
users_table.wait_until_exists()

# Create Classes table
classes_table = dynamodb.create_table(
    TableName='Classes',
    KeySchema=[
        {'AttributeName': 'ClassID', 'KeyType': 'HASH'},
        {'AttributeName': 'SectionNumber', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'ClassID', 'AttributeType': 'N'},
        {'AttributeName': 'SectionNumber', 'AttributeType': 'N'},
        {'AttributeName': 'CourseCode', 'AttributeType': 'S'},
        {'AttributeName': 'Name', 'AttributeType': 'S'},
        {'AttributeName': 'MaximumEnrollment', 'AttributeType': 'N'},
        {'AttributeName': 'WaitlistCount', 'AttributeType': 'N'},
        {'AttributeName': 'WaitlistMaximum', 'AttributeType': 'N'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
classes_table.wait_until_exists()

# Create Students table
students_table = dynamodb.create_table(
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
enrollments_table = dynamodb.create_table(
    TableName='Enrollments',
    KeySchema=[
        {'AttributeName': 'EnrollmentID', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'EnrollmentID', 'AttributeType': 'N'},
        {'AttributeName': 'StudentID', 'AttributeType': 'N'},
        {'AttributeName': 'ClassID', 'AttributeType': 'N'},
        {'AttributeName': 'SectionNumber', 'AttributeType': 'N'},
        {'AttributeName': 'EnrollmentStatus', 'AttributeType': 'S'}
    ],
    GlobalSecondaryIndexes=[
        {
            'Create': {
                'IndexName': 'EnrollmentsIndex',
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'KeySchema': [
                    {
                        'AttributeName': 'ClassID',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'StudentID',
                        'KeyType': 'RANGE'
                    },
                    {
                        'AttributeName': 'SectionNumber',
                        'KeyType': 'RANGE'
                    }
                ]
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
instructors_table = dynamodb.create_table(
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
instructor_classes_table = dynamodb.create_table(
    TableName='InstructorClasses',
    KeySchema=[
        {'AttributeName': 'InstructorClassesID', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'InstructorClassesID', 'AttributeType': 'N'},
        {'AttributeName': 'InstructorID', 'AttributeType': 'N'},
        {'AttributeName': 'ClassID', 'AttributeType': 'N'},
        {'AttributeName': 'SectionNumber', 'AttributeType': 'N'}
    ],
    GlobalSecondaryIndexes=[
        {
            'Create': {
                'IndexName': 'InstructorClassesIndex',
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'KeySchema': [
                    {
                        'AttributeName': 'ClassID',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'SectionNumber',
                        'KeyType': 'RANGE'
                    }
                ]
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
freeze_table = dynamodb.create_table(
    TableName='Freeze',
    KeySchema=[
        {'AttributeName': 'IsFrozen', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'IsFrozen', 'AttributeType': 'BOOL'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
freeze_table.wait_until_exists()

# Insert initial data into Freeze table
freeze_table.put_item(Item={'IsFrozen': 0})
