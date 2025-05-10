**ISTRUZIONI D’USO**

“**Una volta avviato il programma è possibile gestire tutto da User interface laterale senza dover usare più la linea di comando, a meno che non si voglia cambiare mappa (in tal caso rilanciare da linea di comando con nome nuova mappa**).“

**“Da User interface : pulsanti dropdown per cambiare algoritmo ed euristica, pulsante per abilitare/disabilitare movimento diagonale, pulsante di chiusura programma.”**

**“Dato che le direzioni delle correnti sono solo ortogonali, le Mappe currents sono da provare solo con diagonali disattivate.”**

**“E’ presente una semplice animazione del pirata che si muove seguendo il percorso trovato, purtroppo per mappe grandi e per algoritmi lunghi e laboriosi l’animazione risulta molto lunga. Se si desidera togliere e vedere immediatamente il risultato finale è possibile commentare (\#) le righe 459-460-461-462-463 del file Pirate\_path\_finding\_gui.”**

**ISTRUZIONI PER WINDOWS**

⟶  Da linea di comando : py Pirate\_path\_finding\_gui.py \-s nome algoritmo \-h nome euristica \-f maps/nome mappa \-d scelta diagonale  
   
nome algoritmo : BFS, DFS, ASTAR,UCS,WEBEX,GREEDY

nome euristica : Manhattan, Euclidean, Mst, Current

nome mappa : map\_singleGoal.json , map\_multiGoal\_1.json , map\_multiGoal\_2.json , map\_multiGoal\_3.json, map\_currents\_1.json , map\_currents\_2.json

scelta diagonale : true, false

esempio : py Pirate\_path\_finding\_gui.py \-s ASTAR \-h Mst \-f maps/map\_singleGoal.json \-d false

   
**ISTRUZIONI PER MAC**

⟶ Da linea di comando: python3 Pirate\_path\_finding\_gui.py \-s nome algoritmo \-h nome euristica \-f maps/nome mappa \-d scelta diagonale

nome algoritmo : BFS, DFS, ASTAR,UCS,WEBEX,GREEDY

nome euristica : Manhattan, Euclidean, Mst, Current

nome mappa : map\_singleGoal.json , map\_multiGoal\_1.json , map\_multiGoal\_2.json, map\_multiGoal\_3.json, map\_currents\_1.json , map\_currents\_2.json

scelta diagonale : true, false

esempio : python3 Pirate\_path\_finding\_gui.py \-s GREEDY \-h Euclidean \-f maps/map\_multiGoal\_2.json \-d true

