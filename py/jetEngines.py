import formulaegg as egg
import airflow as air

gamiAir = 1.4

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

#basic compressor
def Compressor_PR(sta, eff, CPR):
    CW = (sta.Cp / eff) * (CPR**((sta.gam - 1) / sta.gam) - 1)
    Power = CW * sta.mdot
    sta.Pt *= CPR
    sta.Tt *= CPR**((sta.gam - 1) / sta.gam)
    sta.gam = egg.gam_T(gamiAir, sta.Tt)
    sta.T = sta.Tt * egg.T_Tt(sta.gam, sta.M)
    sta.P = sta.Pt * egg.P_Pt(sta.gam, sta.M)
    sta.rho = egg.rhoIdeal(sta.P, sta.Rs, sta.T)
    #M remains constant
    sta.getSoS()
    sta.V = sta.M * sta.SoS
    sta.updateArea()
    sta.getHeatCapacity()
    return sta, Power

class Compressor:
    def __init__(self, note, eff, PR):
        self.note = str(note)
        self.eff = float(eff)
        self.PR = float(PR)
        self.Power = 0.0

    def __str__(self):
        efp = self.eff * 100
        pkw = self.Power / 1000
        return f"{self.note}\nEfficiency: {efp} percent\nPressure ratio: {self.PR}\nPower: {pkw} kW"

    def runCompressor(self, sta):
        staOut, Powah = Compressor_PR(sta, self.eff, self.PR)
        self.Power = Powah
        return staOut

def initCompressor(eff, PR):
    return Compressor("empty", eff, PR)

#basic turbine
def Turbine_Power(sta, eff, Power):
    TW = Power / sta.mdot
    TPR = 1 / (((TW / (sta.Cp / eff)))**(1 / ((sta.gam - 1) / sta.gam)) + 1)
    sta.Pt *= TPR
    sta.Tt *= TPR**((sta.gam - 1) / sta.gam)
    sta.gam = egg.gam_T(gamiAir, sta.T)
    sta.T = sta.Tt * egg.T_Tt(sta.gam, sta.M)
    sta.P = sta.Pt * egg.P_Pt(sta.gam, sta.M)
    sta.rho = egg.rhoIdeal(sta.P, sta.Rs, sta.T)
    sta.getSoS()
    sta.V = sta.M * sta.SoS
    sta.updateArea()
    sta.getHeatCapacity()
    #Work = (sta.Cp / eff) * ((1 / TPR)**((sta.gam - 1) / sta.gam) - 1)
    #print("TW =", TW, "| TPR =", TPR, "| Work =", Work)
    return sta, TPR

class Turbine:
    def __init__(self, note, eff, Power):
        self.note = str(note)
        self.eff = float(eff)
        self.Power = float(Power)
        self.PR = 1.0

    def __str__(self):
        efp = self.eff * 100
        pkw = self.Power / 1000
        return f"{self.note}\nEfficiency: {efp} percent\nPressure ratio: {self.PR}\nPower: {pkw} kW"

    def runTurbine(self, sta):
        staOut, TPR = Turbine_Power(sta, self.eff, self.Power)
        self.PR = 1.0 / TPR
        return staOut

def initTurbine(eff, Power):
    return Turbine("empty", eff, Power)

#instead of just going with Mach numbers, we'll step by small increments
#since diffusers and convergers are used to ensure the correct dimensions
#they aren't really used to target specific Mach numbers
Mstep = 0.001
def Diffuser_A(sta, Aout):
    while (sta.M > 0.0):
        newMach = sta.M - Mstep
        sta.updateMach(newMach)
        sta.updateArea()
        if (sta.A >= Aout):
            break
    return sta

def Converger_M(sta, Mout):
    while (sta.M < Mout):
        newMach = sta.M + Mstep
        sta.updateMach(newMach)
        sta.updateArea()
        if (sta.M >= Mout):
            break
    return sta

#reflected shock intake spike
class InletRamp:
    def __init__(self, theta):
        self.theta = float(theta)
        self.note = "empty"
        self.OPR = 1.0
        self.Ptr = 1.0
        self.shocks = []

    def __str__(self):
        nshocks = len(self.shocks)
        return f"Inlet ramp\nAngle: {self.theta} deg\nOverall pressure ratio: {self.OPR}\nStagnation pressure ratio: {self.Ptr}\n{nshocks} shocks"

    def runInletRamp(self, sta):
        Pin = sta.P
        Ptin = sta.Pt
        it = 0
        while (sta.M >= 1.0):
            shock = sta.doShockwave(self.theta)
            it += 1
            shock.id = it
            self.shocks.append(shock)
            if (shock.type == "normal"):
                break
        self.OPR = sta.P / Pin
        self.Ptr = sta.Pt / Ptin
        return sta

#an attempt at some Prandtl Meyer stuff later? for now just fuckin Mstep
def Ejector_A(sta, Aout):
    while (sta.M >= 1.0):
        newMach = sta.M + Mstep
        sta.updateMach(newMach)
        sta.updateArea()
        if (sta.A >= Aout):
            break
    return sta

#will update composition
def Combustor_Tmax():
    pass

#figure out best structure for classes
