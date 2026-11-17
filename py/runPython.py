import formulaegg as egg
import airflow as air
import jetEngines as jet
import turbomachinery as turbo

sta = air.initEmptyStation()
sta.getAmbientConds(32000)
sta.setVelocity(1000)
sta.setArea(20.0)
sta.getHeatCapacity()
sta.note = "Ambient"
print(sta)
print()
intake = jet.InletRamp(10.0)
sta = intake.runInletRamp(sta)
sta.note = "Inlet throat"
print(sta)
print()
intake.note = "le inlet"
print(intake)
print()
for x in intake.shocks:
    print(x)
    print()
print()
sta = jet.Diffuser_A(sta, 15.0)
sta.note = "Diffuser"
print(sta)
print()
comp = jet.initCompressor(0.7, 25)
sta = comp.runCompressor(sta)
Power = comp.Power
comp.note = "Compressor"
print(comp)
sta.note = "Compressor outlet"
print(sta)
print()
sta.note = "Turbine inlet"
sta.T = 1800
sta.getHeatCapacity()
sta.P *= 0.9
sta.setMach(0.6)
sta.rho = sta.P / (sta.Rs * sta.T)
sta.updateArea()
print(sta)
print()
turb = jet.initTurbine(0.8, comp.Power)
sta = turb.runTurbine(sta)
turb.note = "Turbine"
print(turb)
sta.note = "Turbine outlet"
print(sta)
print()
PowerKW = Power / 1000
print("POWAH:", PowerKW)
print()
sta = jet.Converger_M(sta, 1.0)
sta.note = "convergent ejector"
print(sta)
print()
sta = jet.Ejector_A(sta, 20.0)
sta.note = "ejector exit"
print(sta)
