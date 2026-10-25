import formulaegg as egg
import airflow as air
import jetEngines as jet

def obliqueShockInletDemo(dynamicP, flightVel, inletArea, inletAngle):
    altMVrange = air.initConstantQTrajectory(dynamicP, 50000, 100)
    altitude = air.getAltitudeAtVel(altMVrange, flightVel)
    sta = air.initEmptyStation()
    sta.getAmbientConds(altitude)
    sta.setVelocity(flightVel)
    sta.setArea(inletArea)
    sta.summary()
    print()
    PtLoss = 1.0
    while sta.M > 1.0:
        sta.getMaxTheta()
        shock = sta.doShockwave(inletAngle)
        print(shock)
        sta.summary()
        print()
        PtLoss *= shock.Ptr
        if shock.type == "normal":
            break
    print()
    byp = sta.bypassAirflow(1.0)
    print(sta)
    print()
    print(byp)
    return PtLoss

#stagPloss = obliqueShockInletDemo(30000, 1050, 10.0, 16.0)

def testFlowMixing():
    s1 = air.initEmptyStation()
    s1.note = "One"
    s2 = air.initEmptyStation()
    s2.note = "Two"
    s1.mdot = 787.67417
    s1.V = 179.47973
    s1.A = 2.4308249
    s1.M = 0.38245119
    s1.gam = 1.3809929
    s1.Cp = 1040.8127
    s1.P = 2.8791537 * 100000
    s1.T = 555.65525
    s1.rho = 1.805417
    s1.Pt = 3.1816272 * 100000
    s1.Tt = 571.18739
    s2.mdot = 660.5058
    s2.V = 310.11246
    s2.A = 6.0010342
    s2.M = 0.62873729
    s2.gam = 1.3737135
    s2.Cp = 1055.4932
    s2.P = 0.62854323 * 100000
    s2.T = 617.05226
    s2.rho = 0.35492069
    s2.Pt = 0.80352258 * 100000
    s2.Tt = 657.59354
    s1.Rs = 287
    s2.Rs = 287
    s1.mol.update({"avg": 28.9703832753})
    s2.mol.update({"avg": 28.9703832753})
    print(s1)
    print()
    print(s2)
    print()
    s1.mixAirflows(s2)
    print(s1)

testFlowMixing()
