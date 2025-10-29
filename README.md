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
  Un <b>semáforo</b> es similar a un mutex, pero más flexible, ya que permite que <b>muchos</b> hilos existan y corran, pero <b>solo N de ellos</b> pueden acceder/usar un recurso específico simultáneamente. Los demás hilos se bloquean (quedan vivos pero dormidos) hasta que se libere un espacio. 
  <br><br>
  Imagina un estacionamiento con 3 espacios: los primeros tres autos pueden entrar sin problema, pero el cuarto debe esperar a que uno salga.  
  Esto se puede representar como <code>semaphore(3)</code>, donde el número indica la <b>cantidad de hilos</b> que pueden estar activos simultáneamente.  
  <br><br>
  Funciona con un contador interno:  
  <ul>
    <li>Cada <code>acquire()</code> <b>resta 1</b> al contador.</li>
    <li>Cuando el contador llega a <b>0</b>, los hilos restantes deben esperar.</li>
    <li>Cada <code>release()</code> <b>suma 1</b>, liberando espacio para el siguiente hilo.</li>
  </ul><br>
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
      </ul><br>
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
      </ul><br>
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

<ol>
  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/bac8f2b9-cd29-4753-98e2-bf2b84f73f78"/></p>
    </div>
    <p>
      En esta sección se crean dos <b>mecanismos de sincronización</b> diferentes.  
      Primero, <code>player_lock</code> es un <b>mutex</b> creado con <code>threading.Lock()</code>, que permite que solo un hilo a la vez modifique la posición del jugador.  
      Segundo, <code>special_enemy_semaphore</code> es un <b>semáforo</b> creado con <code>threading.Semaphore(3)</code>, que actúa como un estacionamiento con 3 espacios: permite que máximo tres enemigos especiales morados existan simultáneamente en el juego.  
      <br><br>
      La diferencia clave es que el <b>mutex</b> solo permite un acceso a la vez, mientras que el <b>semáforo</b> permite <b>N accesos simultáneos</b> (en este caso, 3).
    </p>
  </li>
  
  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/0cf354b2-393c-44bf-b371-82a40c78195b"/></p>
    </div>
    <p>
      Esta función define el hilo que <b>genera enemigos rojos</b> sin ninguna restricción.  
      El bucle <code>while</code> se ejecuta continuamente mientras el juego esté corriendo.  
      Con una probabilidad aleatoria (1 en 60), crea un <b>diccionario</b> con las propiedades del enemigo: posición <code>x</code> aleatoria, <code>y</code> inicial en 120, velocidad de 2, color rojo y tipo “normal”.  
      Luego lo agrega a la lista <code>game.enemies</code> y registra el evento en el log.  
      Este hilo no usa semáforo, por lo que pueden aparecer tantos enemigos rojos como la probabilidad permita, demostrando la diferencia con los enemigos especiales que sí están limitados.
    </p>
  </li>
  
  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/f317dd7d-c48f-4546-a4d5-05ae4b86f5e2"/></p>
    </div>
    <p>
      Esta es la función más importante relacionada con el <b>semáforo</b>.  
      Cada enemigo especial ejecuta esta función en su propio <b>hilo independiente</b>.  
      Primero, el enemigo incrementa el contador de espera <code>special_waiting</code> y muestra un mensaje indicando que está esperando permiso.  
      Luego ejecuta <code>special_enemy_semaphore.acquire()</code>, que es la línea crítica:  
      <ul>
        <li>Si hay espacios disponibles (menos de 3 enemigos activos), el hilo continúa inmediatamente.</li>
        <li>Si ya hay 3 enemigos activos, el hilo se bloquea aquí, quedando en pausa hasta que otro enemigo haga <code>release()</code> y libere un espacio.</li>
      </ul><br>
      Una vez obtenido el permiso, decrementa <code>special_waiting</code>, incrementa <code>special_count</code> y registra que el enemigo está activo.
    </p>
  </li>
  
  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/de357e1e-235c-488e-b62d-5d371a174729"/></p>
    </div>
    <p>
      Esta sección muestra cómo el <b>enemigo especial libera su espacio</b> en el semáforo.  
      Después de que el enemigo “vive” por un tiempo (entre 3 y 6 segundos), se remueve de la lista <code>game.special_enemies</code> y se decrementa el contador <code>special_count</code>.  
      La línea crucial es <code>special_enemy_semaphore.release()</code>, que devuelve el permiso al semáforo, incrementando su contador interno de espacios disponibles.  
      Esto permite que otro enemigo que esté bloqueado esperando en <code>acquire()</code> se despierte y pueda aparecer.  
      Luego, la función <code>spawn_special_enemies_manager()</code> se encarga de intentar continuamente crear nuevos enemigos especiales con baja probabilidad (1 en 120), generando un nuevo hilo para cada uno mediante <code>threading.Thread()</code>.
    </p>
  </li>
  
  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/e32528e7-668a-4f5a-ad32-9541f27ad1b0"/></p>
    </div>
    <p>
      Esta función demuestra el uso del <b>mutex</b> (<code>player_lock</code>).  
      El hilo <code>auto_move_player()</code> mueve al jugador automáticamente de izquierda a derecha.  
      La línea clave es <b>“with player_lock:”</b>, que adquiere el mutex antes de modificar <code>game.player_x</code>.  
      Esto es crucial porque hay dos hilos que pueden modificar la posición del jugador:  
      <ul>
        <li>El hilo automático.</li>
        <li>El hilo principal, cuando el usuario presiona las flechas del teclado.</li>
      </ul><br>
      Sin el mutex, ambos hilos podrían modificar <code>player_x</code> simultáneamente, causando valores corruptos o movimientos erráticos.  
      El mutex garantiza que solo un hilo modifique la posición a la vez y, al salir del bloque “with”, el cerrojo se libera automáticamente, permitiendo que el otro hilo tome su turno.
    </p>
  </li>
  
  <li><br>
    <div align="center">
      <p><img width="850" src="https://github.com/user-attachments/assets/5c24d249-594f-4a42-afe6-465076e871c8"/></p>
    </div>
    <p>
      Esta sección inicia los <b>tres hilos secundarios</b> del programa.  
      Primero, se crea <code>thread_normal</code> para los enemigos rojos usando <code>threading.Thread()</code> con <code>target=spawn_normal_enemies</code>.  
      Luego, <code>thread_special</code> para los enemigos morados, administrados por el manager que controla el semáforo.  
      Finalmente, <code>thread_player</code> para el movimiento automático del jugador que utiliza el mutex.  
      <br><br>
      Todos los hilos tienen <b><code>daemon=True</code></b>, lo que significa que se cerrarán automáticamente cuando el programa principal finalice.  
      Cada hilo se inicia con <code>.start()</code>, y desde ese momento hay <b>cuatro hilos corriendo simultáneamente</b>:
      <ul>
        <li>El hilo principal (<b>render</b>).</li>
        <li>El hilo de enemigos normales.</li>
        <li>El manager de enemigos especiales.</li>
        <li>El hilo de movimiento automático del jugador.</li>
      </ul><br>
      Esta es la demostración visual de cómo <b>mutex</b> y <b>semáforo</b> trabajan en conjunto para coordinar múltiples hilos ejecutándose al mismo tiempo.
    </p>
  </li>
</ol>
