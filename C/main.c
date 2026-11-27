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

// import all the subsections of the program in order
#include "structures.h"
#include "gasdynamics.h"
#include "shockrelations.h"
#include "combustion.h"

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

	Shock cock;
	cock.beta = 60.0;
	obliqueTheta(&sta, &cock);
	printf("\n\nbeta = %.3f\ntheta = %.6f\n\n\n", cock.beta, cock.theta);

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
