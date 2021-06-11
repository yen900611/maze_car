import math

def cross_point(dot1, vec1, dot2, vec2):
    '''
    define line A and line B, write a function which can return the point two lines cross.
    dot_1 = (x1, y1)
    dot_2 = (x2, y2)
    vec_1 = (vx1, vy1)
    vec_2 = (vx2, vy2)
    line1 = [(x1, y1), (x1 + vx1, y1 + vy1)], line2 = [(x2, y2), (x2 + vx2, y2 + vy2)]
    '''
    x1 = dot1[0]
    y1 = dot1[1]
    x2 = dot2[0]
    y2 = dot2[1]
    vx1 = vec1[0]
    vy1 = vec1[1]
    vx2 = vec2[0]
    vy2 = vec2[1]
    if vx1 == 0:  # 如果斜率為0
        k1 = None
        b1 = 0
    else:
        k1 = vy1 * 1.0 / vx1
        b1 = (y1 + vy1) * 1.0 - (x1 + vx1) * k1 * 1.0
    if vx2 == 0:
        k2 = None
        b2 = 0
    else:
        k2 = vy2 * 1.0 / vx2
        b2 = (y2 + vy2) * 1.0 - (x2 + vx2) * k2 * 1.0

    if k1 == k2:
        return None
    elif k1 == None:  # 如果Line1斜率不存在，則取Line1上的點帶入Line2的公式
        x = x1 + vx1
        k1 = k2
        b1 = b2
    elif k2 == None:
        x = x2 + vx2
    else:
        x = (b2 - b1) * 1.0 / (k1 - k2)
    y = k1 * x * 1.0 + b1 * 1.0
    return (x, y)

def cross_point_dot(dot1, vec1, dot2, dot3):
    '''
    this function is same as above. But in this case, one of lines has starting point and ending point.
    If the point two line cross out of the line, function should return None.
    '''
    x2 = dot2[0]
    y2 = dot2[1]
    x3 = dot3[0]
    y3 = dot3[1]
    if vec1[0] == 0:
        vec1[0] = 0.1
    if x3 - x2 == 0:
        x3 += 0.1
    p = cross_point(dot1, vec1, dot2, (x3 - x2, y3 - y2))

    if p:
        if x2 -0.1 <= p[0] <= x3 + 0.1 or x3 - 0.1 <= p[0] <= x2 + 0.1:
            if y2 - 0.1 <= p[1] <= y3 + 0.1 or y3 - 0.1 <= p[1] <= y2 + 0.1:
                return p
            else:
                return None
    else:
        return None

if __name__ == '__main__':
    # p = cross_point((6.55931, -18.08653), (0.72216, 1.87358), (1.0, -12.0), (26.0, 0.0))
    # print(p)
    p = cross_point_dot((6.55931, -18.08654), (0.72215, 1.87358), (1.0, -12.0), (27.0, -12.0))
    print(p)
