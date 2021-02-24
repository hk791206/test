import os

filelog = open("train.txt", "w")

# for i in range(400):
#     if i<10:
#         filelog.write("00%d"%(i))
#         filelog.write("\n")
#     elif 10<=i<100:
#         filelog.write("0%d"%(i))
#         filelog.write("\n")
#     elif i>=100:
#         filelog.write("%d"%(i))
#         filelog.write("\n") 

# You can change the folder path!!!
dir_path = 'C:/Users/nchupmml705/PycharmProjects/keras_YOLOv3/dataset/train/'
# Read and sort images
lines = os.listdir(dir_path)
lines.sort()

for i,line in enumerate(lines[:-1]):
    print(i, line[:-4])
    filelog.write(line[:-4])
    filelog.write("\n")