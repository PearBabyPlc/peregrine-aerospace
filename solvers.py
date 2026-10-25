import math
import numpy as np
import formulaegg as egg

rEarth = 6356766.0
g = 9.80665
molAir = 28.9644
Runiv = 8314.46
RsAir = Runiv / molAir
gamiAir = 1.4

def getISA(geom):
    H = (rEarth * geom) / (rEarth + geom)
    if (H < 11000):
        T = 288.15 + (-0.0065 * H)
        P = 101325.0 * (288.15 / T)**((g * molAir) / (Runiv * -0.0065))
    elif (H >= 11000) and (H < 20000):
        T = 216.65
        P = 22632.6352091 * math.exp((-g * molAir * (H - 11000)) / (Runiv * 216.65))
    elif (H >= 20000) and (H < 32000):
        T = 216.65 + (0.001 * (H - 20000))
        P = 5475.15769257 * (216.65 / T)**((g * molAir) / (Runiv * 0.001))
    elif (H >= 32000) and (H < 47000):
        T = 228.65 + (0.0028 * (H - 32000))
        P = 868.088257003 * (228.65 / T)**((g * molAir) / (Runiv * 0.0028))
    elif (H >= 47000) and (H < 51000):
        T = 270.65
        P = 110.919037481 * math.exp((-g * molAir * (H - 47000)) / (Runiv * 270.65))
    elif (H >= 51000) and (H < 71000):
        T = 270.65 + (-0.0028 * (H - 51000))
        P = 66.9471267903 * (270.65 / T)**((g * molAir) / (Runiv * -0.0028))
    elif (H >= 71000) and (H < 84852):
        T = 214.65 + (-0.002 * (H - 71000))
        P = 3.95709671594 * (214.65 / T)**((g * molAir) / (Runiv * -0.002))
    elif (H >= 84852) and (H < 90000):
        T = 186.95
        P = 0.373462257454 * math.exp((-g * molAir * (H - 84852)) / (Runiv * 186.95))
    elif (H >= 90000):
        T = 186.95 + (0.004 * (H - 90000))
        P = 0.145778536657 * (186.95 / T)**((g * molAir) / (Runiv * 0.004))
    rho = P / (T * RsAir)
    return P, T, rho

class Shockwave:
    def __init__(self, type, theta, beta, Ptr):
        self.type = str(type)
        self.theta = float(theta)
        self.beta = float(beta)
        self.Ptr = float(Ptr)

    def __str__(self):
        return f"Type: {self.type} shock\nDeflection: {self.theta} deg\nShock angle: {self.beta}\nStagnation pressure ratio: {self.Ptr}"

class Station:
    def __init__(self, note, M, P, T, rho, gam, Pt, Tt, mol, Rs, Cp, SoS, V, mdot, A):
        self.note = str(note)
        self.M = float(M)
        self.P = float(P)
        self.T = float(T)
        self.rho = float(rho)
        self.gam = float(gam)
        self.Pt = float(Pt)
        self.Tt = float(Tt)
        self.mol = mol
        self.Rs = float(Rs)
        self.Cp = float(Cp)
        self.SoS = float(SoS)
        self.V = float(V)
        self.mdot = float(mdot)
        self.A = float(A)

    def __str__(self):
        if self.P > 100000.0:
            Pee = self.P / 100000.0
            strP = f"{Pee} bar"
        else:
            strP = f"{self.P} Pa"
        if self.Pt > 100000.0:
            Pet = self.Pt / 100000.0
            strPt = f"{Pet} bar"
        else:
            strPt = f"{self.Pt} Pa"
        strMol = self.mol.get("avg")
        return f"{self.note}\nM: {self.M}\nP: {strP}\nT: {self.T} K\nrho: {self.rho} kg/m3\ngam: {self.gam}\nPt: {strPt}\nTt: {self.Tt}\nmol: {strMol} g\nRs: {self.Rs}\nCp: {self.Cp} J/kg-K\nSoS: {self.SoS}\nV: {self.V} m/s\nmdot: {self.mdot}kg/s\nA: {self.A}m2"

    def summary(self):
        print(f"M: {self.M}\nP: {self.P}\nT: {self.T}\nrho: {self.rho}\nV: {self.V}\nmdot: {self.mdot}\nA: {self.A}")

    def getAmbientConds(self, alt):
        Pres, Temp, Dens = getISA(alt)
        self.P = Pres
        self.T = Temp
        self.rho = Dens
        self.gam = egg.gam_T(gamiAir, Temp)
        self.mol.update({"avg": molAir})
        self.Rs = RsAir
        self.Cp = egg.getCp(self.gam, RsAir)
        self.SoS = egg.getSoS(self.gam, RsAir, Temp)

    def setMach(self, Mach):
        self.M = Mach
        self.Pt = self.P * egg.Pt_P(self.gam, Mach)
        self.Tt = self.T * egg.Tt_T(self.gam, Mach)
        self.V = self.SoS * Mach

    def setVelocity(self, Vel):
        self.V = Vel
        self.M = Vel / self.SoS
        self.Pt = self.P * egg.Pt_P(self.gam, self.M)
        self.Tt = self.T * egg.Tt_T(self.gam, self.M)

    def updateArea(self):
        self.A = self.mdot / (self.V * self.rho)

    def setMdot(self, massflow):
        self.mdot = massflow
        self.updateArea()

    def setArea(self, area):
        self.A = area
        self.mdot = area * self.V * self.rho

    def getAvgMol(self):
        totalStuff = 0.0
        totalMass = 0.0
        for x in self.mol.items():
            if x[0] != "avg":
                totalStuff += x[1]
                xMol = egg.getMol(x[0])
                totalMass += x[1] * xMol
        avgMol = totalMass / totalStuff
        self.mol.update({"avg": avgMol})

    def getHeatCapacity(self):
        self.gam = egg.gam_T(gamiAir, self.T)
        self.Rs = Runiv / self.mol.get("avg")
        self.Cp = egg.getCp(self.gam, self.Rs)

    def getTstatic(self):
        self.T = self.Tt * egg.T_Tt(self.gam, self.M)
        self.getHeatCapacity()

    def getPstatic(self):
        self.P = self.Pt * egg.P_Pt(self.gam, self.M)

    def getRhoIdeal(self):
        self.rho = self.P / (self.Rs * self.T)
        self.updateArea()

    def getPideal(self):
        self.P = self.rho * self.Rs * self.T

    def getTideal(self):
        self.T = self.P / (self.rho * self.Rs)
        self.getHeatCapacity()

    def updateMach(self, Mach):
        self.M = Mach
        self.getPstatic()
        self.getTstatic()
        self.getRhoIdeal()
        self.getHeatCapacity()
        self.setMach(Mach)

    def doNormalShock(self):
        self.P *= egg.normalPr(self.gam, self.M)
        self.T *= egg.normalTr(self.gam, self.M)
        self.rho *= egg.normalRhor(self.gam, self.M)
        self.Pt *= egg.normalPtr(self.gam, self.M)
        prevM = self.M
        self.M = egg.normalMout(self.gam, prevM)
        self.gam = egg.gam_T(gamiAir, self.T)
        self.Cp = egg.getCp(self.gam, self.Rs)
        self.Tt = self.T * egg.Tt_T(self.gam, self.M)
        self.SoS = egg.getSoS(self.gam, self.Rs, self.T)
        self.V = self.M * self.SoS
        self.updateArea()

    def doObliqueShock_getBeta(self, theta):
        beta = egg.obliqueBeta(self.gam, self.M, theta)
        self.P *= egg.obliquePr(self.gam, self.M, beta)
        self.T *= egg.obliqueTr(self.gam, self.M, beta)
        self.rho *= egg.obliqueRhor(self.gam, self.M, beta)
        self.Pt *= egg.obliquePtr(self.gam, self.M, beta)
        prevM = self.M
        self.M = egg.obliqueMout(self.gam, prevM, beta, theta)
        self.gam = egg.gam_T(gamiAir, self.T)
        self.Cp = egg.getCp(self.gam, self.Rs)
        self.Tt = self.T * egg.Tt_T(self.gam, self.M)
        self.SoS = egg.getSoS(self.gam, self.Rs, self.T)
        self.V = self.M * self.SoS
        self.updateArea()
        return beta

    def getMaxTheta(self):
        maxTheta = egg.maxTheta(self.gam, self.M)
        print(f"Max deflection: {maxTheta} deg")

    #at M=1.05 and gam=1.3, even a 0.5deg turn will lead to a normal shock
    #so it has been selected as the Mach number that forces one
    def doShockwave(self, theta):
        maxTheta = egg.maxTheta(self.gam, self.M)
        shockDict = dict()
        prevPt = self.Pt
        if theta >= maxTheta:
            self.doNormalShock()
            Ptr = self.Pt / prevPt
            return Shockwave("normal", 0.0, 90.0, Ptr)
        elif self.M <= 1.05:
            self.doNormalShock()
            Ptr = self.Pt / prevPt
            return Shockwave("normal", 0.0, 90.0, Ptr)
        else:
            beta = self.doObliqueShock_getBeta(theta)
            Ptr = self.Pt / prevPt
            return Shockwave("oblique", theta, beta, Ptr)

###
# M, Mach
# P, Pa, but displays in bar above 100kPa
# T, K
# rho, kg/m3
# gam
# Pt, Pa, but displays in bar above 100kPa
# Tt, K
# mol dict, mol.get("avg") for the desired value
# Rs
# Cp, J/kg-K
# SoS, m/s
# V, m/s
# mdot, kg/s
# A, m2
###

def initEmptyStation():
    emptyMol = {"avg": -1.0}
    emptyStation = Station("empty", -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, emptyMol, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0)
    return emptyStation

def initConstantQTrajectory(Q, maxAltM, step):
    maxAlt = maxAltM + step
    altMVrange = []
    for x in range(0, maxAlt, step):
        P, T, rho = getISA(x)
        #print(f"{x} metres: {P}Pa, {T}K, {rho}kg/m3")
        SoS = math.sqrt(RsAir * gamiAir * T)
        Vreq = math.sqrt((2 * Q) / rho)
        Mreq = Vreq / SoS
        xTup = (x, Mreq, Vreq)
        altMVrange.append(xTup)
    return altMVrange

def getAltitudeAtMach(altMVrange, M):
    alt, _M, _V = min(altMVrange, key=lambda x: abs(M - x[1]))
    return alt

def getAltitudeAtVel(altMVrange, V):
    alt, _M, _V = min(altMVrange, key=lambda x: abs(V - x[2]))
    return alt
