## 📝 8. Technical Report

### 🔧 Lambda Functions Overview

| Lambda Function           | Purpose                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| **FilterVolumes**         | Scans all EBS volumes in the region with `VolumeType = gp2` and tag `AutoConvert=true`. Returns metadata like VolumeId, InstanceId, Size, Region. |
| **LogToDynamoDB**         | Writes each selected volume's metadata to the `EBS_Conversion_Logs` DynamoDB table for audit trail and tracking. |
| **ModifyVolumeType**      | Invokes `modify_volume()` on the volume to convert it from `gp2` to `gp3`. |
| **VerifyModification**    | (Optional) Uses `describe_volumes()` to confirm that the volume type has changed successfully. |
| **SendNotification**      | Publishes success/error message with volume details to an SNS topic that alerts via email. |

---

### 🔐 IAM Policies and Roles

Each Lambda function is given **least privilege** access using individual IAM roles.

| Lambda Function IAM Role            | Permissions                                 |
|-------------------------------------|---------------------------------------------|
| `Lambda_Filter_Volumes_Role`       | `ec2:DescribeVolumes`                       |
| `Lambda_Log_To_Dynamo_DB_Role`     | `dynamodb:PutItem`, `dynamodb:DescribeTable`|
| `Lambda_Modify_Volume_Type_Role`   | `ec2:ModifyVolume`                          |
| `Lambda_Verify_Modification_Role`  | `ec2:DescribeVolumes`                       |
| `Lambda_Notify_Conversion_Role`    | `sns:Publish`                               |

Each policy is defined inline or attached as a managed policy and bound only to the respective Lambda.

---

### 🔁 Step Function Workflow

The state machine follows this order:

1. **FilterVolumes**: Identify target `gp2` volumes.
2. **LogToDynamoDB**: Record metadata for audit.
3. **ModifyVolumeType**: Convert volume to `gp3`.
4. **VerifyModification**: Confirm conversion success.
5. **SendNotification**: Notify via SNS with outcome.

Each Lambda returns data passed to the next state using Step Function's input/output mechanism.

---

### 🌍 Real-World Issues Handled

| Issue                               | Handling Strategy                                                       |
|------------------------------------|-------------------------------------------------------------------------|
| 🔄 **Volume In Use**               | AWS supports modifying in-use volumes; no need to detach.              |
| ❌ **Missing Permissions**          | Scoped IAM roles created to avoid over-permissioning errors.           |
| 🧪 **DynamoDB Validation Errors**   | Ensured partition key `VolumeId` is present; added schema validation.  |
| 🧱 **describe_volume_modifications** not available | Used fallback to `describe_volumes()` instead.                  |
| 📫 **SNS not configured properly** | Error handling added for missing `TopicArn`.                           |
| 🕓 **Lambda Timeout Errors**        | Increased timeout to 10s+ for `VerifyModification` logic.              |

---

### 📚 Lessons Learned

- **Modular Function Design**: Breaking logic into separate Lambdas helped with troubleshooting and reusability.
- **Event-Driven Design**: EventBridge + Step Functions made scheduling and orchestration simple and robust.
- **Least Privilege IAM**: Carefully scoping IAM permissions avoided many runtime access issues.
- **DynamoDB Logging**: Using a NoSQL table as an audit log is efficient and scalable.
- **CloudWatch Monitoring**: Logs from each Lambda were critical in debugging issues.
- **SNS for Visibility**: Email notifications enabled quick awareness of success/failure outcomes.

---

✅ *This report documents the technical logic, implementation challenges, and security posture of the project.*
