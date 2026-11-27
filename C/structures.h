// definitions of structs and some various useful functions to print them and whatever
typedef struct {
	double M;
	double P;
	double T;
	double rho;
	double gam;
	double Pt;
	double Tt;
	double propN2;
	double propO2;
	double propH2O;
	double mol;
	double Rs;
	double Cp;
	double SoS;
	double V;
	double mdot;
	double A;
} Station;

typedef struct {
	double theta;
	double beta;
} Shock;

void resetStation(Station *sta) {
	sta->M = 0.0;
	sta->P = 0.0;
	sta->T = 0.0;
	sta->rho = 0.0;
	sta->gam = 0.0;
	sta->Pt = 0.0;
	sta->Tt = 0.0;
	sta->propN2 = 0.0;
	sta->propO2 = 0.0;
	sta->propH2O = 0.0;
	sta->mol = 0.0;
	sta->Rs = 0.0;
	sta->Cp = 0.0;
	sta->SoS = 0.0;
	sta->V = 0.0;
	sta->mdot = 0.0;
	sta->A = 0.0;
}

void printStation(Station *sta) {
	printf("Mach %.3f\nP: %.1f Pa\nT: %.1f K\nrho: %.6f kg/m3\ngam: %.3f\nPt: %.1f Pa\nTt: %.1f K\n%.6f N2, %.6f O2, %.6f H2O\nmol: %.3f\nRs: %.1f\nCp: %.1f J/kg-K\nSoS: %.1f m/s\nV: %.1f m/s\nmdot: %.3f kg/s\nA: %.3f m2", sta->M, sta->P, sta->T, sta->rho, sta->gam, sta->Pt, sta->Tt, sta->propN2, sta->propO2, sta->propH2O, sta->mol, sta->Rs, sta->Cp, sta->SoS, sta->V, sta->mdot, sta->A);
}



