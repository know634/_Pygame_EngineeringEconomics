num = 4
#可以批量生产
for i in range(num):
    json = {"x": 2532 + 50 * (i), "y": 366, "type": 1}

    print(str(json).replace("\'", "\""), end=",\n\t\t")
