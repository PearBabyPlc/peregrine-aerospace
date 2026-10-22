import formulaegg as egg
import solvers as solve

def testEverything():
    ambient = solve.getAmbientStation(25000)
    ambient = solve.stagStationAtVel(ambient, 1500)
    print(ambient)
    print()
    normal = solve.staticStationAtMach(ambient, 0.95)
    print(normal)
    
testEverything()
