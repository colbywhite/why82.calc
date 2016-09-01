import boto3
import troposphere.iam as iam
from botocore.exceptions import ClientError
from troposphere import Template, Output, Ref, GetAtt, Join

STACK_NAME = 'why82-ci'
SERVICE = 'why82-lambda'
SERVICE_PROD = '%s-*' % SERVICE


def create_template():
    cft = Template(Description='A stack to set up the requirements needed for deploying Why82? Lambda code')
    policy_doc = {
        'Statement': [{
            'Action': ['cloudformation:DescribeStackResources',
                       'cloudformation:DescribeStackResource',
                       'cloudformation:DescribeStacks',
                       'cloudformation:DescribeStackEvents',
                       'cloudformation:CreateStack',
                       'cloudformation:DeleteStack',
                       'cloudformation:UpdateStack'],
            'Effect': 'Allow',
            'Resource': Join(':', ['arn', 'aws', 'cloudformation', Ref('AWS::Region'), Ref('AWS::AccountId'),
                                   Join('/', ['stack', SERVICE_PROD, '*'])])
        }, {
            'Action': ['s3:CreateBucket', 's3:ListBucket', 's3:DeleteBucket'],
            'Effect': 'Allow',
            'Resource': [
                Join(':::', ['arn:aws:s3', ('%s-serverlessdeploymentbucket-*' % SERVICE_PROD)]),
                Join(':::', ['arn:aws:s3', SERVICE_PROD])
            ]
        }, {
            'Action': ['s3:PutObject', 's3:GetObject', 's3:DeleteObject'],
            'Effect': 'Allow',
            'Resource': [
                Join(':::', ['arn:aws:s3', ('%s-serverlessdeploymentbucket-*/*' % SERVICE_PROD)]),
                Join(':::', ['arn:aws:s3', ('%s/*' % SERVICE_PROD)])
            ]
        }, {
            'Action': ['s3:PutBucketCORS', 's3:GetBucketCORS'],
            'Effect': 'Allow',
            'Resource': Join(':::', ['arn:aws:s3', SERVICE_PROD])

        }, {
            'Action': [
                'iam:CreateRole',
                'iam:UpdateRole',
                'iam:DeleteRole',
                'iam:PutRolePolicy',
                'iam:DeleteRolePolicy',
                'iam:ListRolePolicies',
                'iam:ListRoles',
                'iam:PassRole',
                'iam:GetRole'],
            'Effect': 'Allow',
            'Resource': Join(':', ['arn', 'aws', 'iam', '', Ref('AWS::AccountId'),
                                   ('role/%s-IamRoleLambdaExecution-*' % SERVICE_PROD)])
        }, {
            'Action': ['lambda:GetFunction',
                       'lambda:CreateFunction',
                       'lambda:DeleteFunction',
                       'lambda:InvokeFunction',
                       'lambda:GetFunctionConfiguration',
                       'lambda:UpdateFunctionConfiguration',
                       'lambda:UpdateFunctionCode'],
            'Effect': 'Allow',
            # Currently, AWS Lambda doesn't support permissions for this particular action at the resource-level.
            # Therefore, the policy specifies a wildcard character (*) as the Resource value.
            # http://docs.aws.amazon.com/lambda/latest/dg/access-control-identity-based.html
            'Resource': '*'
        }]
    }
    user = iam.User(title='ciUser', UserName='codeship', Policies=[iam.Policy(PolicyDocument=policy_doc,
                                                                              PolicyName=('%s-cipolicy' % SERVICE))])
    key = iam.AccessKey(title='ciKey', UserName=Ref(user))
    cft.add_resource(user)
    cft.add_resource(key)
    cft.add_output([
        Output('CiUser', Description='The user that CI will use to do releases', Value=Ref(user)),
        Output('CiAccessKey', Description='The CI user\'s access key', Value=Ref(key)),
        Output('CiSecretKey', Description='The CI user\'s secret key', Value=GetAtt(key, 'SecretAccessKey'))
    ])
    return cft


def create_stack():
    if does_stack_exist(STACK_NAME):
        print('%s already exists' % STACK_NAME)
    else:
        print('Creating %s stack' % STACK_NAME)
        template_body = create_template().to_json(indent=None)
        cf_client = boto3.client('cloudformation')
        cf_client.create_stack(StackName=STACK_NAME, TemplateBody=template_body, Capabilities=['CAPABILITY_NAMED_IAM'])
        waiter = cf_client.get_waiter('stack_create_complete')
        print('Waiting for stack %s to complete creation' % STACK_NAME)
        waiter.wait(StackName=STACK_NAME)


def update_stack():
    if not does_stack_exist(STACK_NAME):
        print('%s does not exist' % STACK_NAME)
    else:
        print('Updating %s stack' % STACK_NAME)
        template_body = create_template().to_json(indent=None)
        cf_client = boto3.client('cloudformation')
        cf_client.update_stack(StackName=STACK_NAME, TemplateBody=template_body, Capabilities=['CAPABILITY_NAMED_IAM'])
        waiter = cf_client.get_waiter('stack_update_complete')
        print('Waiting for stack %s to complete update' % STACK_NAME)
        waiter.wait(StackName=STACK_NAME)


def delete_stack():
    if not does_stack_exist(STACK_NAME):
        print('%s does not exist' % STACK_NAME)
    else:
        print('Deleting %s stack' % STACK_NAME)
        cf_client = boto3.client('cloudformation')
        cf_client.delete_stack(StackName=STACK_NAME)
        waiter = cf_client.get_waiter('stack_delete_complete')
        print('Waiting for stack %s to complete deletion' % STACK_NAME)
        waiter.wait(StackName=STACK_NAME)


def does_stack_exist(name):
    try:
        stack = boto3.resource('cloudformation').Stack(name)
        stack.stack_status
    except ClientError as err:
        return False
    else:
        return True
