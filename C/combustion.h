// some basic Rayleigh heating and updating of composition

double Tt_Ttstar(Station *sta) {
	return ((2.0 * (sta->gam +1.0) * (sta->M * sta->M)) / ((1.0 + sta->gam * (sta->M * sta->M)) * (1.0 + sta->gam * (sta->M * sta->M)))) * (1.0 + ((sta->gam - 1.0) * 0.5) * (sta->M * sta->M));
}

double Pt_Ptstar(Station *sta) {
	double PtsB = (2.0 / (sta->gam + 1.0)) * (1.0 + ((sta->gam - 1.0) * 0.5) * (sta->M * sta->M));
	double PtsC = sta->gam / (sta->gam - 1.0);
	return ((sta->gam + 1.0) / (1.0 + sta->gam * (sta->M * sta->M))) * pow(PtsB, PtsC);
}
