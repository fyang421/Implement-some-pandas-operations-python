import csv

# read data as dictionary
with open('.../transactions.txt') as file:
  transactions = csv.DictReader(file)
  transactions_ls = []
  for row in transactions:
    transactions_ls.append(row)

#####################################################################################
# Q1. Implement groupby sum

# build dictionary with total_transaction for each day
dic1 = {}
for r in transactions_ls:
  if r['transactionDay'] in dic1:
    dic1[r['transactionDay']] += float(r['transactionAmount'])
  else:
    dic1[r['transactionDay']] = float(r['transactionAmount'])

# write ouput
with open('q1.csv', 'w') as file:
  fields = ['day', 'total_transaction']
  writer = csv.DictWriter(file, fieldnames=fields)
  writer.writeheader()
  for key in dic1.keys():
    writer.writerow({'day':key, 'total_transaction': round(dic1[key], 2)})


#####################################################################################
#Q2. Implement groupby, mean, pivot

# build dictionary with sum and count for each account and each type of transaction
dic2 = {}
for r in transactions_ls:
  if r['accountId'] not in dic2:
    dic2[r['accountId']] = {}
    dic2[r['accountId']][r['category']] = [float(r['transactionAmount']), 1]
  else:
    if r['category'] not in dic2[r['accountId']]:
      dic2[r['accountId']][r['category']] = [float(r['transactionAmount']), 1]
    else:
      dic2[r['accountId']][r['category']] = [dic2[r['accountId']][r['category']][0] + float(r['transactionAmount']),
                                             dic2[r['accountId']][r['category']][1] + 1]

# update dictionary to avg for each account and each type of transaction
for i in dic2.keys():
  for j in dic2[i].keys():
    dic2[i][j] = dic2[i][j][0]/dic2[i][j][1]

# unique types of transaction
category_set = set()
for r in transactions_ls:
  category_set.add(r['category'])
category_set

# write output
with open('q2.csv', 'w') as file:
  fields = ['accountId', 'AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG']
  writer = csv.DictWriter(file, fieldnames=fields)
  writer.writeheader()
  for key in dic2.keys():
    writer.writerow({'accountId':key, 
                     'AA': round(dic2[key].get('AA', 0),2),
                     'BB': round(dic2[key].get('BB', 0),2),
                     'CC': round(dic2[key].get('CC', 0),2),
                     'DD': round(dic2[key].get('DD', 0),2),
                     'EE': round(dic2[key].get('EE', 0),2),
                     'FF': round(dic2[key].get('FF', 0),2),
                     'GG': round(dic2[key].get('GG', 0),2)})



#####################################################################################

#Q3. Implement rolling window, groupby, mean, max, sum, pivot
# unique days of transaction
day_set = set()
for r in transactions_ls:
  day_set.add(int(r['transactionDay']))

# unique accountId
accountId_set = set()
for r in transactions_ls:
  accountId_set.add(r['accountId'])

dic3 = {}
for d in day_set:
  # extract the rolling time window of transactions for previous 5 days of day d
  if d >= 2:
    def day(row):
      return (int(row['transactionDay']) < d and int(row['transactionDay']) >= d-5)
    transaction_d = list(filter(day, transactions_ls))

    # build dictionary with required statistics for day d
    dic3[d] = {}
    for i in transaction_d:
      if i['accountId'] not in dic3[d]:
        dic3[d][i['accountId']] = {'max' : float(i['transactionAmount']),
                                  'avg': float(i['transactionAmount']),
                                  'sum': float(i['transactionAmount']),
                                  'count': 1,
                                  'AAtotal': float(i['transactionAmount']) if i['category'] == 'AA' else 0,
                                  'CCtotal': float(i['transactionAmount']) if i['category'] == 'CC' else 0,
                                  'FFtotal': float(i['transactionAmount']) if i['category'] == 'FF' else 0}
      else:
        dic3[d][i['accountId']]['max'] = max(dic3[d][i['accountId']]['max'], float(i['transactionAmount']))
        dic3[d][i['accountId']]['avg'] = (dic3[d][i['accountId']]['sum'] + float(i['transactionAmount']))/(dic3[d][i['accountId']]['count'] + 1)
        dic3[d][i['accountId']]['sum'] += float(i['transactionAmount'])
        dic3[d][i['accountId']]['count'] += 1
        if i['category'] == 'AA':
          dic3[d][i['accountId']]['AAtotal'] += float(i['transactionAmount'])
        if i['category'] == 'CC':
          dic3[d][i['accountId']]['CCtotal'] += float(i['transactionAmount'])
        if i['category'] == 'FF':
          dic3[d][i['accountId']]['FFtotal'] += float(i['transactionAmount'])
    
    for accountId in accountId_set:
      if accountId not in dic3[d].keys():
        dic3[d][accountId] = {}
        dic3[d][accountId]['max'] = 0
        dic3[d][accountId]['avg'] = 0
        dic3[d][accountId]['AAtotal'] = 0
        dic3[d][accountId]['CCtotal'] = 0
        dic3[d][accountId]['FFtotal'] = 0

# write output
with open('q3_2.csv', 'w') as file:
  fields = ['day', 'accountId', 'max', 'avg', 'AAtotal', 'CCtotal', 'FFtotal']
  writer = csv.DictWriter(file, fieldnames=fields)
  writer.writeheader()
  for day in dic3.keys():
    for accountId in dic3[day].keys():
      writer.writerow({'day': day,
                      'accountId': accountId,
                      'max': round(dic3[day][accountId].get('max'), 2),
                      'avg': round(dic3[day][accountId].get('avg'), 2),
                      'AAtotal': round(dic3[day][accountId].get('AAtotal'), 2),
                      'CCtotal': round(dic3[day][accountId].get('CCtotal'), 2),
                      'FFtotal': round(dic3[day][accountId].get('FFtotal'), 2)})
