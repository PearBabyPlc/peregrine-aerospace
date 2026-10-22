import math
import numpy as np
import formulaegg as egg

class Station:
    def __init__(self, station, M, P, T, rho, gam, Pt, Tt, mol, Rs, Cp, SoS, V):
        self.station = station
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
        return f"Station {self.station}\nM: {self.M}\nP: {strP}\nT: {self.T} K\nrho: {self.rho} kg/m3\ngam: {self.gam}\nPt: {strPt}\nTt: {self.Tt}\nmol: {strMol} g\nRs: {self.Rs}\nCp: {self.Cp} J/kg-K\nSoS: {self.SoS}\nV: {self.V} m/s"

def initEmptyStation():
    emptyMol = {"avg": -1.0,
                "empty": -1.0}
    emptyStation = Station("empty", -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, emptyMol, -1.0, -1.0, -1.0, -1.0)
    return emptyStation

rEarth = 6356766.0
g = 9.80665
molAir = 28.9644
Runiv = 8314.46
RsAir = Runiv / molAir
# this is just simple ideal gas stuff, since the model needs to be run a Lot
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

gamiAir = 1.4
#simple ideal gas stuff
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

def getAmbientStation(alt):
    amb = initEmptyStation()
    P, T, rho = getISA(alt)
    amb.station = "Ambient"
    amb.P = P
    amb.T = T
    amb.rho = rho
    amb.gam = egg.gam_T(gamiAir, T)
    amb.mol.update({"avg": molAir})
    amb.Rs = RsAir
    amb.Cp = egg.getCp(amb.gam, RsAir)
    amb.SoS = egg.getSoS(amb.gam, RsAir, T)
    return amb

def stagStationAtMach(sta, M):
    sta.M = M
    sta.Pt = sta.P * egg.Pt_P(sta.gam, M)
    sta.Tt = sta.T * egg.Tt_T(sta.gam, M)
    sta.V = sta.SoS * M
    return sta

def stagStationAtVel(sta, V):
    sta.V = V
    sta.M = V / sta.SoS
    sta.Pt = sta.P * egg.Pt_P(sta.gam, sta.M)
    sta.Tt = sta.T * egg.Tt_T(sta.gam, sta.M)
    return sta

#gamma is left alone until after isentropic stuff
def staticStationAtMach(sta, M):
    sta.M = M
    sta.P = sta.Pt * egg.P_Pt(sta.gam, M)
    sta.T = sta.Tt * egg.T_Tt(sta.gam, M)
    sta.rho = egg.rhoIdeal(sta.P, sta.Rs, sta.T)
    sta.gam = egg.gam_T(gamiAir, sta.T)
    sta.Cp = egg.getCp(sta.gam, sta.Rs)
    sta.SoS = egg.getSoS(sta.gam, sta.Rs, sta.T)
    sta.V = sta.SoS * M
    return sta
