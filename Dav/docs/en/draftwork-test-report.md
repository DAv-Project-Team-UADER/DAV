# Validation and Test Report — Draft Workbench (`DraftWork`)

**Project:** DAV (Voice-Assisted Design / Accessible Selection for FreeCAD)  
**Date:** August 31, 2026  
**Base branch:** `DavCore`  
**Module evaluated:** `Dav/dic/Workbench/DraftWork`  

---

## 1. Objective
Verify the integration, voice navigation and correct execution of all the tools and geometries of the **Draft (`DraftWork`)** workbench in FreeCAD through DAV's subcontext system.

---

## 2. Test Methodology
1. **Startup:** Running the environment through `iniciar_dav.bat`.
2. **Environment activation:** Loading the `DraftWorkbench` workbench and creating a new document in FreeCAD.
3. **Voice navigation:**
   * Entry: `Base` → `mesa de trabajo` (`workbench`) → `banco de dibujo` (`draft`).
   * Descent and execution in each submodule (`circulo`, `arco`, `elipse`, `curva`, etc.).
   * Ascent by level using the `subir` / `volver` commands.
4. **Output verification:** Visual confirmation in the FreeCAD tree and in the DAV logs (`[DAV] OK (execute)` and `CreateObjects` processing).

---

## 3. Test Results Matrix

| Submodule | Voice Command | Action Executed | Result in FreeCAD / DAV | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Circle (`circle`)** | `"circulo"` → `"centro"` | `Executed center` | Geometry created and decomposed into vertices/edges (`Extrusion`/`Circle`). | **PASSED (OK)** ✅ |
| **Arc (`arc`)** | `"arco"` → `"centro"` / `"puntos"` | `Executed center` / `Executed points` | Creation of arcs by center and by 3 interactive points. | **PASSED (OK)** ✅ |
| **Ellipse (`ellipse`)** | `"elipse"` → `"elipse"` | `Executed center` | Ellipse created in the working plane. | **PASSED (OK)** ✅ |
| **Curves (`curve`)** | `"curva"` → `"bezier"` | `Executed bezier` | Bézier curve created (`BezCurve`). | **PASSED (OK)** ✅ |
| **Point placement (`pointplacement`)** | `"colocación de puntos"` → `"punto en coordenadas"` | `Executed pointatcoords` | Point created at absolute coordinates `(7.0, 5.0, 8.0)`. | **PASSED (OK)** ✅ |
| **Connect points (`pointconnect`)** | `"conectar puntos"` → `"conectar"` | `Executed connect` | Connection and linking of selected points. | **PASSED (OK)** ✅ |
| **Array / Pattern (`circular_array`)** | `"matriz"` → `"circular"` / `"matriz polar"` | `Executed circular` / `Executed polar` | Polar array created (114 lines and 76 associated points). | **PASSED (OK)** ✅ |
| **Annotations (`annotation`)** | `"anotación"` → `"editor"` | `Executed editor` | Annotation styles dialog opened. | **PASSED (OK)** ✅ |
| **Dimensions (`dimension`)** | `"dimensión"` → `"dimension"` | `Executed linear` | Linear dimensioning tool activated. | **PASSED (OK)** ✅ |
| **Modifications (`modify`)** | `"modificar"` → `"clonar"`, `"mover"`, `"rotar"`, `"espejo"`, `"desfase"`, `"boceto"` | `Executed clone`, `move`, `rotate`, `mirror`, `offset`, `sketch` | Modification and conversion operations applied to active objects. | **PASSED (OK)** ✅ |
| **Face Binder (`facebinder`)** | `"unir caras"` → `"crear"` / `"unir caras"` | `Executed create` | `Facebinder` surface created successfully. | **PASSED (OK)** ✅ |

---

## 4. Conclusions and Observations
* **Full operability:** All the tested tools of the `DraftWork` module worked without code exceptions or lockups in FreeCAD.
* **Clean navigation:** The subcontext navigation system respected the nested-submenu convention (Rule 4), allowing descent and ascent without keyword collisions.
* **Accessibility integration:** The `CreateObjects` subsystem automatically recognized and decomposed the generated geometries into points and edges for future voice navigation.
