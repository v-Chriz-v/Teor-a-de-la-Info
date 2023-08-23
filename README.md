Esquema de comunicación.

El proposito del repositorio es el de almacenar el script que simulara un esquema de comunicación. Este se actualizara segun sea requerido y de acuerdo con los avances realizados en clase.

La fuente de información, de comienzo, sera una cadena de texto simple pero larga, lo suficiente para poder trabajar con los siguientes procesos. Esto tambien para poder trabajar de manera mas sencilla la traducción a codigo binario, necesaria para trabajar con los siguientes pasos.

El metodo de transmisión se encargara de codificar la cadena de texto, en mi caso opte por sumar un uno al codigo binario que representa la cadena en transmision. De igual forma al momento de llegar a la parte del receptor, la decodificación sera restandole el uno que se le agrego al codigo binario. 

Para el canal empleare una velocidad de 10Mb/s y por la parte del ruido se modificara la información de la cadena y tambien empleare una reducción de velocidad. Para este ultimo punto es importante mencionar que usare ciclos for para el envio de la información mediante el canal.

![Diagrama en blanco](https://github.com/v-Chriz-v/Teor-a-de-la-Info/assets/54335343/0fafcfc2-fd88-4aad-9378-7a8c087db8c1)
