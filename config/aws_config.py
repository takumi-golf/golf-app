import boto3
from botocore.exceptions import ClientError

def setup_aws_limits():
    # AWS Budgetsの設定
    budgets_client = boto3.client('budgets')
    try:
        budget = {
            'AccountId': '112567275216',
            'BudgetName': 'MonthlyBudget',
            'BudgetLimit': {
                'Amount': '100',
                'Unit': 'USD'
            },
            'TimeUnit': 'MONTHLY',
            'BudgetType': 'COST',
            'CostFilters': {
                'Service': ['Amazon EC2', 'Amazon RDS', 'Amazon ElastiCache']
            }
        }
        budgets_client.create_budget(
            AccountId='112567275216',
            Budget=budget,
            NotificationsWithSubscribers=[
                {
                    'Notification': {
                        'NotificationType': 'ACTUAL',
                        'ComparisonOperator': 'GREATER_THAN',
                        'Threshold': 80,
                        'ThresholdType': 'PERCENTAGE'
                    },
                    'Subscribers': [
                        {
                            'SubscriptionType': 'EMAIL',
                            'Address': 'takumi.n1os.221@gmail.com'
                        }
                    ]
                }
            ]
        )
        print("AWS Budgetsの設定が完了しました")
    except Exception as e:
        print(f"AWS Budgetsの設定中にエラーが発生しました: {e}")

    # CloudWatchアラームの設定
    cloudwatch_client = boto3.client('cloudwatch')
    try:
        # CPU使用率のアラーム
        cloudwatch_client.put_metric_alarm(
            AlarmName='HighCPUUtilization',
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Statistic='Average',
            Period=300,
            EvaluationPeriods=2,
            Threshold=80.0,
            ComparisonOperator='GreaterThanThreshold',
            AlarmActions=[f'arn:aws:sns:ap-northeast-1:112567275216:HighCPUUtilization'],
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': 'i-0a1b2c3d4e5f6g7h8'  # 実際のインスタンスIDに更新
                }
            ]
        )

        # メモリ使用率のアラーム
        cloudwatch_client.put_metric_alarm(
            AlarmName='HighMemoryUtilization',
            MetricName='MemoryUtilization',
            Namespace='System/Linux',
            Statistic='Average',
            Period=300,
            EvaluationPeriods=2,
            Threshold=80.0,
            ComparisonOperator='GreaterThanThreshold',
            AlarmActions=[f'arn:aws:sns:ap-northeast-1:112567275216:HighMemoryUtilization']
        )
        print("CloudWatchアラームの設定が完了しました")
    except Exception as e:
        print(f"CloudWatchアラームの設定中にエラーが発生しました: {e}")

def setup_autoscaling():
    autoscaling_client = boto3.client('autoscaling')
    try:
        # 自動スケーリンググループの設定
        autoscaling_client.create_auto_scaling_group(
            AutoScalingGroupName='GolfClubRecommendationASG',
            LaunchConfigurationName='GolfClubRecommendationLC',
            MinSize=1,
            MaxSize=2,
            DesiredCapacity=1,
            VPCZoneIdentifier='YOUR_SUBNET_IDS',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'GolfClubRecommendation',
                    'PropagateAtLaunch': True
                }
            ]
        )

        # スケーリングポリシーの設定
        autoscaling_client.put_scaling_policy(
            AutoScalingGroupName='GolfClubRecommendationASG',
            PolicyName='ScaleUpPolicy',
            PolicyType='TargetTrackingScaling',
            TargetTrackingConfiguration={
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ASGAverageCPUUtilization'
                },
                'TargetValue': 70.0
            }
        )

    except ClientError as e:
        print(f"Error setting up autoscaling: {e}")

if __name__ == '__main__':
    setup_aws_limits()
    setup_autoscaling() 