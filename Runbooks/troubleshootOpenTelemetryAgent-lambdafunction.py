import boto3
import json

# Create a Systems Manager client
ssm = boto3.client('ssm')

def lambda_handler(event, context):
    # Extract the instance ID from the event
    instance_id = event.get('InstanceId')
    
    # Define the PowerShell commands to run in the Windows Instance
    commands = [
        '$ctlScript = \'C:\\Program Files\\Amazon\\AWSOTelCollector\\aws-otel-collector-ctl.ps1\'',
        '$status = (& $ctlScript -a status | ConvertFrom-Json).status',
        '',
        'if ($status -eq "running") {',
        '    Write-Host "AWSOTelCollector is running."',
        '} else {',
        '    Write-Host "AWSOTelCollector is not running. Starting..."',
        '    & $ctlScript -a start',
        '}'
    ]

    try:
        # Send the command to the instance
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunPowerShellScript',
            Parameters={
                'commands': commands
            }
        )

        # Get the command ID
        command_id = response['Command']['CommandId']

        # Wait for the command to complete
        waiter = ssm.get_waiter('command_executed')
        waiter.wait(
            CommandId=command_id,
            InstanceId=instance_id
        )

        # Get the command output
        output = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': output['Status'],
                'StandardOutputContent': output['StandardOutputContent']
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }


