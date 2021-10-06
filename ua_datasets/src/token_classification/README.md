# Mova Institute Part of speech dataset
This repo is created for POS tagging task to train model using ukrainian language.  
All files for train are available under 
https://lab.mova.institute/files/robochyi_tb.conllu.txt

Table of Contents
=======

-   [General info](#general-info)
-   [Parts of speech](#parts-of-speech)
-   [Examples](#examples)
-   [DATASET](#dataset)
-   [How to use](#how-to-use)
-   [File structure](#file-structure)


General info 
=======

Total amount of files: 647  
Tokens:	141 286  
Words: 111 739  
Sentences:	8016  

Parts of speech:
=======
<br/>
1.Noun - animate(anim) (example: deer), unknown-animate(unanim) (example: virus),<br/> inanimate(inanim) (example: door)<br/>  
deer `noun:anim:m:v_naz`, virus - `noun:unanim:f:v_naz:xp1`, door - `noun:inanim:p:v_naz:ns`  

Noun name:  
fname	first name	ім’я	Леопольд `noun:anim:m:v_naz:prop:fname`
lname	last name	прізвище	Кравець `noun:anim:m:v_naz:prop:lname`  
patr	patronym	по батькові	Леопольдівна `noun:anim:f:v_naz:prop:patr`  
nick	nickname прізвисько/окличка	собака Мушка `noun:anim:f:v_naz:prop:nick`  

Noun forms:  
v_naz	називний  
v_rod	родовий  
v_dav	давальний  
v_zna	знахідний  
v_oru	орудний  
v_mis	місцевий  
v_kly	кличний  


Plural forms:  
ns no singular	без однини	Шешори noun:inanim:p:v_naz:prop:ns  
np no plural	без множини  
s singular  
p plural  

Gender:  
m - masculine  
f - feminine  
n - neuter  

More info you can find here: </br>
https://github.com/mova-institute/zoloto/blob/master/docs/tagset.md#%D1%80%D0%B8%D1%81%D0%B8-%D1%84%D0%BE%D1%80%D0%BC

Examples
=======
|Primary parts of speech|Definition                  |Example                            
| -------------         |:--------------------------:|:---------------------------------:|
|`NOUN`                 |Іменник                     |зображення,футбол,людина            
|`VERB`                 |Дієслово                    |робити,грати,співати               
|`NUMR`                 |Числівник                   |один,два,сто                       
|`ADV`                  |Прислівник                  |абсолютно,безумовно,точно,яскраво  |
|`ADJ`                  |Прийменник                  |звичайна,веселий,грайливий,радісний|
|`PREP`                 |Прийменник                  |в,у,на,під,за                      |
|`CONJ`                 |Сполучник                   |і,та,й,але,а                       |
|`PART`                 |Частка                      |не,хай,нехай,де,аби                |              
|Additional parts of speech   |
|`PRON`                       |Займенник           |ти,ми,вони,я                       |
|`ADJP`                       |Дієприкметник       |Кохана,написана,прочитана,заспівана|
|`NUMR`                       |Порядковий числівник|перший,сотий,другий                |


У[ADP] домі[NOUN] римського[ADJ] патриція[NOUN] Руфіна[PROPN] була[VERB] прегарна[ADJ] фреска[NOUN],[PUNCT] зображення[NOUN] Венери[PROPN] та[CCONJ] Адоніса[PROPN].[PUNCT]

Ходить[VERB] постійно[ADV] у[PREP] драній[ADJP].
Зробив[VERB] перший[NUMR] крок[NOUN] для[PREP] неї[PRON].

Якось[ADV] зібралися[VERB] у[PREP] нього[PRON],[PUNCT] ховаючися[VERB] від[PREP] переслідувань[NOUN],[PUNCT] одновірці[NOUN] дружини[NOUN] – християнки[NOUN].[PUNCT]

Й[CONJ] одразу[ADV] ж[PART] узялися[VERB] замазувати[VERB] стіну[NOUN],[PUNCT] певні[ADJ] свого[PRON] права[NOUN] негайно[ADV] знищити[VERB] гріховне[ADJ],[PUNCT]
як[SCONJ] на[ADP] їх[DET] погляд[NOUN],[PUNCT] мальовидло[NOUN].[PUNCT]


DATASET
=======
A dataset with 115,500 sentences can be found here: https://drive.google.com/drive/folders/1NV5dEdBO_lO4FNbBqUoBzxpy91qDuKrX?usp=sharing

How to use
=======



File structure
=======
* <em>ENG_MAIN.txt, UKR_MAIN.txt</em> - core dataset with all 115,500 lines translated from English to Ukrainian language.
  * <em>ENG_0.txt - ENG_384.txt</em> - files which contain original text, 300 lines per each file.
  * <em>UKR_0.txt - UKR_384.txt</em> - translation of files <em>ENG_0.txt - ENG_384.txt</em>

```
Example:
File "ENG_281.txt" line #94 - Question: What amendment to the United States Constitution forbids cruel and unusual punishment?
File "UKR_281.txt" line #94 - Питання: Яка поправка до Конституції США забороняє жорстокі та незвичні покарання?

line #94 of the second file is an exact translation of line #94 in the first file.
```
# News Dataset
A dataset with 11000 parsed articles can be found here:
https://drive.google.com/drive/folders/1Hlx7J4AMvNRriDlB1zHRy4lb5BxptP76?usp=sharing

## File Structure
* <em>pravda_final_valid.csv, pravda_final_invalid.csv</em>  - core dataset wiht all 11000 articles  on Ukrainian langauge.
    * <em>pravda_final_valid.csv</em> - valid data which contain 4000 articles ready to use.
    * <em>pravda_final_invalid.csv</em> - invalid data which contain 7000 articles with some problems

