UP = (-1,0)
LEFT = (0, -1)
TOPLEFT = (-1, -1)
ORIGIN = (0, 0)

def traceback_global(v, w, pointers):
    i,j = len(v), len(w)
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
        if (i <= 0 and j <= 0):
            break
    return str(''.join(new_v[::-1])+'\n'+''.join(new_w[::-1])).split('\n')


"""
global_align(v,w,delta):
Returns the score of the maximum scoring alignment of the strings v and w, as well as the actual alignment as
computed by traceback_global.

:param: v
:param: w
:param: delta
"""
def global_align(v, w, delta):

    M = [[0 for j in range(len(w)+1)] for i in range(len(v)+1)]
    pointers = [[ORIGIN for j in range(len(w)+1)] for i in range(len(v)+1)]
    score, alignment = None, None
    ### BEGIN SOLUTION
    def needleman(v,w, delta):
        for i in range(len(v)+1):
            for j in range(len(w)+1):
                if i == 0 and j == 0:
                    M[i][j] = 0
                elif i == 0:
                    M[i][j] = M[i][j-1] + delta['-'][w[j-1]]
                    pointers[i][j] = LEFT
                elif j == 0:
                    M[i][j] = M[i-1][j] + delta[v[i-1]]['-']
                    pointers[i][j] = UP
                else:
                    best_sub = max([(LEFT, M[i][j-1] + delta['-'][w[j-1]]),
                                   (UP, M[i-1][j] + delta[v[i-1]]['-']),
                                   (TOPLEFT, M[i-1][j-1] + delta[v[i-1]][w[j-1]])], key = lambda x: x[1])
                    pointers[i][j] = best_sub[0]
                    M[i][j] = best_sub[1]
        return M, pointers
    M, pointers = needleman(v,w,delta)
    score = M[len(v)][len(w)]
    ### END SOLUTION
    alignment = traceback_global(v,w, pointers)
    return score, alignment
