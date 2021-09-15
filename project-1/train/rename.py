import os 
for x in os.listdir("out1"):
    if ".jpg" in x:
        print("out1/"+x.replace(".jpg","_predicted"))
        os.rename("out1/"+x,"out1/"+x.replace(".jpg","_predicted"))

