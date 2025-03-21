import boto3

class SMS:
    def __init__(self,aws_access_key_id,aws_secret_access_key,region):
        self.sns = boto3.client("sns", 
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region)

    def verified(self,arn,phone):
        res = self.sns.list_subscriptions_by_topic(TopicArn=arn)
        for s in res['Subscriptions']:
            if s['Protocol'] == "sms" and s['Endpoint'] == phone:
                return True
        return False

    def subscribe(self,arn,phone) -> bool:
        try:
            if self.verified(arn,phone):
                return True
            else:
                self.sns.subscribe(
                    TopicArn=arn,
                    Protocol="sms",
                    Endpoint=phone
                )
                return True
        except:
            return False

    def publish(self,phone,message):
        res = self.sns.publish(
            PhoneNumber=phone,
            Message=message
        )
        return res
