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

<h2>¿Qué son los <b>Hilos (Threads)</b>?</h2>
<p>
  Los <b>hilos</b> (<i>threads</i>) son como <b>trabajadores independientes</b> dentro de un programa que pueden ejecutar tareas al mismo tiempo.  
  Imagina una cocina: sin hilos, un solo cocinero hace todo (cortar, cocinar, lavar).  
  Con hilos, varios cocineros trabajan simultáneamente: uno corta verduras mientras otro cocina la carne.  
  <br><br>
  En el juego, por ejemplo, un hilo se encarga de <b>dibujar en pantalla</b> (renderizar gráficos), mientras otro <b>calcula colisiones</b> o realiza los <b>procesos lógicos</b> del juego.  
  Esto permite que todo funcione de forma más fluida, evitando que una tarea lenta bloquee a las demás.  
  En resumen, los hilos permiten una <b>mejor distribución del trabajo</b> y un aprovechamiento más eficiente del procesador.
</p>

<h2>¿Qué es un <b>Mutex (Mutual Exclusion)</b>?</h2>
<p>
  Un <b>mutex</b> (<i>Mutual Exclusion</i>) es como un <b>candado</b> que asegura que solo <b>un hilo a la vez</b> pueda acceder o modificar un recurso compartido.  
  <br><br>
  Piensa en el baño de tu casa: solo una persona puede usarlo al mismo tiempo.  
  Cuando alguien entra, <b>cierra el cerrojo</b> (<code>acquire()</code>), usa el baño, y al salir <b>abre el cerrojo</b> (<code>release()</code>).  
  <br><br>
  En programación, si dos hilos intentan modificar la variable <code>score</code> simultáneamente sin un mutex, podrías perder datos o generar errores.  
  El mutex garantiza que cada hilo espere su turno, evitando conflictos y manteniendo un <b>orden seguro en la escritura y ejecución</b>.  
  Es como una vía de tren donde solo puede pasar <b>un tren a la vez</b> para evitar choques.
</p>

<h2>¿Qué es un <b>Semáforo (Semaphore)</b>?</h2>
<p>
  Un <b>semáforo</b> es similar a un mutex, pero más flexible, ya que permite que <b>varios hilos</b> accedan al mismo recurso al mismo tiempo (hasta un límite definido).  
  <br><br>
  Imagina un estacionamiento con 3 espacios: los primeros tres autos pueden entrar sin problema, pero el cuarto debe esperar a que uno salga.  
  Esto se puede representar como <code>semaphore(3)</code>, donde el número indica la <b>cantidad de hilos</b> que pueden estar activos simultáneamente.  
  <br><br>
  Funciona con un contador interno:  
  <ul>
    <li>Cada <code>acquire()</code> <b>resta 1</b> al contador.</li>
    <li>Cuando el contador llega a <b>0</b>, los hilos restantes deben esperar.</li>
    <li>Cada <code>release()</code> <b>suma 1</b>, liberando espacio para el siguiente hilo.</li>
  </ul>
  <br>
  En el contexto del juego, el semáforo podría limitar a máximo <b>3 enemigos morados</b> activos al mismo tiempo, mientras que los enemigos rojos pueden aparecer sin límite.  
  Es ideal para <b>controlar recursos limitados</b> como conexiones de red, canales de audio o memoria.  
  Además, permite una <b>gestión más precisa</b> y eficiente del sistema, siendo muy útil para procesos más pesados en comparación con un mutex.
</p>

<hr>

<div align="center">
  <p><em>Explicación de los Códigos</em></p>
</div>

<hr>

<h2>Explicación del Código con mMtex</h2>

<ol>
  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/40eda16a-9e10-49cb-9aa0-b83d81ef4f82"/></p>
    </div>
    <p>
      En esta sección se crean tres <b>mutex</b> (candados) usando <code>threading.Lock()</code>.  
      El <b>game_state_lock</b> protege las variables del estado del juego, como <code>score</code>, <code>lives</code> y <code>level</code>.  
      El <b>enemies_lock</b> protege la lista de enemigos para evitar que se corrompa cuando varios hilos intentan modificarla al mismo tiempo.  
      Finalmente, el <b>player_lock</b> protege la posición del jugador (<code>player_x</code>, <code>player_y</code>), impidiendo que dos hilos cambien su ubicación simultáneamente y generen movimientos erráticos.  
      <br><br>
      Cada mutex funciona como un <b>cerrojo</b>: solo un hilo puede “entrar” y modificar la variable protegida, asegurando que los cambios sean consistentes y libres de errores.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/cfc59830-ee1b-4bb3-869f-2bd599c0ff29"/></p>
      <p><img width="850" src="https://github.com/user-attachments/assets/63f79184-6dc3-4a7c-ac68-09560b43dace"/></p>
    </div>
    <p>
      Aquí se define el hilo secundario <b><code>game_logic_thread()</code></b>, encargado de manejar toda la <b>lógica del juego</b> mientras el hilo principal se enfoca en el <b>dibujo y renderizado</b>.  
      Este hilo ejecuta un bucle <code>while</code> que:
      <ul>
        <li>Incrementa la dificultad con el tiempo (aumentando <code>enemy_speed</code> cada 300 frames).</li>
        <li>Genera nuevos enemigos.</li>
        <li>Mueve los enemigos existentes y detecta colisiones.</li>
      </ul>
      La clave está en las líneas <code>with game_state_lock:</code>, donde se utiliza el mutex para <b>proteger las modificaciones</b> de variables compartidas.  
      Sin este control, si dos hilos modificaran <code>game.game_time</code> al mismo tiempo, se podrían perder actualizaciones y el juego empezaría a comportarse de manera errática.  
      En resumen, este hilo mantiene el funcionamiento lógico del juego sin interferir con el procesamiento gráfico.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/365f06a7-3555-49f8-b5bc-0ffbfb21e469"/></p>
    </div>
    <p>
      Esta parte del código crea e inicia el hilo de lógica utilizando <code>threading.Thread()</code>.  
      El parámetro <code>target=game_logic_thread</code> indica qué función ejecutará este hilo, mientras que <code>daemon=True</code> hace que el hilo se cierre automáticamente cuando el programa principal finalice.  
      Luego, <code>logic_thread.start()</code> inicia su ejecución en paralelo.  
      <br><br>
      A partir de este punto, existen <b>dos hilos corriendo simultáneamente</b>:
      <ul>
        <li>El hilo principal, que maneja los <b>eventos de pygame</b> y el <b>renderizado visual</b>.</li>
        <li>El hilo secundario, que gestiona la <b>lógica interna</b> del juego, como colisiones y generación de enemigos.</li>
      </ul>
      Ambos hilos comparten variables protegidas por los mutex definidos anteriormente, lo que permite una ejecución paralela estable y sincronizada.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/da778a2e-6ac2-45fa-ad12-85bb38f6a48f"/></p>
    </div>
    <p>
      Al final del bucle principal, cuando el usuario cierra el juego, se realiza la <b>limpieza final</b>.  
      El <code>print()</code> indica que el juego terminó correctamente y muestra un mensaje en consola.  
      La línea <code>logic_thread.join(timeout=2)</code> es esencial, ya que le dice al programa principal:  
      <i>“espera hasta 2 segundos para que el hilo de lógica finalice sus tareas”</i>.  
      <br><br>
      Sin esta instrucción, el programa podría cerrarse abruptamente mientras el hilo de lógica aún ejecuta código, provocando errores o cierres inesperados.  
      El parámetro <b><code>timeout</code></b> evita que el programa se quede colgado indefinidamente.  
      Finalmente, <code>pygame.quit()</code> cierra la ventana y <code>sys.exit()</code> termina el programa de forma <b>segura y ordenada</b>.
    </p>
  </li>
</ol>

<h2>Explicación del Código con Semaforo</h2>

