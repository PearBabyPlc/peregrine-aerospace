import formulaegg as egg
import airflow as air
import jetEngines as jet
import turbomachinery as turbo

sta = air.initEmptyStation()
sta.getAmbientConds(10000)
sta.setVelocity(290)
sta.setArea(5.0)
sta.getHeatCapacity()
sta.note = "Ambient"
print(sta)
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
sta.note = "Converging outlet"
print(sta)
print()
fan = sta.doExpansionFan(10.0)
fan = sta.doExpansionFan(10.0)
fan = sta.doExpansionFan(10.0)
sta.note = "expansion fan 10,10,10"
print(sta)
