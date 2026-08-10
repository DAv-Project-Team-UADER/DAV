# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""Data contract between the voice engine and the DAV panel."""

from __future__ import annotations


class ContextEntryView:
    """One selectable entry of the active context, ready to be drawn.

    Plain data: it carries what the panel needs to render a button and to
    report back which phrase the user picked. It deliberately knows nothing
    about ``Browser``, FreeCAD or the file bridge, so the panel can be built
    and tested without any of them.

    Args:
        Spoken: phrase the user says (already translated), shown as tooltip.
        InternalKey: internal dictionary key, used to look the icon up.
        IsSubContext: True when selecting it descends into a submenu.

    Example::

        entry = ContextEntryView("explorador", "explorer", IsSubContext=True)
    """

    def __init__(self, Spoken: str, InternalKey: str, IsSubContext: bool = False) -> None:
        self.Spoken = Spoken
        self.InternalKey = InternalKey
        self.IsSubContext = IsSubContext

    def __repr__(self) -> str:
        kind = "sub" if self.IsSubContext else "cmd"
        return f"<ContextEntryView {kind} {self.Spoken!r} key={self.InternalKey!r}>"


class ContextView:
    """Snapshot of the active voice context, ready to be drawn.

    This is the whole input the panel needs to render itself. Whoever builds
    it decides where the data comes from: today the JSON written by the file
    bridge, after the migration the ``Browser`` in-process.

    Args:
        ContextPath: human readable path, e.g. ``"Base > workbench > part"``.
        SubMenus: entries that descend into another context.
        Commands: entries that execute a FreeCAD callable.

    Example::

        view = ContextView(
            "Base",
            [ContextEntryView("explorador", "explorer", IsSubContext=True)],
            [ContextEntryView("preferencias", "preferences")],
        )
    """

    #: Context path of the dictionary tree root; the panel hides "back" here.
    ROOT_PATH = "Base"

    def __init__(
        self,
        ContextPath: str = "",
        SubMenus: list[ContextEntryView] | None = None,
        Commands: list[ContextEntryView] | None = None,
    ) -> None:
        self.ContextPath = ContextPath
        self.SubMenus = SubMenus or []
        self.Commands = Commands or []

    def IsEmpty(self) -> bool:
        """True when there is nothing to draw."""
        return not self.SubMenus and not self.Commands

    def IsRoot(self) -> bool:
        """True when this is the top of the tree (no way further up)."""
        return not self.ContextPath or self.ContextPath == self.ROOT_PATH

    def Entries(self) -> list[ContextEntryView]:
        """Submenus first, then commands — the order they are drawn in."""
        return list(self.SubMenus) + list(self.Commands)

    @classmethod
    def FromDict(cls, Data: dict) -> "ContextView":
        """Build a view from the ``context_state.json`` contract.

        Kept so the panel can be fed by the current file bridge without
        knowing about it. Once the panel is docked inside FreeCAD the
        ``Browser`` builds the view directly and this stops being used.

        Args:
            Data: dict with ``context_path``, ``submenus`` and ``commands``;
                each entry a dict with ``spoken`` and ``key``.

        Returns:
            The parsed view, or an empty one when Data is not a dict.
        """
        if not isinstance(Data, dict):
            return cls()

        def _entries(RawList, IsSub: bool) -> list[ContextEntryView]:
            out = []
            for Raw in RawList or []:
                if not isinstance(Raw, dict):
                    continue
                Spoken = Raw.get("spoken") or Raw.get("key") or ""
                if not Spoken:
                    continue
                out.append(ContextEntryView(Spoken, Raw.get("key", ""), IsSub))
            return out

        return cls(
            Data.get("context_path", ""),
            _entries(Data.get("submenus"), True),
            _entries(Data.get("commands"), False),
        )
