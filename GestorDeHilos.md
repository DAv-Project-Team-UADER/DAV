# GestorDeHilos — Documentación

**Autores:** Bianca Micaela Tournour, Maitén Blanc, Julian Agustín Olivera  
**Grupo 4 — Práctica Educativa Territorial FCyT-UADER, 2026**

---

## Descripción

`GestorDeHilos` gestiona el ciclo de vida de hasta N hilos de trabajo dentro del DAVCore.  
Levanta todos los hilos de forma secuencial (uno tras otro) y luego los cierra uno a uno
con un segundo de separación, mientras el hilo principal imprime la cuenta del 1 al 9
seguida de "listo".

---

## Diagrama de clases

```mermaid
classDiagram
    class GestorDeHilos {
        -int _maxHilos
        -list _hilos
        -list _eventos
        +__init__(maxHilos: int)
        +iniciar() void
        +detener() void
        -_tareaHilo(indice: int, evento: Event) void
    }
    class Thread {
        +start()
        +join()
    }
    class Event {
        +wait()
        +set()
    }
    GestorDeHilos --> Thread : crea y gestiona
    GestorDeHilos --> Event : usa para sincronizar
```

---

## Diagrama de flujo

```mermaid
flowchart TD
    A([Inicio]) --> B[GestorDeHilos.iniciar]
    B --> C{i < maxHilos?}
    C -- Sí --> D[Crear Event i]
    D --> E[Crear Thread i]
    E --> F[Thread i arranca y espera evento]
    F --> G[Imprimir 'Hilo i activo']
    G --> C
    C -- No --> H[GestorDeHilos.detener]
    H --> I{quedan hilos?}
    I -- Sí, i menor a maxHilos-1 --> J[Imprimir i+1]
    J --> K[evento.set]
    K --> L[sleep 1s]
    L --> M[Thread i imprime 'Hilo i cerrando']
    M --> I
    I -- último hilo --> N[evento.set]
    N --> O[sleep 1s]
    O --> P[Thread i imprime 'Hilo i cerrando']
    P --> Q[Imprimir 'listo']
    Q --> R[join todos los hilos]
    R --> S([Fin])
```
