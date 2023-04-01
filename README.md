# Pràctica de compiladors, intèrpret Funx
Autor: Iván Gonzalez Reguera, estudiant del grau d'ingenieria informàtica a la FIB

## Descripció
Pràctica de Llenguatges de programació 2022-2023 Q1. Intèrpret per un llenguatge d'expresions i funcions.

## Contingut del repositori
- **funx.g4**: Conté la gramàtica del intèrpret Funx.
- **funx.py**: Conté el programa del intèrpret i els seus visitadors. Genera la pàgina web amb el template del fitxer html. Segueix les regles d'estil PEP8.
- El template del html a la carpeta **templates**

## Instalació

```
pip3 install antlr4-python3-runtime 
```
Descarregar l'axiu jar de la pàgina oficial de antlr,la última versió "https://www.antlr.org/", la versió 4.11.1. Una altra opció és descarregar-ho tot des de la terminal, a la seva pàgina també explica com fer-ho.


Moure el jar a la carpeta on està la gramàtica.

## Compilació

Per compilar executar:
```
java -jar antlr-4.11.1-complete.jar -Dlanguage=Python3 -no-listener -visitor funx.g4
```
O alternativament si tenim antlr amb la versió correcte instalada:
```
antlr4 -Dlanguage=Python3 -no-listener -visitor funx.g4
```
## Executar l'intèrpret

Per invocar l'intèrpret, en bash executar:
```
export FLASK_APP=funx
flask run
```
O també:
```
python3 funx.py
```
Si no s'obre automàticament el navegador amb el programa, manualment accedir a la pàgina "http://127.0.0.1:5000".
Per tancar el programa simplement prémer Ctrl+C.

## Funcionament

A la pàgina podrem veure una interfície on destaquen 3 elements:
- **Funcions**: Aquí s'aniran afegint el nom de les funcions que anem declarant, hi ha un scroll vertical si hi han moltes funcions.
- **Consola**: On l'usuari pot introduir el input (funcions o expresions) sota de la qual trobem el botó "Submit" per enviar la informació. 
- **Resultats**: On veurem els inputs i outputs del programa, els últims 5.

Per enviar una expressió o una funció cal escriure-la i donar-li a "submit". Es recomana enviar funcions i expressions d'una en una per claredat, tot i que l'intèrpret funciona si introduïm una declaració de funció i una trucada a aquella funció.

Les operacions treballen amb enters, inclosa la divisió. Per tant en cas d'introduir variables amb decimals es retornarà un error.
Exemple: 5.5 + 2 dóna error. 5 / 2 = 2

Per evaluar expressions cal introduir-les com faríem en una calculadora tradicional, per ejemple: "2*3" o "5 + 6". En el cas de funcions per trucar una funció cal introduir el seu nom (començant sempre per majúscula) i introduir els seus arguments, per exemple: "Suma2 3"

Per declarar funcions, introduïm el nom començant per majúscula, després introduim els parámetres (si hi té) que volem separats per espais i definir les instruccions de la funció, entre "{ }". Sempre hem d'acabar una instrucció amb una expressió que es el punt de sortida d'aquesta (el que seria un return en un llenguatge tradicional).

Si una variable no esta definida, o sigui, s'ha declarat malament una funció, es retorna una excepció.

## Exemple de declaració de funcions:

Si volem introduir la funció "Suma2 x" que donat un número li sumi 2 escribiríem:
`Suma2 x { 2 + x }` i a continuació la podrem veure en la interficie de **Funcions**.
En resultats trobarem com a input el que hem escrit i com a output: "None"; indicant que no ha hagut cap error en la declaració ja que aquesta operació no retorna res.

Ara per trucarla escribiríem `Suma2 3`, i en **Resultats** veuríem com a input el que hem escrit i output un 5 que es el resultat d'aplicar la funció Suma2 al número 3.

Per algún exemple més complexe que inclogui altres instruccions i condicionals a més de comentaris per la funció podem seguir el següent exemple:

`# funció que rep dos enters i en torna el seu maxim comu divisor`

`Euclides a b
{
  while a != b
  {
    if a > b 
    {
      a <- a - b
    }
    else
    {
      b <- b - a
    }
  }
  a
}`

I per trucarla: `Euclides 6 8` que retornarà 2.

