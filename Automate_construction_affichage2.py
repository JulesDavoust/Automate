from collections import OrderedDict
import pandas
import re
#J:
def ajout_transition_matrice_auto(nvline, nvline1,col, tab_decomp_transition):
    val_transition = []
    #print(nvline, " ", nvline1[col])
    for l in range(len(tab_decomp_transition)):
            if(tab_decomp_transition[l][0] == nvline and tab_decomp_transition[l][1] == nvline1[col]):
                val_transition.append(tab_decomp_transition[l][2])
                #print("ajout valeur :", val_transition)
    z = 0
    while z < len(tab_decomp_transition):
        if (tab_decomp_transition[0][0] == nvline and tab_decomp_transition[0][1] == nvline1[col]):
            del tab_decomp_transition[0]
        z += 1
    return val_transition
#J:
def matrice_auto(matrice, nbr_symb, nbr_etats, I, T, Q, nvline1, tab_decomp_transition, etats_term_num, etats_init_num):
    tab_affichage_auto = []
    cpt_Q = 0
    cpt_Q2 = 0
    cpt_nv1 = 2
    verif = 0
    I1 = I
    T1 = T
    for line in range(nbr_etats):
        nvline = []
        for col in range(nbr_symb + 2):
            if (col == 0):
                E = 0
                S = 0
                ES = 0
                for i in range(etats_init_num):
                    for j in range(etats_term_num):
                        if(T[j] == I[i] == line):
                            #nvline.append("ES")
                            ES = 1
                            verif = 1
                        elif(I[i] == line):
                            #nvline.append("E")
                            E = 1
                            verif = 1
                        elif(T[j] == line):
                            #nvline.append("S")
                            S = 1
                            verif = 1
                if(S == 1 and E == 1 or ES == 1):
                    nvline.append("ES")
                elif(S == 1 and ES == 1):
                    nvline.append("ES")
                elif(E == 1 and ES == 1):
                    nvline.append("ES")
                elif(E == 1):
                    nvline.append("E")
                elif(S == 1):
                    nvline.append("S")
                if verif == 0:
                    nvline.append("  ")
                verif = 0
                cpt_Q = cpt_Q + 1
            elif (col == 1):
                nvline.append(Q[cpt_Q2])
                cpt_Q2 = cpt_Q2 + 1
            else:
                nvline.append("-")
            if (col != 0 and col != 1):
                transi_nv = nvline[1]
                tab_ajout = ajout_transition_matrice_auto(transi_nv, nvline1,col, tab_decomp_transition)
                if(tab_ajout):
                    cdc = tab_ajout[0]
                    i = 1
                    if(len(tab_ajout) > 1):
                        while(i < len(tab_ajout)):
                            cdc = str(cdc) + "," + str(tab_ajout[i])
                            i = i + 1
                    #print(cdc)
                    nvline[col] = cdc

                #tab_tri2 = []
                #for a in range(2, len(A) + 2):
                #    for rs in range(len(tab_recup_symboles)):
                #        rpt = rs
                #        if (tab_recup_symboles[rs] == nvline1[a] and nvline[1] == tab_recup_prem_transition[rs]):
                #            print(nvline1[a], "et", nvline[1], " :", tab_recup_der_transition[rpt])
                #print("-------------")
                # print("tt2 :",tab_tri2)
        matrice.append(nvline)
#J:
def construction_automate(text):
    file = open(text, "r")
    data = file.read()
    lines = data.splitlines()

    nbr_symb = int(lines[0])
    nbr_etats = int(lines[1])
    etats_init_num = list(map(int, lines[2].split()))
    I = []
    len_etats_init_num = len(etats_init_num)
    etats_term_num = list(map(int, lines[3].split()))
    T = []
    len_etats_term_num = len(etats_term_num)
    nbr_transitions = int(lines[4])
    Q = []
    A = []
    tab_decomp_transition = []
    leng_auto = len(lines)

    cpt = 1
    # print("=================== Longueurs ===================")
    # print("longueur automate :", leng_auto)
    # print("longueur états init num :", len_etats_init_num,"\n")
    # print("=================== Symboles + états ===================")

    code_ascii = 97
    # print(nbr_symb, " symboles dans l'alphabet")
    while (cpt <= nbr_symb):
        A.append(chr(code_ascii))
        code_ascii = code_ascii + 1
        cpt = cpt + 1
    # print("A = ", A)
    # print(nbr_etats, "états")

    cpt = 0
    while (cpt < nbr_etats):
        Q.append(cpt)
        cpt = cpt + 1
    # print("Q = ", Q)

    # print("\n=================== Initiaux ===================")
    cpt = 1
    # print("Nombre états initiaux tableau + numéro:", etats_init_num)
    nombre_etats_init = 0
    for i in [0, 1]:
        if i == 0:
            nombre_etats_init = etats_init_num[i]
        elif i == 1:
            while (cpt <= len_etats_init_num - 1):
                I.append(etats_init_num[cpt])
                cpt = cpt + 1
    # print(nombre_etats_init, "états initiaux")
    # print("I = ", I)

    # print("\n=================== Terminaux ===================")
    cpt = 1
    # print("Nombre états terminaux tableau + numéro:", etats_term_num)
    nombre_etats_term = 0
    for i in [0, 1]:
        if i == 0:
            nombre_etats_term = etats_term_num[i]
        elif i == 1:
            while (cpt <= len_etats_term_num - 1):
                T.append(etats_term_num[cpt])
                cpt = cpt + 1
    # print(nombre_etats_term, "états terminaux")
    # print("T = ", T)
    # if tab_nombre_etats_init == 2:
    #    print("ça marche")

    # <état de départ><symbole><état d’arrivée>
    cpt = 5
    epsilon = 0
    check = 1
    verif = 0
    tab_recup_symboles = []
    tab_recup_prem_transition = []
    tab_recup_der_transition = []

    while (cpt <= leng_auto - 1):
        tab_tri = list(lines[cpt].strip())
        var_recup = tab_tri[0]
        tab_decomp = []
        print(tab_tri)
        check = 1
        while ((ord("a") > ord(tab_tri[check]) or ord(tab_tri[check]) > ord("z")) and ord(tab_tri[check]) != ord("*")):
            var_recup = var_recup + tab_tri[check]
            check = check + 1
        # print("1 :", var_recup)
        # print("c1 :", check)
        tab_recup_prem_transition.append(var_recup)
        tab_decomp.append(var_recup)
        for i in range(len(tab_tri)):
            if (tab_tri[i] == '*'):
                tab_recup_symboles.append('*')
                tab_decomp.append('*')
                A.append('*')
                epsilon = 1 + epsilon
            for j in range(nbr_symb):
                if (tab_tri[i] == A[j]):
                    tab_recup_symboles.append(tab_tri[i])
                    tab_decomp.append(tab_tri[i])
        # print(A)
        if ((ord("a") < ord(tab_tri[check]) or ord(tab_tri[check]) < ord("z")) or ord(tab_tri[check]) == ord("*")):
            check2 = check + 1
            var_recup = tab_tri[check2]
            if (check2 < len(tab_tri)):
                while (check2 + 1 < (len(tab_tri))):
                    var_recup = var_recup + tab_tri[check2 + 1]
                    check2 = check2 + 1
            tab_recup_der_transition.append(var_recup)
            tab_decomp.append(var_recup)
        tab_decomp_transition.append(tab_decomp)
        cpt = cpt + 1
    for i in range(len(tab_decomp_transition)):
        for j in range(3):
            if (j != 1):
                if ("0" in tab_decomp_transition[i][j]):
                    if (tab_decomp_transition[i][j].index('0') == 0 and len(tab_decomp_transition[i][j]) > 1):
                        val_transit = tab_decomp_transition[i][j]
                        val_transit = list(val_transit.strip())
                        val_transit[0], val_transit[1] = val_transit[1], val_transit[0]
                        val_transit = ''.join(val_transit)
                        tab_decomp_transition[i][j] = val_transit
                tab_decomp_transition[i][j] = int(tab_decomp_transition[i][j])

    # print("1er tab decomp :", tab_decomp_transition[0])

    # print("\n=================== Transitions ===================")
    # print(nbr_transitions, " transitions (dont", epsilon, "epsilon)")

    # print("\n=================== <état de départ><symbole><état d’arrivée> ===================")
    tab_recup_prem_transition = [int(i) for i in tab_recup_prem_transition]
    # print(tab_recup_prem_transition)
    # print(tab_recup_symboles)
    tab_recup_der_transition = [int(i) for i in tab_recup_der_transition]
    # print(tab_recup_der_transition)
    A = list(OrderedDict.fromkeys(A))
    matrice = []
    nvline1 = []
    cpt_A = 0
    cpt = 0
    nbr_symb_bis = len(A)
    while (cpt < nbr_symb_bis + 2):
        if (cpt > 1):
            nvline1.append(A[cpt_A])
            cpt_A = cpt_A + 1
        else:
            nvline1.append(" ")
        cpt = cpt + 1
    matrice.append(nvline1)
    matrice_auto(matrice, nbr_symb_bis, nbr_etats, I, T, Q, nvline1, tab_decomp_transition, nombre_etats_term,nombre_etats_init)
    #print(matrice)
    column_labels = matrice[0]
    row_labels = []
    del matrice[0]
    for i in range(len(matrice)):
        row_labels.append(matrice[i][0])
        del matrice[i][0]
    del column_labels[0]
    #print(row_labels)
    #print(column_labels)
    #print(matrice)
    # print(row_labels)
    # print(column_labels)
    # print(matrice)
    file.close()# print("\n\n===================Automate===================\n")
    automate = pandas.DataFrame(matrice, columns=column_labels, index=row_labels)
    return nbr_symb, A, nbr_etats, Q, etats_init_num, nombre_etats_init, I, etats_term_num, ,row_labels, column_labels, matrice, automate

def automate_affichage_main(validation, nbr_symb, A, Q, etats_init_num, nombre_etats_init, I, etats_term_num, nombre_etats_term, T, nbr_transitions, epsilon, automate, nbr_etats, matrice, row_labels):

    deter_ok = 1
    complet_ok = 1
    a = 0
    i = 0
        #for i in range(len(matrice)):
        #    for j in range(len(matrice[0])):

        #while(a < len(row_labels)):
        #    if(row_labels[a] == "ES" or row_labels[a] == "S"):
        #        teta[0][1].append("T")
        #    a = a + 1
        #print(teta)
    if(validation == "PA"):
        print("=================== Symboles + états ===================")
        print(nbr_symb, " symboles dans l'alphabet")
        print("A = ", A)
        print(nbr_etats, "états")
        print("Q = ", Q)
        print("\n=================== Initiaux ===================")
        print("Nombre états initiaux tableau + numéro:", etats_init_num)
        print(nombre_etats_init, "états initiaux")
        print("I = ", I)
        print("\n=================== Terminaux ===================")
        print("Nombre états terminaux tableau + numéro:", etats_term_num)
        print(nombre_etats_term, "états terminaux")
        print("T = ", T)
        print("\n=================== Transitions ===================")
        print(nbr_transitions, " transitions (dont", epsilon, "epsilon)")
    elif(validation == "A"):
        print("\n\n===================Automate===================\n")
        print(automate)
    elif(validation == "APA"):
        print("=================== Symboles + états ===================")
        print(nbr_symb, " symboles dans l'alphabet")
        print("A = ", A)
        print(nbr_etats, "états")
        print("Q = ", Q)
        print("\n=================== Initiaux ===================")
        print("Nombre états initiaux tableau + numéro:", etats_init_num)
        print(nombre_etats_init, "états initiaux")
        print("I = ", I)
        print("\n=================== Terminaux ===================")
        print("Nombre états terminaux tableau + numéro:", etats_term_num)
        print(nombre_etats_term, "états terminaux")
        print("T = ", T)
        print("\n=================== Transitions ===================")
        print(nbr_transitions, " transitions (dont", epsilon, "epsilon)")
        print("\n\n===================Automate===================\n")
        print(automate)
#L:
def est_un_automate_asynchrone(matrice, nbr_espilon):
    if(nbr_espilon > 0):
        return True
    else:
        return False
#T:
def est_un_automate_deterministe(matrice_deter, row_labels_v1, Q1, etat_deter):
    parcourir = 0
    deja_fait = []
    #print(matrice_deter)
    ok = 0
    while(parcourir < len(row_labels_v1)):
        if((row_labels_v1[parcourir] == "ES" or row_labels_v1[parcourir] == "E")):
            ok = 1 + ok
        parcourir = parcourir + 1
    tjr_deter = 0
    if(ok == 1):
        if(row_labels_v1[0] == "ES" or row_labels_v1[0] == "E"):
            deja_fait.append(etat_deter[0])
            deter_fin = 0
            parcourir_md = 0
            parcourir_edet = 0
            i = 0
            w = 0
            j = 0
            virgule = 0
            while ((deter_fin < len(etat_deter) - 1) and (tjr_deter == 0)):
                #print("déjà fait :",deja_fait)
                #print(deter_fin)
                deja_fait_ln = []
                parcourir_md = 0
                tjr_deter_ln = 0
                tab_virgule = []
                while (parcourir_md < deter_fin+1) and (tjr_deter_ln == 0):
                    j = 0
                    #print("parcourir_md", parcourir_md)
                    while (j < len(matrice_deter[0])) and (tjr_deter_ln == 0):
                   #     print("j", j)
                        trouver = 0
                        q_e = 0
                        while((q_e < len(Q1)) and (trouver == 0)):
                            if (str(Q1[q_e]) in str(matrice_deter[parcourir_md][j]) and (trouver == 0)):
                                trouver = 1
                                continuer = 0
                                df = 0
                                trouver_df = 0
                                while(df < len(deja_fait)) and (trouver_df == 0):
                  #                  print("df", df)
                                    if(str(deja_fait[df]) == str(matrice_deter[parcourir_md][j])):
                                        trouver_df = 1
                                    df = df + 1
                                if((str(etat_deter[parcourir_edet + 1]) == str(matrice_deter[parcourir_md][j])) and (trouver_df == 0)):
                                    tjr_deter_ln = 1
                                    deja_fait.append(matrice_deter[parcourir_md][j])
                                    deja_fait_ln.append(matrice_deter[parcourir_md][j])
                                    parcourir_edet = parcourir_edet + 1
                                else:
                                        tjr_deter_ln = 0
                 #           print("q_e", q_e)
                            q_e = q_e + 1
                        j = j + 1
                    parcourir_md = parcourir_md + 1
                #print("deja ln",deja_fait_ln)
                if not deja_fait_ln:
                    tjr_deter = 1
                #print("tjr deter", tjr_deter)
                deter_fin = deter_fin + 1
            if(tjr_deter == 1):
                return False
            else:
                return True
        #print("L'automate est déterministe")
    else:
        return False
#V:
def est_un_automate_complet(matrice, asynch, deter):
    matrice_comp = matrice
    #print(matrice_comp)
    fin = 0
    if(asynch == False and deter == True):
        i = 0
        while i < len(matrice_comp) and fin == 0:
            j = 0
            while j < len(matrice_comp[0]) and fin == 0:
                if(str(matrice_comp[i][j]) == "-"):
                    fin = 1
                    return False
                j = j + 1
            i = i + 1
        return True
    else:
        return False
#L:
def completion(matrice_complete, asynch, deter, comp, row_labels_p, nbr_symb):
    if(comp == False and asynch == False and deter == True):
        i = 0
        poubelle = []
        while i < len(matrice_complete):
            j = 0
            while j < len(matrice_complete[0]):
                if (str(matrice_complete[i][j]) == '-'):
                    matrice_complete[i][j] = 'P'
                j = j + 1
            i = i + 1
        for nbrt in range(2, nbr_symb+2):
            poubelle.append('P')
        row_labels_p.append(' ')
        matrice_complete.append(poubelle)

        return matrice_complete, row_labels_p
#T & L:
def determinisation_et_completion(matrice, row_labels, column_labels, asynch, deter, comp, Q, A, T, I):
        parcourir = 0
        etat_labels_deter = []
        row_labels_deter = []
        matrice_deter = []
        entre_deter = ""
        while (parcourir < len(row_labels)):
            if((row_labels[parcourir] == "ES" or row_labels[parcourir] == "E")):
                entre_deter =  entre_deter + str(matrice[parcourir][0])
            parcourir = parcourir + 1
        entre_deter_tab = list(entre_deter.strip())
        entre_deter_tab.sort()
        #print(entre_deter_tab)
        entre_deter = str(entre_deter)
        entre_deter2 = entre_deter
        entre_deter = ','.join(entre_deter)
        #print(entre_deter)
        etat_labels_deter.append(entre_deter)
        tjr_deter = 0
        deja_fait = []
        deja_fait.append(entre_deter2)
        while(tjr_deter != 1):
            i = 0
            j = 0
            Q_cpt = 0
            #est_vide = 0
            cpt_m = 0
            nvline_tab = []
            for cpt_A in range(len(A)):
                Q_cpt = 0
                nvline_char = ""
                while (Q_cpt < len(Q)):
                    for i in range(len(entre_deter_tab)):
                        if(entre_deter_tab[i] == str(Q[Q_cpt])):
                            if (str(matrice[Q_cpt][cpt_A + 1]) != "-"):
                                nvline_char = nvline_char + str(matrice[Q_cpt][cpt_A + 1])
                                #print(nvline_char)
                    Q_cpt = Q_cpt + 1
                nvline_tab.append(nvline_char)
            #print(nvline_tab)
            virgule_a_suppr = ","
            for cpt_nvt in range(len(nvline_tab)):
                suppr_virgule = nvline_tab[cpt_nvt]
                suppr_virgule = suppr_virgule.replace(virgule_a_suppr, "")
                new_str_tab = list(suppr_virgule.strip())
                new_str_tab.sort()
                #print("new str_tab", new_str_tab)
                new_str2 = ''.join(new_str_tab)
                #print("new str", new_str2)
                #print(suppr_virgule)
                nvline_tab[cpt_nvt] = new_str2
            #print(nvline_tab)
            for cpt_nvt2 in range(len(nvline_tab)):
                for Q_cpt2 in range(len(Q)):
                    if(nvline_tab[cpt_nvt2].count(str(Q[Q_cpt2]))>1):
                        #print(nvline_tab[cpt_nvt2])
                        #print(Q[Q_cpt2])
                        cpt_sup = 0
                        #while cpt_sup < len(nvline_tab[cpt_nvt2]):
                        for cpt_sup2 in range(len(nvline_tab[cpt_nvt2])):
                                if (nvline_tab[cpt_nvt2].count(str(Q[Q_cpt2])) > 1):
                                    if(nvline_tab[cpt_nvt2][cpt_sup2] == str(Q[Q_cpt2])):
                                        new_str = nvline_tab[cpt_nvt2].replace(str(Q[Q_cpt2]),"")
                                        new_str = new_str + str(Q[Q_cpt2])
                                        new_str_tab = list(new_str.strip())
                                        new_str_tab.sort()
                                        #print("new str_tab", new_str_tab)
                                        new_str = ''.join(new_str_tab)
                                        #print("new str", new_str)
                                        nvline_tab[cpt_nvt2] = new_str
                                        #print(nvline_tab[cpt_nvt2])
                            #cpt_sup = cpt_sup + 1
            #print(nvline_tab)
            matrice_deter.append(nvline_tab)
            #print(matrice_deter)
            #print(entre_deter2)

            deter_fin = 0
            parcourir_md = 0
            parcourir_edet = 0
            i = 0
            w = 0
            j = 0
            virgule = 0
            tjr_deter1 = 0
            deja_fait_ln = []
            #print("len matrice", len(matrice_deter))
            while ((deter_fin < len(matrice_deter)) and (tjr_deter1 == 0)):
                # print("déjà fait :",deja_fait)
                #print(deter_fin)
                parcourir_md = 0
                tjr_deter_ln = 0
                tab_virgule = []
                #if(deter_fin)
                while (parcourir_md <= deter_fin) and (tjr_deter_ln == 0):
                    j = 0
                    # print("parcourir_md", parcourir_md)
                    while (j < len(matrice_deter[0])) and (tjr_deter_ln == 0):
                        #     print("j", j)
                        trouver = 0
                        q_e = 0
                        while ((q_e < len(Q)) and (trouver == 0)):
                            #print("QE",q_e,"parcourirmd", parcourir_md,"j",j)
                            if (str(Q[q_e]) in str(matrice_deter[parcourir_md][j]) and (trouver == 0)):
                                trouver = 1
                                continuer = 0
                                df = 0
                                trouver_df = 0
                                while (df < len(deja_fait)) and (trouver_df == 0):
                                    #                  print("df", df)
                                    if (str(deja_fait[df]) == str(matrice_deter[parcourir_md][j])):
                                        trouver_df = 1
                                    df = df + 1
                                if ((str(entre_deter2) != str(matrice_deter[parcourir_md][j])) and (trouver_df == 0)):
                                    tjr_deter_ln = 1
                                    entre_deter2 = matrice_deter[parcourir_md][j]
                                    entre_deter_tab = list(entre_deter2.strip())
                                    entre_deter_tab.sort()
                                    entre_deter2 = ''.join(entre_deter_tab)
                                    deja_fait.append(entre_deter2)
                                    deja_fait_ln.append(entre_deter2)
                                    #print("deja fait",deja_fait)
                                    #print("deja ln",deja_fait_ln)

                                    #print("edt",entre_deter_tab)
                                    #print("ed2",entre_deter2)
                                    parcourir_edet = parcourir_edet + 1
                                    tjr_deter1 = 1
                                else:
                                    tjr_deter_ln = 0
                            #           print("q_e", q_e)
                            q_e = q_e + 1
                        j = j + 1
                    parcourir_md = parcourir_md + 1
                deter_fin = deter_fin + 1
            if not deja_fait_ln:
                #print("ON est rentré...")
                tjr_deter = 1
                # print("tjr deter", tjr_deter)
        for ln in range(len(matrice_deter)):
            for ln_j in range(len(matrice_deter[0])):
                if(matrice_deter[ln][ln_j] == ''):
                    matrice_deter[ln][ln_j]='-'
        #print(matrice_deter)
        entree_sortie = []
        E = 0
        S = 0
        ES = 0
        verif = 0
        for i in range(len(I)):
            for j in range(len(T)):
                if (str(T[j]) in deja_fait[0] and str(I[i]) in deja_fait[0]):
                    # nvline.append("ES")
                    ES = 1
                    verif = 1
                elif (str(I[i]) in deja_fait[0]):
                    # nvline.append("E")
                    E = 1
                    verif = 1
        if (E == 1 and ES == 1):
            entree_sortie.append("ES")
        elif (E == 1):
            entree_sortie.append("E")
        elif(ES == 1):
            entree_sortie.append("ES")
        S = 0
        verif = 0
        for djf in range(1, len(deja_fait)):
            for t_T in range(len(T)):
                    if (str(T[t_T]) in deja_fait[djf]):
                        # nvline.append("S")
                        S = 1
                        verif = 1
            if (S == 1):
                entree_sortie.append("S")
                verif = 0
            elif verif == 0:
                entree_sortie.append("  ")

        #print(deja_fait)
        #print(entree_sortie)
        for ln in range(len(matrice_deter)):
            matrice_deter[ln].insert(0, deja_fait[ln])
        #print(matrice_deter)
        #comp = est_un_automate_complet(matrice_deter, asynch, deter)
        return deja_fait, entree_sortie, matrice_deter
#V:
def lecture_mot():
    a=True
    while (a==True):
        mot= str(input("Saisir le mot mot que vous souhaitez lire (saisir @ à la fin de votre mot):"))
        if (("@" in mot)==True):
            a=False
        else:
            a=True
    return mot
#V:
def reconnaitre_mot(mot, A, text):
    a= 1
    b= True
    file = open(text, "r")
    data = file.read()
    lines = data.splitlines()
    nbrmax_transi_A= int(lines[4])
    nbrmax_caract_mot= int(len(mot))
    nbr_symbols= int(lines[0])
    mot_reco= mot_reconnu(A, text)
    cpt=0
    A=[]        #determination des transitions
    code_ascii = 97        #"
    while (cpt <= nbr_symbols):        #"
        A.append(chr(code_ascii))        #"
        code_ascii = code_ascii + 1        #"
        cpt = cpt + 1        #"
    while (a==1):
        for j in range (len(mot)):
            if ((mot[j] in A)== True):        #vérification que l'ensemble des caractères saisi par l'utilisateur fait parti des transitions
                a= 1
            else:
                a= 0
        if (nbrmax_caract_mot <= nbrmax_transi_A):      #vérification que le mot saisi par l'utilisateur n'est pas plus long que le nombre maximal de transitions possible
            while (b == True):
                for i in range(nbrmax_caract_mot):
                    if (mot[i] == mot_reco[i]) and (mot[i] != '@'):     #vérification que chaque caractère du mot saisi correspond au mot reconnu par l'automate
                        b = True
                        i = i + 1
                    else:
                        b = False
    return b
#V:
def mot_reconnu(A, text):
    file = open(text, "r")
    data = file.read()
    lines = data.splitlines()
    nbr_lignes= len(lines)
    caracteres_non_voulus= '0123456789'
    mot_reco= ''
    for i in range (nbr_lignes):
        for j in range (len(caracteres_non_voulus)):
            lines= lines[i].replace(caracteres_non_voulus[j], '')
        mot_reco= mot_reco + lines
        i= i+1
    return mot_reco

def main():
    print("Choisir automate, taper soit : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44 :\n")
    x = int(input("Automate :"))
    text = str(x)+".txt"
    print(text)
    tout_automate = construction_automate(text)
    nbr_symb = tout_automate[0]
    A = tout_automate[1]
    nbr_etats = tout_automate[2]
    Q = tout_automate[3]
    etats_init_num = tout_automate[4]
    nombre_etats_init = tout_automate[5]
    I = tout_automate[6]
    etats_term_num = tout_automate[7]
    nombre_etats_term = tout_automate[8]
    T = tout_automate[9]
    nbr_transitions = tout_automate[10]
    epsilon = tout_automate[11]
    row_labels = tout_automate[12]
    column_labels = tout_automate[13]
    matrice = tout_automate[14]
    automate = tout_automate[15]
    validation = "Z"
    while(validation != "A" and validation != "PA" and validation != "APA"):
            print("\n- Afficher l'Automate, taper : A\n- Afficher des précisions sur l'Automate, taper : PA\n- Afficher les deux, taper : APA\n")
            validation = input("Que voulez-vous ?\n")
    automate_affichage_main(validation, nbr_symb, A, Q, etats_init_num, nombre_etats_init, I, etats_term_num, nombre_etats_term, T, nbr_transitions, epsilon, automate, nbr_etats, matrice, row_labels)
    matrice_v1 = tout_automate[14]
    row_labels_v1 = row_labels
    Q1 = Q
    asynch = est_un_automate_asynchrone(matrice_v1, epsilon)
    etat_deter = []
    for i in range(len(matrice_v1)):
        etat_deter.append(matrice_v1[i][0])
    for i in range(len(matrice_v1)):
        del matrice_v1[i][0]
    deter = est_un_automate_deterministe(matrice_v1, row_labels_v1, Q1, etat_deter)

    q_cpt = 0
    for m_cpt in range(len(matrice)):
            matrice[m_cpt].insert(0, Q[q_cpt])
            q_cpt = q_cpt + 1
    quitt = "N"
    while(quitt == "N"):
        print("Voulez vous savoir si votre automate est : asynchrone ou deterministe ou complet ?\n")
        val = input("Asynchrone (ASYNCH?), Deterministe (DETER?), Complet (COMP?) :\n")
        if (val == "ASYNCH?"):
            if asynch == True:
                print("L'automate est asynchrone car il contient", epsilon, " transitions avec des epsilons")
            else:
                print("L'automate est synchrone car il ne contient pas d'epsilons")
        elif (val == "DETER?"):
            #print(deter)
            if deter == True:
                print("L'automate est déterministe")
            else:
                print("L'automate n'est pas déterministe")
                if(asynch == True):
                    print("Voulez vous déterminiser votre automate asynchrone ? (ne marche pas)")
                else:
                    print("Voulez vous déterminiser votre automate synchrone et/ou le compléter (attention problème sur les sorties) ?")
                    oui = "N"
                    oui = input("Oui (O) Non(N) :")
                    if(oui == "O"):
                        asynch = False
                        comp = False
                        tout_deter = determinisation_et_completion(matrice, row_labels, column_labels, asynch, deter, comp, Q,A, T, I)
                        deter_deja_fait = tout_deter[0]
                        deter_entree_sortie = tout_deter[1]
                        matrice_deter = tout_deter[2]
                        # print(column_labels)
                        automate_deter = pandas.DataFrame(matrice_deter, columns=column_labels, index=deter_entree_sortie)
                        print(automate_deter)
                        matrice = matrice_deter
                        row_labels = deter_entree_sortie
                        deter = True
                        asynch = False

        elif(val == "COMP?"):
            comp = est_un_automate_complet(matrice, asynch, deter)
            if comp == True:
                print("Votre automate est complet")
            else:
                if(deter == False and asynch == True):
                    print("Votre automate ne peut pas être complété car il n'est ni synchrone, ni déterministe")
                elif(asynch == True):
                    print("Votre automate ne peut pas être complété car il n'est pas synchrone")
                elif(deter == False):
                    print("Votre automate ne peut pas être complété car il n'est pas déterministe")
                else:
                    print("Votre automate n'est pas complet")
                    for i in range(len(matrice)):
                        del matrice[i][0]
                    # print(matrice)
                    print("Votre automate peut être complété")
                    print("Voulez-vous le compléter ?\n")
                    val_comp = input("Oui (O) ou Non (N) ?\n")
                    if (val_comp == "O"):
                        asynch = False
                        deter = True
                        matrice_v1 = matrice
                        # print(matrice_complete)
                        row_labels_p = row_labels
                        # print(row_labels_p)
                        tout_complete = completion(matrice_v1, asynch, deter, comp, row_labels_p, nbr_symb)
                        matrice_cp = tout_complete[0]
                        matrice_cp[len(matrice_cp)-1].insert(0, " ")
                        for i in range(len(Q)):
                            matrice_cp[i].insert(0, Q[i])
                        # print(tout_complete[0], tout_complete[1])
                        automate_complete = pandas.DataFrame(tout_complete[0], columns=column_labels,index=tout_complete[1])
                        print(automate_complete)
        quitt = input("Voulez vous quitter ? Oui (O) Non (N)")
        print("Voulez vous lire un mot ? :")
        oui = input("Oui (O) Non(N)")
        if(oui == "O"):
            mot = lecture_mot()
            if (mot == '@'):
                mot_vide = mot
                print("Vous avez saisi le mot vide.")
            else:
                print("Vous avez saisi: ", mot)

quitter = "N"
while(ord(quitter) == ord("N")):
    main()
    quitter = input("\n\nVoulez-vous quitter (O pour Oui, N pour Non) ?\n")
