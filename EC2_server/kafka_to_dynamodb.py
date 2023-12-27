from confluent_kafka import Consumer, KafkaError
import json
import boto3

# Kafka broker 서버 주소 설정
bootstrap_servers = 'ec2-13-125-191-87.ap-northeast-2.compute.amazonaws.com'
# Consumer 그룹 ID 설정
group_id = 'my-consumer-group'
# Confluent Kafka Topic 설정
topic = 'my_topic'

session = boto3.Session(
    aws_access_key_id='AKIAS5BXMQNDPCTNUPYW',
    aws_secret_access_key='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',
    region_name='ap-northeast-2'  # 사용하는 리전으로 변경하세요
)



dynamodb= session.client("dynamodb")
table_name="data"


# Consumer 구성 설정
conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'  # 가장 초기 위치부터 메시지 수신
}

# Kafka Consumer 생성
consumer = Consumer(conf)

# 구독 설정
consumer.subscribe([topic])


# 메시지 수신 루프
while True:
    msg = consumer.poll(0.1)  # 폴링 간격 설정 (1.0초)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break
    text=json.loads(msg.value())
    try:
        print(text['system']['network']['out']['packets'])
        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                'timestamp': {'S': str(text['@timestamp'])},
                'IN': {'M': {
                    'packets': {'N': str(text['system']['network']['in']['packets'])},
                    'errors': {'N': str(text['system']['network']['in']['errors'])},
                    'dropped': {'N': str(text['system']['network']['in']['dropped'])},
                    'bytes': {'N': str(text['system']['network']['in']['bytes'])},
                }},
                'OUT': {'M': {
                    'packets': {'N': str(text['system']['network']['out']['packets'])},
                    'errors': {'N': str(text['system']['network']['out']['errors'])},
                    'dropped': {'N': str(text['system']['network']['out']['dropped'])},
                    'bytes': {'N': str(text['system']['network']['out']['bytes'])},
                }}
            }
        )
        print("PutItem succeeded:", response)
    except KeyError:
        continue