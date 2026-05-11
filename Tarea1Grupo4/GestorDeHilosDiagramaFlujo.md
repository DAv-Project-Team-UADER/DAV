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
    I -- Sí --> J{¿es el último?}
    J -- No --> K[Imprimir i+1]
    K --> L[evento.set]
    J -- Sí --> L
    L --> M[sleep 1s]
    M --> N[Thread i imprime 'Hilo i cerrando']
    N --> I
    I -- No --> O[Imprimir 'listo']
    O --> P[join todos los hilos]
    P --> S([Fin])
```
