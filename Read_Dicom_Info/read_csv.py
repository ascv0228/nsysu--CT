import csv
results = {}
with open('patient_xyz.csv',newline='') as pscfile:
    reader = csv.DictReader(pscfile)
    for row in reader:
        results[row['Patient']] = (float(row['x']),float(row['y']),float(row['z']))

P = []
G = []
L = []
M = []
for i in results.keys():
    if i[-2:] == '-P':
        P.append(i[:-2])
    elif i[-2:] == '-G':
        G.append(i[:-2])
    elif i[-2:] == '-L':
        L.append(i[:-2])
    elif i[-2:] == '-M':
        M.append(i[:-2])

print(P)
print(G)
print(L)
print(M)