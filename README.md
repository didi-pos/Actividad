<div align="center">
<h1>Actividad</h1>
  <p>
    Ingeniería Electrónica · Universidad Santo Tomás
    <br>
    <b>Didier Posse</b>
  </p>
</div>

<hr>

<div align="center">
  <p><em>Definiciones de Gestionamiento de Recursos Compartidos</em></p>
</div>

<hr>

<h2>¿Qué son los Hilos (Threads)?</h2>
<p>
  Los hilos (threads) son como trabajadores independientes dentro de un programa que pueden ejecutar tareas al mismo tiempo. Imagina una cocina: sin hilos, un solo cocinero hace todo (cortar, cocinar, lavar). Con hilos, varios cocineros trabajan simultáneamente: uno corta verduras mientras otro cocina la carne. En el juego, un hilo dibuja en pantalla, osea que se encarga de la parte gráfica del juego, como lo es renderizar el juego, mientras otro calcula colisiones, y los demás razonamientos lógicos haciendo que todo funcione más fluido sin que una tarea lenta bloquee las demás, esto hace una mejor distribución de las ejecuciones que se deben hacer para correr el juego.
</p>

<h2>¿Qué es Mutex (Mutual Exclusion)?</h2>
<p>
  Un mutex (Mutual Exclusion) es como un candado que asegura que solo un hilo a la vez pueda modificar una variable compartida. Piensa en el baño de tu casa: solo una persona puede usarlo a la vez. Cuando alguien entra, cierra el cerrojo (acquire), usa el baño, y al salir abre el cerrojo (release). En programación, si dos hilos intentan modificar la variable "score" simultáneamente sin mutex, podrías perder puntos. El mutex garantiza que cada hilo espere su turno para evitar conflictos y choques en la información que se este modificando, esto genera un orden en escritura y ejecución, como una via de trenes solo permite pasar a un tren a la vez.
</p>

<h2>¿Qué es el Semáforo?</h2>
<p>
  Un semáforo es como un mutex pero permite que N cantidad de hilos accedan a un recurso simultáneamente, no solo uno. Imagina un estacionamiento con 3 espacios: los primeros 3 autos entran sin problema, pero el cuarto debe esperar hasta que alguien salga. Se crea con <code>semaphore(3)</code>, donde 3 serian la cantidad de hilos que pueden estar activos y funciona con un contador interno: cada acquire() resta 1 al contador, y cuando llega a 0, los siguientes hilos se bloquean. Cada release() suma 1, liberando espacio para el siguiente hilo en espera. En el juego, el semáforo limita a máximo 3 enemigos morados simultáneos, mientras que los rojos pueden aparecer sin límite. Es perfecto para controlar recursos limitados como conexiones de red, canales de audio o memoria, es muy útil para tener un control más preciso de los recursos y sirve para ejecuciones más pesadas a diferencia del mutex.
</p>

<hr>

<div align="center">
  <p><em>Explicación de los Códigos</em></p>
</div>

<hr>

