def LPS(S):
    """ find longest palindromes
    """
    if len(S) == 0: return 0
    elif len(S) == 1: return 1
    else:
        if S[0] == S[-1]: return 2 + LPS(S[1:-1])
        else:
            front = LPS(S[1:])
            end = LPS(S[:-1])
            return max(front,end)

def superLCS(S1,S2):
    """ find longest LCS
    """
    