import formulaegg as egg

def testEverything():
    g300 = egg.gam_T(1.4, 300)
    g1k = egg.gam_T(1.4, 1000)
    print("gam 300:", g300)
    print("gam 1k:", g1k)

    ther = egg.maxTheta(1.4, 2.5)
    print("max theta at M2.5:", ther)
    print()

    npr = egg.normalPr(1.4, 2.5)
    ntr = egg.normalTr(1.4, 2.5)
    nrr = egg.normalRhor(1.4, 2.5)
    nmo = egg.normalMout(1.4, 2.5)
    npt = egg.normalPtr(1.4, 2.5)
    print("Normal Pr, Tr, Rr, Mout, Ptr")
    print(npr)
    print(ntr)
    print(nrr)
    print(nmo)
    print(npt)
    print()

    ot = egg.obliqueTheta(1.4, 2.5, 30)
    print("Theta for 30deg shock:", ot)
    Mout = egg.obliqueMout(1.4, 2.5, 30, ot)
    print("Mout:", Mout)
    opr = egg.obliquePr(1.4, 2.5, 30)
    otr = egg.obliqueTr(1.4, 2.5, 30)
    orr = egg.obliqueRhor(1.4, 2.5, 30)
    opt = egg.obliquePtr(1.4, 2.5, 30)
    print("Oblique Pr, Tr, Rr, Ptr")
    print(opr)
    print(otr)
    print(orr)
    print(opt)

    print()
    beta = egg.obliqueBeta(1.4, 2.5, 10)
    print("final beta:", beta)
    thetaTest = egg.obliqueTheta(1.4, 2.5, beta)
    print("confirming theta is 10deg:", thetaTest)
    pass

testEverything()
