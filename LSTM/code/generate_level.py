import os
from textToImage import CIM
import sys
        
text_level_folder = "../levels_prediction_textfiles/"
new_img_level_folder = "../Generated_levels/"

predicted_level = sys.argv[1]

for z in range(1,50):
    predicted_level = sys.argv[1]

    r = open(text_level_folder + os.path.splitext(predicted_level)[0] + "_new_"+str(z)+".txt", "r")
    f = open(new_img_level_folder + os.path.splitext(predicted_level)[0] + "_new_"+str(z) +"_upRight.csv", "w")

    text = ""
    w, h = 213, 13;
    itr = 0
    copy = 0
    trans = [[0 for x in range(h)] for y in range(w)]
    for i in range(0, 213):
            text= r.readline()
            for c in text:
                if(copy == 13): break
                trans[i][copy] = c
                copy += 1
            text = ""
            copy = 0

    r.close()
    # print(trans)

    for i in range(0,13):
            for j in range(0,213):
                text += trans[j][i]
            f.write(text)
            f.write("\n")
            text = ""
    f.close()
    predicted_level_n =  "mario-1-1-edited_trans_new_"+str(z)+".txt"
    csv_pred = "mario-1-1-edited_trans_new_"
    CIM(new_img_level_folder + csv_pred  +str(z)+ "_upRight.csv", predicted_level_n)