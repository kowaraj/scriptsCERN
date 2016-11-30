from math import sqrt,pi
print ''


def calc_ftw(h):
    c = 299792458

    f_rf = 199.928e+6 * h / 4620
    print 'f_rf    = ', f_rf

    F_rev = c / (2 * pi * 1100.0093)
    F_inf = h * F_rev 
    print 'F_inf   = ', F_inf

    cfp_cal = 0.0078125 
    cfp = ( F_inf - f_rf + pow(2,20)  )*cfp_cal
    cfp = int(round(cfp))
    print 'cfp     = ', cfp

    cfp_gain = 998200
    cfp_off = 920767342
    ftw = cfp_off - cfp * cfp_gain / pow(2,9)
    print 'ftw     = ', ftw, ' hex: ', hex(int(round(ftw)))

    return ftw

def calc_rf_master(ftw):
    f_rf_master = ftw * 5e+8 / pow(2,32) + 2.5e+8
    print 'f_rf_master = ', f_rf_master 
    return f_rf_master

h = 4620
f_rf_master = calc_rf_master(calc_ftw(h))
print ''

h = 4653
f_rf_master = calc_rf_master(calc_ftw(h))

#f_rf = 199.928000e+6
#f_rf = 201.928000e+6
# f_rf_m1 = calc_rf_master(calc_ftw(201e+6))
# f_rf_m1 = calc_rf_master(calc_ftw(199e+6))


