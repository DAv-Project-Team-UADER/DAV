from ..draftcommand import runDraftCommand
from .ayuda import ayuda

annotation = {
    'editor': lambda: runDraftCommand("Draft_AnnotationStyleEditor"),
    'help': ayuda,
}