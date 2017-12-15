import numpy as np
import pickle
import matplotlib.pyplot as plt
import time

def hasher(size):
    random_vector = np.random.normal(size=size)
    for l in range(size):
        if random_vector[l]<0:
            random_vector[l] = -1
        else:
            random_vector[l] = 1
    return random_vector

def projection(data,hash_functions,r,b):
    temp = {}
    for l in data:
        for j in hash_functions:
            if j[0] not in temp:
                temp[j[0]] = 0
            temp[j[0]] += j[1][l[1]]*l[2]
    result = {}
    for l in range(b*r):
        if temp[l]>0:
            temp[l] = "1"
        else:
            temp[l] = "0"
        c = l%r
        if c not in result:
            result[c]=""
        result[c]+=temp[l]
    return result.items()

def cosine(a,b):
    i = 0
    j = 0
    s = 0
    p = 0
    q = 0
    while i<len(a) and j<len(b):
        if int(a[i][0])==int(b[j][0]):
            p+=(a[i][1]**2)
            q+=(b[j][1]**2)
            s+=(a[i][1]*b[j][1])
            i+=1
            j+=1
        elif int(a[i][0])>int(b[j][0]):
            j+=1
        else:
            i+=1
    if p==0 or q==0:
        return 0.0
    return s*1.0/(p**0.5 * q**0.5)

def user_predictions(user,items,user_data,item_data,user_hashes,hash_tables_users):
    k_values = 15
    err = [0.0]*k_values
    c = 0
    ann = set()
    for l in user_hashes:
        for k in hash_tables_users[l]:
            if k!=l:
                ann.add(k)
    similarities = {}
    for k in ann:
        similarities[k] = cosine(user_data[k],user_data[user])
    
    predicted_values = []
    for item,rating in items:
        temp = []
        num = [0]*k_values
        den = [0]*k_values
        if item not in item_data:
            continue
        for user in ann:
            if user in item_data[item]:
                temp.append((similarities[k],item_data[item][user]))
        temp = sorted(temp,key=lambda x:x[0], reverse=True)
        order = 0
        for l in temp:
            order+=1
            for j in range(k_values):
                if order<=10*(j+1):
                    num[j] += l[0]*l[1]
                    den[j] += l[0]
            if order>=10*k_values:
                break
        item_prediction = []
        for j in range(k_values):
            if den[j]>0:
                err[j]+=(rating - (num[j]*1.0/den[j]))**2
                c+=1
                item_prediction.append(num[j]*1.0/den[j])
        predicted_values.append((item,item_prediction))
    return predicted_values

from pyspark import SparkContext,SparkConf
conf = SparkConf().setAppName("LSH").setMaster("local[8]")\
        .set("spark.driver.memory","10g").set("spark.driver.cores","8")\
        .set("spark.executor.cores","8").set("spark.executor.memory","10g")\
        .set("spark.memory.fraction","0.6").set("spark.memory.storageFraction","0.5")\
        .set("spark.executor.extraJavaOptions","-XX:+UseG1GC -Xms10g -Xmn10g")
sc = SparkContext(conf=conf)

for i in range(1,5):

    data = sc.textFile('train_'+str(i)+'.csv').map(lambda line: line.split(","))\
                .map(lambda token: (int(token[0]),int(token[1]),float(token[2]))).groupBy(lambda line: line[0])\
                .map(lambda x : (x[0], list(x[1]))).cache()
    print data.count()

    f = open('train_'+str(i)+'.csv')
    lines = f.readlines()
    user_data = {}
    users = {}
    items = {}
    item_data = {}
    for line in lines:
        user,item,rating = line.strip().split(',')
        if int(user) not in user_data:
            user_data[int(user)] = []
        if int(item) not in item_data:
            item_data[int(item)] = {}
        item_data[int(item)][int(user)] = float(rating)
        users[int(user)] = 0
        items[int(item)] = 0
        user_data[int(user)].append((int(item),float(rating)))
    print len(user_data),min(users),min(items),max(users),max(items)

    for user in user_data:
        user_data[user] = sorted(user_data[user],key=lambda x:x[0])
        user_data[user] = np.array(user_data[user])

    b = 7
    r = 10

    start = time.time()
    hash_list = []
    item_size = 26744
    for z in range(b*r):
        hash_list.append(hasher(item_size+1))
    hash_functions = list(enumerate(hash_list))

    user_hashes = data.map(lambda x: (x[0],projection(x[1],hash_functions,r,b)))
    print user_hashes.count()
    end = time.time()
    print end-start

    start = time.time()
    user_hashes_dict = user_hashes.collectAsMap()
    end = time.time()
    print end-start

    hash_tables_users = {}
    for l in user_hashes_dict:
        for j in user_hashes_dict[l]:
            if j not in hash_tables_users:
                hash_tables_users[j] = []
            hash_tables_users[j].append(l)

    f = open('split_'+str(1+(i+2)%4)+'.csv')
    lines = f.readlines()
    test_data_dict = {}
    for line in lines:
        user,item,rating = line.strip().split(',')
        if int(user) not in test_data_dict:
            test_data_dict[int(user)] = []
        test_data_dict[int(user)].append((int(item),float(rating)))

    predictions = {}
    partial_test_users = np.random.choice(user_data.keys(),int(len(user_data)*0.01))
    c = 0
    start = time.time()
    for user in partial_test_users:
        if c%10==0 and c>0:
            end = time.time()
            print c,(end-start)*1.0/c
        c+=1
        predictions[user] = user_predictions(user,test_data_dict[user],user_data,item_data,user_hashes_dict[user],hash_tables_users)

    pickle.dump(predictions,open('predictions_'+str(b)+'_'+str(r)+'_'+str(i)+'.dat','wb'))