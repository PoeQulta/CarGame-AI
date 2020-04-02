def is_left(P0, P1, P2):
    return (P1[0] - P0[0]) * (P2[1] - P0[1]) - (P2[0] - P0[0]) * (P1[1] - P0[1])

def wn_PnPoly(P, V):
    wn = 0   # the winding number counter

    # repeat the first vertex at end
    V = tuple(V[:]) + (V[0],)

    # loop through all edges of the polygon
    for i in range(len(V)-1):     # edge from V[i] to V[i+1]
        if V[i][1] <= P[1]:        # start y <= P[1]
            if V[i+1][1] > P[1]:     # an upward crossing
                if is_left(V[i], V[i+1], P) > 0: # P left of edge
                    wn += 1           # have a valid up intersect
        else:                      # start y > P[1] (no test needed)
            if V[i+1][1] <= P[1]:    # a downward crossing
                if is_left(V[i], V[i+1], P) < 0: # P right of edge
                    wn -= 1           # have a valid down intersect
    return wn