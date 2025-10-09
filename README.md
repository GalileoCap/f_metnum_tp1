# TP1 Métodos Numéricos - Trabajamos y nos divertimos...

## Integrantes

* F. Galileo Cappella Lewi, 653/20, https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip
* Juan Pablo Anachure, 99/16, https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip

## Compilar

Se compila con el script `https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip`. 

## Ejecutables

Hay tres ejecutables diferentes, todos reciben los mismos parámetros: Path al archivo de entrada, el path de salida, y el método deseados (0 Gauss, 1 LU). También todos reciben el mismo formato de archivo de input, que es el pedido por la cátedra:
~~~
ri re m+1 n isoterma ninst
T(ri, 0) ... T(ri, 2pi) T(re, 0) ... T(re, 2pi)
~~~
Se agregan más lineas de temperaturas en base a la cantidad de instancias


### Entrega
 
Este ejecutable devuelve el archivo de output pedido por la cátedra.  
Se puede correr un ejemplo:
~~~
./tp1 https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip 0
~~~

### Profiling

Este ejecutable devuelve una linea adicional que incluye los tiempos de corrida en nanosegundos (si corresponde el primero es el que tomó calcular la factorización LU), y `ninst` lineas de la posición de la isoterma pedida.  
Se puede correr un ejemplo:
~~~
https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip 1
~~~

### Float

Este ejecutable corre al programa usando `float` en lugar de `long double` como su tipo de punto flotante. Devuelve el mismo archivo de output pedido por la cátedra.

## Análisis

Ver archivo `https://raw.githubusercontent.com/janachure/f_metnum_tp1/main/unsensible/f_metnum_tp1.zip` dentro del directorio `analysis`
