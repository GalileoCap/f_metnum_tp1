# TP1 Métodos Numéricos - Trabajamos y nos divertimos...

## Análisis

Hay cuatro scripts de análisis, todos pueden ser corridos desde el shell de Pipenv.
~~~
pipenv shell
~~~

### `analyze_expected.py`

Este archivo corre nuestro programa y compara los resultados con los proveídos por la cátedra. Imprime en pantalla si los resultados están dentro del margen de error.  
Los gráficos y el output se guardan en el directorio `data/tests_alu`.

### `analyze_isotherm.py`

Este archivo analiza los cambios de la isoterma en base a la temperatura interna y la cantidad de radios. Los resultados se pueden ver en el directorio `data/isotherm`.

### `analyze_rounding.py`

Este archivo compara los resultados conseguidos usando `float` o `long double`. Imprime en pantalla si los resultados están dentro del margen de error.
Los gráficos se guardan en el directorio `data/rounding`

### `analyze.py`

Este archivo genera gráficos para datos generados aleatoriamente. El output se puede ver en los directorios `data/simple` y `data/big`.
