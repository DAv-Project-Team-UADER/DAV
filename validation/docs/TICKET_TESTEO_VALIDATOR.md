# Ticket de testeo — Validator

Completar y adjuntar capturas en el Word o en esta carpeta.

| Campo | Valor |
|-------|-------|
| Módulo | `validation/Validator` |
| Rama | `Pruebas` |
| Fecha | __________ |
| Integrantes | __________ |

---

## CP-01 — Documento activo + demo automática

- [ ] Ejecuté `App.newDocument("PruebaValidator")`
- [ ] Ejecuté `RunValidatorPrueba()`
- [ ] geometry creó `LineaDemo` (es/en/pt)
- [ ] additive sin sketch mostró error esperado
- [ ] caso `NoExiste` mostró error esperado

**Captura:** __________  
**Estado:** [ ] OK  [ ] FAIL  
**Observaciones:** __________

---

## CP-02 — Geometry OK (`MiLinea`)

- [ ] `CallIfValid` con coords válidas creó `MiLinea`
- [ ] Objeto visible en árbol del documento

**Captura consola:** __________  
**Captura árbol:** __________  
**Estado:** [ ] OK  [ ] FAIL  

---

## CP-03 — Geometry ERROR (tipo incorrecto)

- [ ] `x1 = "hola"` produjo error de conversión
- [ ] No se creó objeto `Fail`

**Captura:** __________  
**Estado:** [ ] OK  [ ] FAIL  

---

## CP-04 — GetRequirements tres idiomas (geometry)

- [ ] Español: Dato1…
- [ ] Inglés: Data1…
- [ ] Portugués: Dado1…

**Captura:** __________  
**Estado:** [ ] OK  [ ] FAIL  

---

## CP-05 — Additive OK (con Sketch)

- [ ] Sketch creado en Sketcher
- [ ] `CallIfValid` con `"sketch": "Sketch"` ejecutó Pad
- [ ] Consola: `[additive] Pad on 'Sketch'...`

**Captura:** __________  
**Estado:** [ ] OK  [ ] FAIL  

---

## CP-06 — Additive ERROR (objeto inexistente)

- [ ] `"sketch": "NoExiste"` → error, no ejecuta

**Captura:** __________  
**Estado:** [ ] OK  [ ] FAIL  

---

## CP-07 — Tests automáticos (opcional)

- [ ] `python validation/run_tests.py` → 12 tests OK

**Captura terminal:** __________  
**Estado:** [ ] OK  [ ] FAIL  [ ] N/A  

---

## Conclusión general

_____________________________________________________________

_____________________________________________________________

**Firma / fecha entrega:** __________
