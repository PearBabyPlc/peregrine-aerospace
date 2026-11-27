// gas dynamics header
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
