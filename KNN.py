import numpy as np
import pandas
from sklearn.neighbors import KNeighborsClassifier

x = np.array([(1, 8, .15, 1, 1000, 5, "GOOD"), 
                (2, 15, .19, .9, 2500, 8 , "BAD"),
                (3, 10, .35, 1, 500, 10, "BAD"),
                (4, 11, .4, .95, 2000, 6, "BAD"),
                (5, 12, .1, .99, 3000, 6, "GOOD"),
                (6, 18, .15, 1, 2000, 5, "GOOD"),
                (7, 3, .21, 1, 1500, 7, "BAD"),
                (8, 14, .04, 1, 3500, 5, "GOOD"),
                (9, 13, .05, 1, 3000, 3, "GOOD"),
                (10, 6, .25, .94, 2800, 9, "BAD"),
                (11, 20, .5, .9, 4500, 12, 'P1'), 
                (12, 8, .1,1,550, 4, 'P2'),
                (13, 9, .13, .99, 3000, 6, 'P3')],
                dtype=[('id', int), ('Total Accounts', float), ('Utilization', float),
                        ('Payment History', float), ('Age of Account', float), ('Inquiries', float), ('Label', object)
                        ])
#predx = np.array([(11, 20, .5, .9, 4500, 12, 'P1'), (12, 8, .1,1,550, 4, 'P2'),
 #                   (13, 9, .13, .99, 3000, 6, 'P3')],  dtype=[('id', int), ('Total Accounts', float), ('Utilization', float),
  #                      ('Payment History', float), ('Age of Account', float), ('Inquiries', float), ('Label', object)])
df = pandas.DataFrame(x)
#predf = pandas.DataFrame(predx)
#['Total Accounts','Utilization', 'Payment History', 'Age of Account', 'Inquiries']
cols_to_norm = [x for x in df.columns if (x != 'Label' and x!= 'id')]

df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
#predf[cols_to_norm] = predf[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
#print df
predf = df[10:]
df = df[:10]
X_data = df[cols_to_norm]
Y_data = df['Label']

X_pred = predf[cols_to_norm]
knn = KNeighborsClassifier(n_neighbors=3,algorithm ='brute', p=1)
knn = knn.fit(X_data, Y_data)
ans = knn.predict(X_pred)


test_data_model = X_data[:6]
test_data = X_data[6:]
print "test_Data_model"
print test_data_model
print "test data"
print test_data

Y_test_data_model = Y_data[:6]
Y_test_data = Y_data[6:]



#knn = KNeighborsClassifier(n_neighbors=3,metric='l1')
#knn = knn.fit(X_data, Y_data)
#ans = knn.predict(X_pred)

knnSecond = KNeighborsClassifier(n_neighbors=3,algorithm ='brute', p=1)
knnSecond = knnSecond.fit(test_data_model, Y_test_data_model)
ansSecond = knnSecond.predict(test_data)
#ans_Test_Data = knnSecond.predict(X_pred)

#print ans_Test_Data
# 1 = .75
# 2 = 1
# 3,4 = .75

def accuracy(real, predict):
    return sum(real == predict) / float(real.shape[0])

print accuracy(Y_test_data, ansSecond)

print ans
