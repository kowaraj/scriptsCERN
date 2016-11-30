
def ftw1(fcav, frev):
    FTW1 = pow(2,19) * fcav / frev
    return FTW1

def ftw2(ftw1, h):
    FTW2 = pow(2,20) * h - ftw1
    return FTW2

def to_dds(ftw):
    FTW1 = pow(2,19) * fcav / frev
    return FTW1

def sum_ftw_prime(h):
    return pow(2,33) - pow(2,20)* h

