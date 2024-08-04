Az önkormányzatban van egy képviselőtestület [test] (az összes képviselő részt vesz benne),  
és több bizottság [biz] (csak azok vesznek részt akik tagjai a bizottságnak).  

A testületnek és a bizottságnak is vannak üléseik [folder].   
Ezek lehetnek előre meghirdetett időpontok (rendes), vagy sürgős ülések (rendkívüli).   
Van időpontjuk, helyszínük.  
Az testületi / bizottsági ülés előtt X nappal ki kell küldeni a meghívót [inv].   
Ebben szerepelnek a napirendi pontok, a döntési javaslatok (amikről megy majd a szavazás),   
és az előterjesztések kapcsolódó dokumentumai (háttéranyagok).  

Az ülés napján ezt földolgozzák, megszavazzák, és készül a jegyzőkönyv.  
A sikeresen megszavazott előterjesztésekből pedig határozatok lesznek.  

- Képviselőtestületi / bizottsági ülés
    - meghívó
    - jegyzőkönyv
    - napirendi pont
        - döntési javaslat / előterjesztés
            - melléklet
            - szavazás
                - határozat

## Mappák

A mappák a MikroDat által használt logikát tükrözik:


- **Meghívók**  
    - Testület  
        - Napirendek  
            - Előterjesztés  
            - Döntési javaslat  
            - Melléklet  
- **Határozatok**  
    - Bizottságok
        - Napirendek
            - Határozat
- **Jegyzőkönyvek**  
    - Bizottságok
        - Napirendek
            - Jegyzőkönyv

---
### Mappa API Endpointok

#### ` Minden mappát évek azonosítanak`

* /inv/years  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/inv/years  
* /hat/years
https://mikrodat.ujbuda.hu/app/cms/api/honlap/hat/years  
* /jegy/years
https://mikrodat.ujbuda.hu/app/cms/api/honlap/jegy/years  

Ezek egy önkormányzaton belül rendre ugyanazt az évlistát adják vissza.

#### Meghívók (inv)
> /**inv**/folders?year=[year]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/inv/folders?year=2024  
- datum
- kategoria
- idopont
- hely
- uuid **<-- meghívó mappa UUID**
- nev

#### Határozatok (hat)
> /**hat**/folders?year=[year]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/hat/folders?year=2024  
- datum
- kategoria
- idopont
- hely
- uuid **<-- határozat mappa UUID**
- nev

#### Jegyzőkönyvek (jegy)
> /**hat**/folders?year=[year]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/jegy/folders?year=2024  
- datum
- kategoria
- idopont
- hely
- uuid **<-- jegyzőkönyv mappa UUID**
- nev

## Meghívók

#### `Minden meghívót mappa UUID azonosít`
---

### Meghívó API Endpointok

`Az alábbi meghívó endpontok mind egy sornyi adatot adnak vissza`

#### Meghívó részletek (detail)
> /**detail**?id=[folder_UUID]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/detail?id=3dd07e6f-2885-11ef-a7ed-e70a27390546


* datum
* gyujto
* kategoria
* folapra
* eloterjeszto
* targy
* napirend
* uuid **<--mappa UUID**
* nyilvanossagjelolo
* testuletijelolo
* dateLastModified
* name
* idopont
* hely
* nev
* iktatoszam
---


#### Bizottsági  (biz)
> /inv/**biz**?id=[folder_UUID]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/inv/biz?id=a57cdad5-4a65-11ef-a077-e70a27390546

- datum
- nyilvanossagjelolo
- kategoria
- idopont
- hely
- uuid **<--bizottság UUID**
- nev
---

#### Testületi (test)
> /inv/**test**?id=[folder_UUID]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/inv/test?id=8ba08f48-4373-11ef-a7ed-e70a27390546

- datum
- nyilvanossagjelolo
- kategoria
- idopont
- hely
- uuid **<--testület UUID**
- nev
---

## Napirendi pont  

`A napirendi pontok apija nem egységes, míg a testületi napirendi pontokhoz elég a testület mappa UUID, 
addig a bizottság már bizottság mappa UUID-t és bizottság UUID-t is kér`

### Testület
> inv/listtest?id=[testület_UUID]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/inv/listtest?id=8ba08f48-4373-11ef-a7ed-e70a27390546

- gyujto
- nyilvanossagjelolo
- hasPermissions
- folapra
- eloterjeszto
- targy
- name
- napirend
- uuid **<--Testület napirend UUID**
- linkName
- referencia

### Bizottság

>inv/list?id=[bizottság mappa UUID]id2=[bizottság UUID]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/inv/list?id=5417b7af-2fae-11ef-a7ed-e70a27390546&id2=545b0250-2fae-11ef-a7ed-e70a27390546

- gyujto
- nyilvanossagjelolo
- hasPermissions
- folapra
- eloterjeszto
- targy
- name
- napirend
- uuid **<--Bizottság napirend UUID**
- linkName
- referencia

---
## Döntési / határozati javaslatok dokumentumai (pdf)

>/elo/djav/uuid=[meghívó uuid]&uuid2=[napirendi pont uuid]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/elo/djav?uuid=8ba08f48-4373-11ef-a7ed-e70a27390546&uuid2=25ac459d-4d89-11ef-a077-e70a27390546

- gyujto
- nyilvanossagjelolo
- dateLastModified
- statetext
- name **<---dokumentum név**
- userLastModified
- filesize
- uuid **<---dokumentum UUID**

---
## Előterjesztés mellékletek dokumentumai (pdf)

> elo/att/uuid=[meghívó UUID]&uuid2=[napirendi pont UUID]  
https://mikrodat.ujbuda.hu/app/cms/api/honlap/elo/att?uuid=8ba08f48-4373-11ef-a7ed-e70a27390546&uuid2=25ac459d-4d89-11ef-a077-e70a27390546

- gyujto
- nyilvanossagjelolo
- dateLastModified
- statetext
- name **<---dokumentum név**
- userLastModified
- filesize
- uuid **<---dokumentum UUID**

## Jegyzőkönyvek
# TODO

## Határozatok
# TODO
