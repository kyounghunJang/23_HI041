from confluent_kafka import Consumer, KafkaError, Producer
import json
import pandas as pd
import numpy as np
from keras.models import Model, load_model
from pickle import load
import pickle

load_scaler = load(open('./scaler.pkl','rb'))
# Kafka broker 서버 주소 설정
bootstrap_servers = 'ec2-13-125-191-87.ap-northeast-2.compute.amazonaws.com'
# Consumer 그룹 ID 설정
group_id = 'my-consumer-group'
# Confluent Kafka Topic 설정
topic = 'my_topic'
# Consumer 구성 설정
conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'  # 가장 초기 위치부터 메시지 수신
}
producer_config = {
    'bootstrap.servers': bootstrap_servers,

}
producer = Producer(producer_config)

# Kafka Consumer 생성
consumer = Consumer(conf)
# 구독 설정
consumer.subscribe([topic])
# 메시지 수신 루프
isolation = load_model('isolation_forest_model.pkl')

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
        data=[text['system']['network']['out']['dropped'],text['system']['network']['out']['packets']\
        ,text['system']['network']['out']['errors'],text['system']['network']['out']['bytes'],\
        text['system']['network']['in']['dropped'],text['system']['network']['in']['packets'],\
        text['system']['network']['in']['errors'],text['system']['network']['in']['bytes']]

        test_array = np.array(data)
        test_array = test_array.reshape(1,-1)
        test_array_std=load_scaler.transform(test_array)
        predictions=isolation.predict(test_array_std)
        mse = np.mean(np.power(test_array_std - predictions, 2), axis=1)
        error_df = pd.DataFrame({'reconstruction_error': mse}) 
        threshold = np.mean(mse) + np.std(mse)/2
        y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]
        print(y_pred)
        mse=str(mse).replace("[","").replace("]","")
        mse_data={"mse":str(mse)}
        producer.produce('mse', json.dumps(mse_data).encode('utf-8'))
        producer.flush()
    except KeyError:
        continue