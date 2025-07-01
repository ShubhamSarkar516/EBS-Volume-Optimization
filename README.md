# 🚀 Intelligent EBS Volume Optimization using AWS Lambda, Step Functions, CloudWatch, SNS & DynamoDB

This project demonstrates a fully automated, serverless AWS pipeline that **identifies gp2 EBS volumes**, verifies if they are tagged for conversion, converts them to **gp3**, logs the actions, and notifies via SNS — all coordinated using **AWS Step Functions**.

---

## 🎯 Objective

The aim is to reduce EBS storage costs by automatically converting eligible `gp2` volumes to `gp3`. This solution supports:

- Cost optimization with no manual intervention
- Full visibility via DynamoDB logs
- Real-time notifications via SNS
- Modular Lambda functions for each stage
- Scheduled, event-driven orchestration

---

## 🛠 Services Used

| AWS Service         | Purpose                                                   |
|---------------------|-----------------------------------------------------------|
| EC2 / EBS           | EBS volumes to be monitored and converted                 |
| Lambda              | Function logic (Filter, Modify, Log, Notify)              |
| Step Functions      | Orchestrates the workflow                                 |
| DynamoDB            | Stores audit logs of converted volumes                    |
| CloudWatch Logs     | Logs Lambda execution output and errors                   |
| SNS                 | Sends email notifications on success/failure              |
| EventBridge         | Triggers the Step Function based on schedule              |
| IAM Roles / Policies| Ensures secure and scoped access for Lambda functions     |

---

## 🧱 Project Architecture

> Diagram is stored at `architecture/diagram.png`

![EBS Optimization Architecture](architecture/diagram.png)

---

## 📂 Folder Structure

```bash
ebs-volume-optimization/
├── architecture/
│   └── diagram.png
├── lambdas/
│   ├── filter_volumes.py
│   ├── log_to_dynamodb.py
│   ├── modify_volume.py
│   ├── verify_modification.py
│   └── send_notification.py
├── step-function/
│   └── state_machine_definition.json
├── dynamodb/
│   └── table_schema.json
├── eventbridge/
│   └── rule_schedule.json
├── iam-policies/
│   ├── lambda_filter_policy.json
│   ├── log_to_dynamo_policy.json
│   └── general_lambda_role.json
├── screenshots/
│   ├── step_function_execution.png
│   ├── dynamodb_entries.png
│   ├── sns_email_alert.png
│   └── cloudwatch_logs.png
├── technical-report.md
└── README.md
```

🔄 Workflow Breakdown
1. Scheduled Trigger
EventBridge Rule triggers every day at 1 AM UTC.
Target: AWS Step Function.

2. Step Function Workflow
Step	                     Lambda Function	                    Description

FilterVolumes	             Filter_Volume.py	                  Scans EBS for gp2 volumes with tag AutoConvert=true
LogToDynamo	               Log_To_Dynamo_DB.py	              Logs volume metadata to DynamoDB
ModifyVolume	             Modify_Volume_Type.py	            Converts the volume to gp3 using modify_volume()
VerifyModification	       Verify_Modification.py	            Optionally confirms if the conversion succeeded
SendNotification	         Send_Notification.py	              Sends SNS email notification

🧪 Input Payload

[
  {
    "VolumeId": "vol-080d7c30627aae74a",
    "Size": 8,
    "Region": "ap-south-1",
    "InstanceId": "i-08de65bc01076ef0d"
  }
]

📘 DynamoDB Table: EBS_Conversion_Logs
Attributes:
VolumeId (Partition Key)
InstanceId
Region
Size
Status
Timestamp

📨 SNS Notification Example
Subject: EBS Volume Converted
Volume ID: vol-0123456789abcdef0
Region: ap-south-1
Status: SUCCESS

🔐 IAM Role Summary

Lambda Function	                        Required Permissions

Lambda_Filter_Volumes_Role       ->    ec2:DescribeVolumes
Lambda_Log_To_Dynamo_DB_Role	   ->    dynamodb:PutItem, dynamodb:DescribeTable
Lambda_Modify_Volume_Type_Role   ->    ec2:ModifyVolume
Lambda_Verify_Modification_Role	 ->    ec2:DescribeVolumes
Lambda_Notify_Conversion_Role    ->    sns:Publish

All policies follow the principle of least privilege.

🖥 Deployment Steps Summary
✅ Create a EC2/EBS
✅ Create EBS_Conversion_Logs DynamoDB table
✅ Create SNS topic EBS-Conversion-Alert and subscribe via email
✅ Create custom IAM policies and roles
✅ Create all Lambda functions (Python 3.13)
✅ Create Step Function with the state machine JSON
✅ Set up EventBridge rule with cron expression
✅ Test manually with sample event → verify logs and notification
✅ Capture screenshots and validate flow

📸 Sample Screenshots (in /screenshots)
✅ Step Function execution flow
✅ DynamoDB Scan output
✅ Email alert from SNS
✅ CloudWatch logs of Lambda output

📋 Technical Report
Detailed technical report is available in technical-report.md, which explains:
Design reasoning
IAM role and policy decisions
Real-world error handling (e.g., in-use volumes, permission failures)
Logging and observability practices

✍ Author
Shubham Sarkar
AWS | DevOps | Python
🔗 Github -> https://github.com/ShubhamSarkar516
🔗 LinkedIn -> www.linkedin.com/in/shubham-sarkar-584570247
