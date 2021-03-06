import pandas as pd

numRecordsMeso = 500
iter = 4

numRecordsThermo = 575

mergedDf = pd.read_csv('MergedData.csv')
mesoDf = mergedDf[mergedDf['label'] == 0]
thermoDf = mergedDf[mergedDf['label'] == 1]
print(mesoDf.shape[0])
print(thermoDf.shape[0])

mesoDfsCV = []
for i in range(iter):
    mesoSubset = mesoDf.sample(n=numRecordsMeso, replace=False, random_state=42)
    mesoDfsCV.append(mesoSubset)
    mesoDf = mesoDf.drop(mesoSubset.index)

thermoDfCV = thermoDf.sample(n=numRecordsThermo, replace=False, random_state=42)
thermoDf = thermoDf.drop(thermoDfCV.index)

for i in range(iter):
    tempDf = pd.concat([mesoDfsCV[i], thermoDfCV])
    tempDf.to_csv('MergedBalancedSubset_' + str(i) + '.csv', index=False)

print('Done')
