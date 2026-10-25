import math
import numpy as np

def getMol(gas):
    match gas:
        case "N2":
            return 28.014
        case "O2":
            return 31.998
        case "H2O":
            return 18.015
        case "H2":
            return 2.016
        case "air":
            return 28.9644
        case _:
            return -1.0

def Tt_T(gam, M):
    return 1 + ((gam - 1) / 2) * M**2

def Pt_P(gam, M):
    Ttr = Tt_T(gam, M)
    return Ttr**(gam / (gam - 1))

def rhot_rho(gam, M):
    Ttr = Tt_T(gam, M)
    return Ttr**(1 / (gam - 1))

def A_Astar(gam, M):
    Ttr = Tt_T(gam, M)
    return (1 / M) * (((gam + 1) / 2) / Ttr)**((gam + 1) / (2 - (2 * gam)))

def T_Tt(gam, M):
    Ttr = Tt_T(gam, M)
    return 1 / Ttr

def P_Pt(gam, M):
    Ptr = Pt_P(gam, M)
    return 1 / Ptr

def rho_rhot(gam, M):
    rhotr = rhot_rho(gam, M)
    return 1 / rhotr

def Astar_A(gam, M):
    Ar = A_Astar(gam, M)
    return 1 / Ar

def q_rhoV(rho, V):
    return 0.5 * rho * V**2

def q_gamPM(gam, P, M):
    return (gam / 2) * P * M**2

def getSoS(gam, Rs, T):
    return math.sqrt(gam * Rs * T)

def getRs(mol):
    return 8314.5 / mol

def getCp(gam, Rs):
    return (Rs / (gam - 1)) + Rs

def gam_T(gami, T):
    Theta = 3055 + (5 / 9)
    TT = Theta / T
    return 1 + ((gami - 1) / (1 + (gami - 1) * (TT**2 * (math.exp(TT) / (math.exp(TT) - 1)**2))))

def rhoIdeal(P, Rs, T):
    return P / (Rs * T)

def Pideal(rho, Rs, T):
    return rho * Rs * T

def Tideal(P, rho, Rs):
    return P / (rho * Rs)

def maxTheta(gam, M):
    thetaRad = (4 / (3 * math.sqrt(3) * (gam + 1))) * ((M**2 - 1)**1.5 / M**2)
    return math.degrees(thetaRad)

def normalPr(gam, M):
    return (2 * gam * M**2 - (gam - 1)) / (gam + 1)

def normalTr(gam, M):
    return ((2 * gam * M**2 - (gam - 1)) * ((gam - 1) * M**2 + 2)) / ((gam + 1)**2 * M**2)

def normalRhor(gam, M):
    return ((gam + 1) * M**2) / ((gam - 1) * M**2 + 2)

def normalMout(gam, M):
    return math.sqrt(((gam - 1) * M**2 + 2) / (2 * gam * M**2 - (gam - 1)))

def normalPtr(gam, M):
    rhor = normalRhor(gam, M)
    Pr = normalPr(gam, M)
    return rhor**(gam / (gam - 1)) * (Pr**(-1))**(1 / (gam - 1))

def obliqueTheta(gam, M, betaDeg):
    beta = math.radians(betaDeg)
    invertme = math.tan(beta) * ((((gam + 1) * M**2) / (2 * (M**2 * math.sin(beta)**2 - 1))) - 1)
    thetaRad = math.atan(invertme**(-1))
    return math.degrees(thetaRad)

def obliqueMout(gam, M, betaDeg, thetaDeg):
    beta = math.radians(betaDeg)
    theta = math.radians(thetaDeg)
    return math.sqrt(((gam - 1) * M**2 * math.sin(beta)**2 + 2) / (((2 * gam * M**2 * math.sin(beta)**2) - (gam - 1)) * math.sin(beta - theta)**2))

def obliquePr(gam, M, betaDeg):
    beta = math.radians(betaDeg)
    return (2 * gam * M**2 * math.sin(beta)**2 - (gam - 1)) / (gam + 1)

def obliqueTr(gam, M, betaDeg):
    beta = math.radians(betaDeg)
    return ((2 * gam * M**2 * math.sin(beta)**2 - (gam - 1)) * ((gam - 1) * M**2 * math.sin(beta)**2 + 2)) / ((gam + 1)**2 * M**2 * math.sin(beta)**2)

def obliqueRhor(gam, M, betaDeg):
    beta = math.radians(betaDeg)
    return ((gam + 1) * M**2 * math.sin(beta)**2) / ((gam - 1) * M**2 * math.sin(beta)**2 + 2)

def obliquePtr(gam, M, betaDeg):
    rhor = obliqueRhor(gam, M, betaDeg)
    Pr = obliquePr(gam, M, betaDeg)
    return rhor**(gam / (gam - 1)) * (Pr**(-1))**(1 / (gam - 1))

def obliqueBeta(gam, M, theta):
    betaRange = np.linspace(theta, 90.0, num=10000)
    candidates = []
    for x in betaRange:
        thetaCand = obliqueTheta(gam, M, x)
        if (abs(thetaCand - theta) < 0.1):
            thetaDiff = abs(thetaCand - theta)
            candTup = (x, thetaCand, thetaDiff)
            candidates.append(candTup)
            continue
        elif ((thetaCand - theta) > 1.0):
            break
        else:
            continue
    candidates.sort(key=lambda x: x[2])
    return candidates[0][0]

