def grille_exemple():
  for i in range(9):  # 9 lignes
    ligne = ""
    for j in range(9):  # 9 colonnes
      num = i * 9 + j
      ligne += f"{num:2} "
      if j % 3 == 2 and j < 8:
        ligne += "| "
    print(ligne)
    if i % 3 == 2 and i < 8:
      print("_" * 30)

def remplir_grille():
  global data
  data=[]
  while True:
    print("Veuillez entrer un chiffre entre 1 et 9 pour chaque case, ou appuyez sur Entrée pour laisser vide.")
    for i in range(81):
      while True:
        case = input(f"Case {i} ? ")
        if case == "":
          data.append(proba[:])  # Copie indépendante
          break
        try:
          case = int(case)
          if 1 <= case <= 9:
            data.append(case)
            break
          else:
            print("Veuillez saisir un chiffre entre 1 et 9.")
        except ValueError:
          print("Entrée invalide.")
    afficher_grille()
    answer=input("Cette grille vous convient-elle ? (Y:Oui/N:Non)")
    if answer=="Y" and control(data):
      break
    else:
      data=[]
      continue

def afficher_grille():
  for i in range(9):
    ligne = ""
    for j in range(9):
      cell = data[i * 9 + j]
      if isinstance(cell, int):
        num = cell
      elif isinstance(cell, list) and len(cell) == 1:
        num = cell[0]
      else:
        num = "."  # Affichage pour cases vides
      ligne += f"{num:2} "
      if j % 3 == 2 and j < 8:
        ligne += "| "
    print(ligne)
    if i % 3 == 2 and i < 8:
      print("_" * 30)

def control_colonne(data):
  check=True
  for col in range(9):
    chiffres=[data[i] for i in range(col,81,9) if isinstance(data[i],int)]
    for chiffre in chiffres:
      if chiffres.count(chiffre)>1:
        check=False
  return check
      
def control_ligne(data):
  check=True
  for ligne in range(0,81,9):
    chiffres=[data[i] for i in range(ligne, ligne+9) if isinstance(data[i],int)]
    for chiffre in chiffres:
      if chiffres.count(chiffre)>1:
        check=False
  return check

def control_region(data):
  check=True
  regionID=[0,3,6,27,30,33,54,57,60]
  for region in regionID:
    indices=[region,region+1,region+2,region+9,region+10,region+11,region+18,region+19,region+20]
    chiffres=[data[i] for i in indices if isinstance(data[i],int)]
    for chiffre in chiffres:
      if chiffres.count(chiffre)>1:
        check=False
  return check

def control(data):
  print("Vérification de la grille...")
  if control_colonne(data) and control_ligne(data) and control_region(data):
    print("Données correctes !")
    return True
  else:
    print("Données incorrectes. Veuillez saisir une autre grille.")
    return False

def verif_colonne():
  global data
  for col in range(9):
    destroy = [data[i] for i in range(col, 81, 9) if isinstance(data[i], int)]
    for chiffre in destroy:
      for i in range(col, 81, 9):
        if isinstance(data[i], list) and chiffre in data[i]:
          data[i].remove(chiffre)
          if len(data[i]) == 1:
            data[i] = data[i][0]

def verif_ligne():
  global data
  for ligne in range(0, 81, 9):
    destroy = [data[i] for i in range(ligne, ligne + 9) if isinstance(data[i], int)]
    for chiffre in destroy:
      for i in range(ligne, ligne + 9):
        if isinstance(data[i], list) and chiffre in data[i]:
          data[i].remove(chiffre)
          if len(data[i]) == 1:
            data[i] = data[i][0]

def verif_region():
  global data
  regionID = [0,3,6,27,30,33,54,57,60]
  for region in regionID:
    indices = [region, region+1, region+2, region+9, region+10, region+11, region+18, region+19, region+20]
    destroy = [data[i] for i in indices if isinstance(data[i], int)]
    for chiffre in destroy:
      for i in indices:
        if isinstance(data[i], list) and chiffre in data[i]:
          data[i].remove(chiffre)
          if len(data[i]) == 1:
            data[i] = data[i][0]

def verif_grille():
  return all(isinstance(i, int) for i in data)

def propagation_solver():
  print("Résolution en cours...")
  verif_colonne()
  verif_ligne()
  verif_region()

def solver():
  change=True
  while not verif_grille() and change:
    change=False
    old_data=data[:]
    propagation_solver()
    if data!=old_data:
      change=True
  if verif_grille():
    print("Résolution complète !")
    afficher_grille()
  if not change:
    print("La propagation seule ne suffit pas. Il faut passer à une autre méthode.")
    brute_force()

def brute_force():
  case_number=[]
  probes=[]
  for i in range(len(data)):
    if isinstance(data[i],list):
      case_number.append(i)
      probes.append(data[i][:])
  read=0
  subread=0
  while not (verif_grille() and control(data)):
    while read >= 0 and subread >= len(probes[read]):
      print(f"Retour arrière sur la case {case_number[read]}")
      data[case_number[read]]=probes[read]
      read-=1
      if read < 0:
        print("Aucune solution trouvée.")
        return
      subread=probes[read].index(data[case_number[read]])+1 if isinstance(data[case_number[read]], int) else 0
    if read < 0:
      break
    print(f"Test de la case {case_number[read]} avec {probes[read][subread]}...")
    data[case_number[read]]=probes[read][subread]
    if control(data):
      read+=1
      subread=0
    else:
      subread+=1
  print("C'était pas gagné mais c'est bon !")
  afficher_grille()
  
print("SolverDOKU - Résolveur de Sudoku")
grille_exemple()
proba = list(range(1, 10))
data = []
remplir_grille()
solver()
exit=input("Press ENTER to exit")
