## 1) Mappák

A mappák a Mikrodat által használt logikát tükrözik:


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

## 2 ) Meghívók

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

