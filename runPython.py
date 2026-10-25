import formulaegg as egg
import solvers as solve

def obliqueShockInletDemo(dynamicP, flightVel, inletArea, inletAngle):
    altMVrange = solve.initConstantQTrajectory(dynamicP, 50000, 100)
    altitude = solve.getAltitudeAtVel(altMVrange, flightVel)
    sta = solve.initEmptyStation()
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
    return PtLoss

stagPloss = obliqueShockInletDemo(30000, 1050, 10.0, 16.0)
print()
print(f"Stagnation pressure ratio: {stagPloss}")
