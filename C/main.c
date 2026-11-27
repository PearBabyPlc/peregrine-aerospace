#include <stdio.h>
#include <math.h>
#include <time.h>

// definitions of constants
#define MOL_N2 28.014
#define MOL_O2 31.998
#define MOL_H2 2.016
#define MOL_H2O 36.03
#define R_UNIV 8314.46
#define GAMI_AIR 1.4
#define SQRT_THREE 1.73205080757

static const double THETA = 3055.0 + (5.0 / 9.0);
static const double RAD_DEG = 180.0 / M_PI;
static const double DEG_RAD = M_PI / 180.0;

// definitions of structs
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

// isentropic relations
double Tt_T(Station *sta) {
	return 1.0 + ((sta->gam - 1.0) * 0.5) * (sta->M * sta->M);
}

double Pt_P(Station *sta) {
	double PtA = 1.0 + ((sta->gam - 1.0) * 0.5) * (sta->M * sta->M);
	double PtB = sta->gam / (sta->gam - 1.0);
	return pow(PtA, PtB);
}

double T_Tt(Station *sta) {
	return 1.0 / (1.0 + ((sta->gam - 1.0) * 0.5) + (sta->M * sta->M));
}

double q_rhoV(Station *sta) {
	return 0.5 * sta->rho * sta->V * sta->V;
}

void getSoS(Station *sta) {
	sta->SoS = sqrt(sta->gam * sta->Rs * sta->T);
}

void getMach(Station *sta) {
	sta->M = sta->V / sta->SoS;
}

void getVel(Station *sta) {
	sta->V = sta->M * sta->SoS;
}


// heat capacity
void getRs(Station *sta) {
	sta->Rs = R_UNIV / sta->mol;
}

void getCp(Station *sta) {
	sta->Cp = (sta->Rs / (sta->gam - 1.0)) + sta->Rs;
}

void gam_T(Station *sta) {
	double TT = THETA / sta->T;
	double eTT = exp(TT);
	sta->gam = 1.0 + ((GAMI_AIR - 1.0) / (1.0 + (GAMI_AIR) * (TT * TT * (eTT / ((eTT - 1.0) * (eTT - 1.0))))));
}

// ideal gas law
void rhoIdeal(Station *sta) {
	sta->rho = sta->P / (sta->Rs * sta->T);
}

void Pideal(Station *sta) {
	sta->P = sta->rho * sta->Rs * sta->T;
}

void Tideal(Station *sta) {
	sta->T = sta->P / (sta->rho * sta->Rs);
}

// normal shock relations
double normalPr(Station *sta) {
	return (2.0 * sta->gam * (sta->M * sta->M) - (sta->gam - 1.0)) / (sta->gam + 1.0);
}

double normalTr(Station *sta) {
	return ((2.0 * sta->gam * (sta->M * sta->M) - (sta->gam - 1.0)) * ((sta->gam - 1.0) * (sta->M * sta->M) + 2.0)) / (((sta->gam + 1.0) * (sta->gam + 1.0)) * (sta->M * sta->M));
}

double normalRhor(Station *sta) {
	return ((sta->gam + 1.0) * (sta->M * sta->M)) / ((sta->gam - 1.0) * (sta->M * sta->M) + 2.0);
}

double normalMout(Station *sta) {
	return sqrt(((sta->gam - 1.0) * (sta->M * sta->M) + 2.0) / (2.0 * sta->gam * (sta->M * sta->M) - (sta->gam - 1.0)));
}

double normalPtr(Station *sta) {
	double nPtA = ((sta->gam + 1.0) * (sta->M * sta->M)) / ((sta->gam - 1.0) * (sta->M * sta->M) + 2.0);
	double nPtB = sta->gam / (sta->gam - 1.0);
	double nPtC = 1.0 / ((2.0 * sta->gam * (sta->M * sta->M) - (sta->gam - 1.0)) / (sta->gam + 1.0));
	double nPtD = 1.0 / (sta->gam - 1.0);
	return pow(nPtA, nPtB) * pow(nPtC, nPtD);
}

// oblique shock relations
double maxTheta(Station *sta) {
	double mTA = (sta->M * sta->M) - 1.0;
	return ((4.0 / (3.0 * SQRT_THREE * (sta->gam + 1.0))) * (pow(mTA, 1.5) / (sta->M * sta->M))) * RAD_DEG;
}

// obliqueTheta
// obliqueMout
// obliquePr
// obliqueTr
// obliqueRhor
// obliquePtr
// obliqueBeta
//
// don't bother with Prandtl meyer for now
//
// Tt_Ttstar
// Pt_Ptstar


//////

void testFormulaegg() {
	Station sta;
	resetStation(&sta);
	sta.M = 2.5;
	sta.P = 50000.0;
	sta.T = 400.0;
	sta.rho = 0.65;
	sta.gam = 1.4;
	sta.Rs = 287.0;

	gam_T(&sta);
	getSoS(&sta);
	getVel(&sta);
	getCp(&sta);
	sta.Pt = sta.P * Pt_P(&sta);
	sta.Tt = sta.T * Tt_T(&sta);
	printStation(&sta);

	double maix = maxTheta(&sta);
	printf("\nmax theta: %.3f deg\n", maix);

	printf("\n\nnormal\n\n");
	sta.P *= normalPr(&sta);
	sta.T *= normalTr(&sta);
	sta.rho *= normalRhor(&sta);
	sta.Pt *= normalPtr(&sta);
	sta.M = normalMout(&sta);
	gam_T(&sta);
	getVel(&sta);
	getCp(&sta);
	sta.Tt = sta.T * Tt_T(&sta);
	printStation(&sta);
}

int main() {
	clock_t start = clock();

	testFormulaegg();
	
	double elapsed = ((double)(clock() - start) * 1000.0) / CLOCKS_PER_SEC;
	printf("\n\nProgram finished in %f ms", elapsed);
	return 0;
}
