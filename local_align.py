UP = (-1,0)
LEFT = (0, -1)
TOPLEFT = (-1, -1)
ORIGIN = (0, 0)

def traceback_local(v, w, M, init_i, init_j, pointers):
    i,j = init_i, init_j
    new_v = []
    new_w = []
    while True:
        di, dj = pointers[i][j]
        if (di,dj) == LEFT:
            new_v.append('-')
            new_w.append(w[j-1])
        elif (di,dj) == UP:
            new_v.append(v[i-1])
            new_w.append('-')
        elif (di,dj) == TOPLEFT:
            new_v.append(v[i-1])
            new_w.append(w[j-1])
        i, j = i + di, j + dj
        if (M[i][j] == 0):
            break
    return str(''.join(new_v[::-1])+'\n'+''.join(new_w[::-1])).split('\n')

"""
local_align(v,w,delta):
Returns the score of the maximum scoring alignment of all possible substrings of v and w.

:param: v
:param: w
:param: delta
"""
def local_align(v, w, delta):

    M = [[0 for j in range(len(w)+1)] for i in range(len(v)+1)]
    pointers = [[ORIGIN for j in range(len(w)+1)] for i in range(len(v)+1)]
    score = None
    init_i, init_j = 0,0
    ### BEGIN SOLUTION
    def get2dmax(M):
        maxval = -float("inf")
        max_i,max_j = 0,0
        for i in range(len(M)):
            rowmax = max(list(enumerate(M[i])), key = lambda x: (x[1],x[0]))
            if rowmax[1] >= maxval:
                maxval = rowmax[1]
                max_i = i
                max_j = rowmax[0]
        return maxval, (max_i, max_j)

    def smith_waterman(v, w, delta):
        for i in range(len(v)+1):
            for j in range(len(w)+1):
                if i == 0 or j == 0:
                    M[i][j] = 0
                else:
                    best_sub = max([(ORIGIN, 0),(LEFT, M[i][j-1] + delta['-'][w[j-1]]),
                                   (UP, M[i-1][j] + delta[v[i-1]]['-']),
                                   (TOPLEFT, M[i-1][j-1] + delta[v[i-1]][w[j-1]])], key = lambda x: x[1])
                    pointers[i][j] = best_sub[0]
                    M[i][j] = best_sub[1]
        return M, pointers
    M, pointers = smith_waterman(v,w,delta)
    init_i,init_j = get2dmax(M)[1]
    score = get2dmax(M)[0]
    ### END SOLUTION
    alignment = traceback_local(v, w, M, init_i, init_j , pointers)
    return score, alignment
