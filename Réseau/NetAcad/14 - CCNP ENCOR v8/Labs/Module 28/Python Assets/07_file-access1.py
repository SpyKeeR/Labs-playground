devices=[]
file=open("devices.txt","r")
for item in file:
    devices.append(item.strip())
file.close()
print(devices)
