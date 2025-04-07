def where_to_turn(point_a, point_b, point_c):
    xa, ya = point_a
    xb, yb = point_b
    xc, yc = point_c
    cross_product = (xb - xa) * (yc - yb) - (yb - ya) * (xc - xb)
    
    if cross_product > 0:
        print("LEFT")
    elif cross_product < 0:
        print("RIGHT")
    else:
        print("TOWARDS")

if __name__ == '__main__':
    point_a = tuple(map(int, input().split()))
    point_b = tuple(map(int, input().split()))
    point_c = tuple(map(int, input().split()))
    where_to_turn(point_a, point_b, point_c)
