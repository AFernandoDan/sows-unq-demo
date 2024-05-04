import asyncio

# esta funcion simula un proceso que toma un tiempo en ejecutarse
async def procesar_numero(numero):
    print(f"Procesando {numero}")
    await asyncio.sleep(numero)
    print(f"Terminado {numero}")

# este programa toma una lista de numeros del 10 al 1 y los procesa en paralelo
# es decir, cada numero se procesa en un hilo distinto, cuando un numero empieza a procesarse
# el programa no espera a que termine para procesar el siguiente numero
# esto se logra con la funcion asyncio.create_task que pone la tarea en segundo plano
# y con await asyncio.wait(asyncio.all_tasks()) que espera a que todas las tareas terminen

# en este caso la primera en terminar es la tarea que procesa el numero 1, 
# ya que es la que menos tiempo toma y la ultima en terminar es la tarea que
# procesa el numero 10 ya que espera 10 segundos para terminar
async def main():
    numeros = range(10, 0, -1)

    # Iterar sobre cada número en la lista de números
    for num in numeros:
        # Crear una tarea para procesar el número y ponerla en segundo plano
        asyncio.create_task(procesar_numero(num))

    # Esperar a que todas las tareas se completen
    await asyncio.wait(asyncio.all_tasks())

asyncio.run(main())