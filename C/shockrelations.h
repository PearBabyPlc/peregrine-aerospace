// shock relations header with a few solvers
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

void obliqueTheta(Station *sta, Shock *sho) {
	double tanBeta = tan(sho->beta * DEG_RAD);
	double sinBeta = sin(sho->beta * DEG_RAD);
	sho->theta = atan(1.0 / (tanBeta * ((((sta->gam + 1.0) * (sta->M * sta->M)) / (2.0 * ((sta->M * sta->M) * (sinBeta * sinBeta) - 1.0))) - 1.0))) * RAD_DEG;
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
