import math

#Ns is American
def centrifugalTPeff_NASA(Ns, psi):
    def f2(x):
        a = (1.26949 * 10**(-14)) * x**4
        b = (2.05646 * 10**(-10)) * x**3
        c = 0.00000115809 * x**2
        d = 0.0230073 * x
        return a - b - c + d + 13.44883
    def f4(x):
        a = (3.08992 * 10**(-15)) * x**4
        b = (3.63925 * 10**(-10)) * x**3
        c = 0.00000718233 * x**2
        d = 0.036644 * x
        return -a + b - c + d + 30.90883
    def f6a(x):
        a = (3.52657 * 10**(-9)) * x**3
        b = 0.0000255838 * x**2
        c = 0.101172 * x
        return -a - b + c #+0
    def f6b(x):
        a = (0.00121064 * x) - 1.95137
        return 1.43253 * math.sin(a) + 80.57608
    def f6c(x):
        a = -(0.00111024 * x) + 6.2494
        return 86.89636 / (1 + math.exp(-a))
    def f6(x):
        if (x <= 1270):
            return f6a(x)
        elif (x > 1270) and (x <= 3095.87185):
            return f6b(x)
        elif (x > 3095.87185):
            return f6c(x)
    def f8(x):
        a = (1.1833 * 10**(-13)) * x**4
        b = (2.10513 * 10**(-9)) * x**3
        c = 0.0000175735 * x**2
        d = 0.0503068 * x
        return -a + b - c + d + 34.31181
    def c2(x):
        if (x <= 0.2):
            return 1.0
        elif (x > 0.2) and (x <= 0.4):
            return (-5 * (x - 0.2)) + 1.0
        elif (x > 0.4):
            return 0.0
    def c4(x):
        if (x <= 0.2):
            return 0.0
        elif (x > 0.2) and (x <= 0.4):
            return (5 * (x - 0.4)) + 1.0
        elif (x > 0.4) and (x <= 0.6):
            return (-5 * (x - 0.4)) + 1.0
        elif (x > 0.6):
            return 0.0
    def c6(x):
        if (x <= 0.4):
            return 0.0
        elif (x > 0.4) and (x <= 0.6):
            return (5 * (x - 0.6)) + 1.0
        elif (x > 0.6) and (x <= 0.8):
            return (-5 * (x - 0.6)) + 1.0
        elif (x > 0.8):
            return 0.0
    def c8(x):
        if (x <= 0.6):
            return 0.0
        elif (x > 0.6) and (x <= 0.8):
            return (5 * (x - 0.8)) + 1.0
        elif (x > 0.8):
            return 1.0
    #x = Ns
    return (c2(psi) * f2(Ns)) + (c4(psi) * f4(Ns)) + (c6(psi) * f6(Ns)) + (c8(psi) * f8(Ns))
