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

from pyspark import SparkContext,SparkConf
conf = SparkConf().setAppName("LSH").setMaster("local[8]")\
        .set("spark.driver.memory","10g").set("spark.driver.cores","8")\
        .set("spark.executor.cores","8").set("spark.executor.memory","10g")\
        .set("spark.memory.fraction","0.6").set("spark.memory.storageFraction","0.5")\
        .set("spark.executor.extraJavaOptions","-XX:+UseG1GC -Xms10g -Xmn10g")
sc = SparkContext(conf=conf)

data = sc.textFile('train.csv').map(lambda line: line.split(","))\
            .map(lambda token: (int(token[0]),int(token[1]),float(token[2]))).groupBy(lambda line: line[0])\
            .map(lambda x : (x[0], list(x[1]))).cache()
print data.count()

f = open('train.csv')
lines = f.readlines()
user_data = {}
users = {}
items = {}
for line in lines:
    user,item,rating = line.strip().split(',')
    if int(user) not in user_data:
        user_data[int(user)] = []
    users[int(user)] = 0
    items[int(item)] = 0
    user_data[int(user)].append((int(item),float(rating)))
print len(user_data),min(users),min(items),max(users),max(items)

for user in user_data:
    user_data[user] = sorted(user_data[user],key=lambda x:x[0])
    user_data[user] = np.array(user_data[user])

test_users = np.random.choice(user_data.keys(),20)
print len(test_users)

users_rdd = sc.parallelize(users.keys())

for b in range(2,11):
    for r in range(2,11):

        r = 2*r
        start = time.time()
        hash_list = []
        item_size = 26744
        for i in range(b*r):
            hash_list.append(hasher(item_size+1))
        hash_functions = list(enumerate(hash_list))

        user_hashes = data.map(lambda x: (x[0],projection(x[1],hash_functions,r,b)))
        print user_hashes.count()
        end = time.time()
        print end-start

        start = time.time()
        user_hashes_dict = user_hashes.collectAsMap()
        pickle.dump(user_hashes_dict,open('result_'+str(b)+'_'+str(r)+'_py.dat','wb'))
        end = time.time()
        print end-start

        hash_tables_users = {}
        for l in user_hashes_dict:
            for j in user_hashes_dict[l]:
                if j not in hash_tables_users:
                    hash_tables_users[j] = []
                hash_tables_users[j].append(l)

        # reverse_hash = user_hashes.flatMap(lambda x: [(i,x[0]) for i in x[1]]).groupBy(lambda x:x[0])
        # print reverse_hash.count()

        # for test_user in test_users:
        #     all_similarities = users_rdd.map(lambda x: (x,cosine(user_data[x],user_data[test_user])))

        # test_user_hashes = user_hashes.filter(lambda x: x in test_users)
        # test_user_hashes_df = test_user_hashes.toDF()

        count = 0
        true_positives = {}
        predicted = {}
        positive = {}
        for user in test_users:

            count+=1
            print user,count

            temp = {}
            start = time.time()
            for friend in user_data:
                if friend in test_users:
                    continue
                cs = cosine(user_data[user],user_data[friend])
                temp[friend] = cs

            ann = set()
            for k in user_hashes_dict[user]:
                for friend in hash_tables_users[k]:
                    if friend not in test_users:
                        ann.add(friend)
            print len(ann),len(temp)

            for threshold in [0.8,0.83,0.85,0.87,0.9]:

                temp_tp = 0
                temp_p = 0
                if threshold not in true_positives:
                    true_positives[threshold] = 0
                    positive[threshold] = 0
                    predicted[threshold] = 0

                for l in temp:
                    if temp[l]>=threshold:
                        positive[threshold]+=1
                        temp_p+=1
                        if l in ann:
                            temp_tp+=1

                print temp_tp*1.0/temp_p, temp_tp*1.0/len(ann)
                true_positives[threshold]+=temp_tp
                predicted[threshold]+=len(ann)
            end = time.time()
            print end-start

        for threshold in [0.8,0.83,0.85,0.87,0.9]:
            print threshold,true_positives[threshold]*1.0/positive[threshold],true_positives[threshold]*1.0/predicted[threshold]