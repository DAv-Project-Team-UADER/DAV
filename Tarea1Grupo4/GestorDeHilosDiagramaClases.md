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
