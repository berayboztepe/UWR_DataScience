def mult_table(x1, x2, y1, y2, d):
    x_values = [x1 + i * d for i in range(int((x2 - x1) / d) + 1)]
    y_values = [y1 + i * d for i in range(int((y2 - y1) / d) + 1)]

    print(x_values)
    print(y_values)
    
    for x in range(int(x1) - 1, int(x2)+1):
        if x == int(x1) - 1:
            print(end='\t')
        else:
            print(float(x), end="\t")
    
    print()
    for y in range(len(y_values)):
        print(y_values[y], end="\t") 
        for x in x_values:
            print(x*y_values[y], end="\t")
        print()

mult_table(3.0, 5.0, 2.0, 4.0, 1.0)
mult_table(-3.0,5.0,2.0345, 4.0, 1.0)

