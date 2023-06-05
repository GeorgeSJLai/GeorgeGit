import pickle
pickleFile=r'c:\users\george\H610.pickle'
with open(pickleFile,'rb') as f:
    d1=pickle.load(f)
    d2=pickle.load(f)
    d3=pickle.load(f)
    d4=pickle.load(f)
    d5=pickle.load(f)
print(d1)
print(d2)
print(d3)
print(d4)
print(d5)
with open(pickleFile,'wb') as f:
    pickle.dump(d1,f)
    pickle.dump(d2,f)
    pickle.dump(d3,f)
    pickle.dump(d4,f)
    pickle.dump(d5,f)