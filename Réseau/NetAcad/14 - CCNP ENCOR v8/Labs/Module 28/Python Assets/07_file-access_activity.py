file = open("devices.txt","a")
while True:
    newItem = input("Enter device name: ")
    if newItem == "exit":
        print("All done!")
        file.close()
        break
    file.write(newItem + "\n")
