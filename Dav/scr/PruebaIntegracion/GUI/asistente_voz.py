#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.
import sys
import os
import json
import threading
import queue
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QDialog, QFrame
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QFont
import vosk
import sounddevice as sd


# ================================================================
# HELP WINDOW
# ================================================================
class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda - Asistente de Voz")
        self.setMinimumSize(550, 500)
        self.setModal(False)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
                border-radius: 15px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("🎙️ ASISTENTE DE VOZ")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #7c3aed;")
        layout.addWidget(title)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #7c3aed; max-height: 2px;")
        layout.addWidget(line)
        
        help_text = QLabel(
            "🗣️ COMANDOS DE VOZ DISPONIBLES:\n\n"
            "🎮 CONTROL DE LA APP:\n"
            "   • 'ayuda' → abre esta ventana\n"
            "   • 'cerrar ayuda' → cierra esta ventana\n"
            "   • 'minimizar' → minimiza el programa\n"
            "   • 'maximizar' → maximiza el programa\n"
            "   • 'cerrar programa' → cierra la aplicación\n\n"
            "📏 COMANDOS TÉCNICOS:\n"
            "   • 'dibujar linea'\n"
            "   • 'dibujar circulo'\n"
            "   • 'acercar'\n"
            "   • 'guardar archivo'\n"
            "   • 'limpiar pantalla'\n\n"
            "📜 NAVEGACIÓN EN HISTORIAL:\n"
            "   • 'subir' → sube 5 comandos en el historial\n"
            "   • 'bajar' → baja 5 comandos en el historial\n\n"
            "💡 TIP: Hablá CLARO. También podés hacer CLICK."
        )
        help_text.setFont(QFont("Arial", 11))
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #e2e2e2; line-height: 1.6;")
        layout.addWidget(help_text)
    
        close_btn = QPushButton("CERRAR AYUDA")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #7c3aed;
                color: white;
                padding: 12px;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover { background-color: #6d28d9; }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)


# ================================================================
# VOSK VOICE THREAD 
# ================================================================
class VoiceWorker(QObject):
    finished = Signal()
    partial_result = Signal(str)
    final_result = Signal(str)
    status_signal = Signal(str)
    
    def __init__(self, model_path="vosk-model-small-es-0.42"):
        super().__init__()
        self.model_path = model_path
        self.running = True
        self.audio_queue = queue.Queue()
        
    def audio_callback(self, indata, frames, time, status):
        if status:
            pass
        self.audio_queue.put(bytes(indata))
        
    def run(self):
        try:
            self.status_signal.emit("Cargando modelo...")
            model = vosk.Model(self.model_path)
            recognizer = vosk.KaldiRecognizer(model, 16000)
            
            self.status_signal.emit("🎤 Micrófono activo - Escuchando...")
            
            stream = sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                channels=1,
                dtype='int16',
                callback=self.audio_callback
            )
            
            with stream:
                while self.running:
                    try:
                        data = self.audio_queue.get(timeout=0.5)
                        if recognizer.AcceptWaveform(data):
                            result = json.loads(recognizer.Result())
                            text = result.get("text", "")
                            if text:
                                self.final_result.emit(text)
                        else:
                            partial = json.loads(recognizer.PartialResult())
                            partial_text = partial.get("partial", "")
                            if partial_text:
                                self.partial_result.emit(partial_text)
                    except queue.Empty:
                        continue
                    except Exception as e:
                        self.status_signal.emit(f"Error: {e}")
                        
        except Exception as e:
            self.status_signal.emit(f"Error: {e}")
        finally:
            self.finished.emit()
            
    def stop(self):
        self.running = False


# ================================================================
# PRINCIPAL WINDOW
# ================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎙️ Asistente de Voz - Control por Comandos")
        self.setMinimumSize(900, 650)
        
        self.help_window = None
        self.history_scroll_position = 0  
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f0f1a;
            }
            QLabel {
                color: #e2e2e2;
            }
            QTextEdit {
                background-color: #1a1a2e;
                color: #e2e2e2;
                border: 2px solid #2d2d3d;
                border-radius: 12px;
                padding: 12px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #7c3aed;
            }
        """)
        
        self.setup_ui()
        self.start_voice_recognition()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel("🎙️ ASISTENTE DE VOZ PARA TÉCNICOS")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #7c3aed; padding: 10px;")
        main_layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("🎤 Iniciando...")
        self.status_label.setFont(QFont("Arial", 11))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("background-color: #1a1a2e; border-radius: 10px; padding: 8px; color: #fbbf24;")
        main_layout.addWidget(self.status_label)
        
        # User speech
        label_escuchando = QLabel("🔊 LO QUE ESTÁS DICIENDO:")
        label_escuchando.setFont(QFont("Arial", 12, QFont.Bold))
        label_escuchando.setStyleSheet("color: #a78bfa; margin-top: 10px;")
        main_layout.addWidget(label_escuchando)
        
        self.current_text = QTextEdit()
        self.current_text.setPlaceholderText("Habla... el texto aparecerá acá")
        self.current_text.setMaximumHeight(80)
        self.current_text.setFont(QFont("Arial", 14))
        self.current_text.setStyleSheet("background-color: #1a1a2e; border: 2px solid #7c3aed;")
        self.current_text.setReadOnly(True)
        main_layout.addWidget(self.current_text)
        
        # History
        label_historial = QLabel("📜 HISTORIAL DE COMANDOS:")
        label_historial.setFont(QFont("Arial", 12, QFont.Bold))
        label_historial.setStyleSheet("color: #a78bfa; margin-top: 10px;")
        main_layout.addWidget(label_historial)
        
        self.history_list = QTextEdit()
        self.history_list.setMaximumHeight(180)
        self.history_list.setFont(QFont("Arial", 11))
        self.history_list.setReadOnly(True)
        main_layout.addWidget(self.history_list)
        
        # Suggested Commands
        label_sugerencias = QLabel("💡 COMANDOS SUGERIDOS:")
        label_sugerencias.setFont(QFont("Arial", 12, QFont.Bold))
        label_sugerencias.setStyleSheet("color: #a78bfa; margin-top: 10px;")
        main_layout.addWidget(label_sugerencias)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        comandos = [
            ("📏 DIBUJAR LÍNEA", "dibujar linea"),
            ("⚪ DIBUJAR CÍRCULO", "dibujar circulo"),
            ("🔍 ACERCAR", "acercar"),
            ("💾 GUARDAR", "guardar archivo"),
            ("🧹 LIMPIAR", "limpiar pantalla")
        ]
        
        for texto, comando in comandos:
            btn = QPushButton(texto)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #7c3aed;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px;
                    font-size: 12px;
                    font-weight: bold;
                    min-height: 60px;
                }
                QPushButton:hover {
                    background-color: #6d28d9;
                }
            """)
            btn.clicked.connect(lambda checked, c=comando: self.execute_command(c, from_voice=False))
            buttons_layout.addWidget(btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Help Button
        help_button = QPushButton("❓ AYUDA (o decí 'ayuda')")
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 10px;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        help_button.clicked.connect(self.open_help_window)
        help_layout = QHBoxLayout()
        help_layout.addWidget(help_button, alignment=Qt.AlignCenter)
        main_layout.addLayout(help_layout)
        

    def start_voice_recognition(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, os.pardir, os.pardir, "vosk-model-small-es-0.42"))
        print("\n==============================")
        print("DIRECTORIO ACTUAL:")
        print(os.getcwd())
        print("\nDIRECTORIO DEL SCRIPT:")
        print(BASE_DIR)
        print("\nRUTA DEL MODELO:")
        print(MODEL_PATH)
        print("\n¿EXISTE EL MODELO?:")
        print(os.path.exists(MODEL_PATH))
        
        if os.path.exists(MODEL_PATH):
            print("\nCONTENIDO DEL MODELO:")
            print(os.listdir(MODEL_PATH))
        else:
            print("\n⚠️ NO SE ENCONTRÓ LA CARPETA DEL MODELO")
        
        print("==============================\n")
        
        self.voice_worker = VoiceWorker(model_path=MODEL_PATH)
        self.voice_thread = threading.Thread(target=self.voice_worker.run)
        self.voice_thread.daemon = True
        self.voice_worker.partial_result.connect(self.update_current_text)
        self.voice_worker.final_result.connect(self.process_voice_command)
        self.voice_worker.status_signal.connect(self.update_status)
        self.voice_thread.start()

    def update_status(self, msg):
        self.status_label.setText(msg)
        if "activo" in msg or "Escuchando" in msg:
            self.status_label.setStyleSheet("background-color: #1a1a2e; border-radius: 10px; padding: 8px; color: #4ade80;")
        elif "Error" in msg:
            self.status_label.setStyleSheet("background-color: #1a1a2e; border-radius: 10px; padding: 8px; color: #ef4444;")
        
    def update_current_text(self, text):
        self.current_text.setText(text)
        
    def process_voice_command(self, command):
        command_lower = command.lower().strip()
        self.current_text.setText(f"✅ Detectado: '{command}'")
        
        # AYUDA - abrir
        if command_lower == "ayuda":
            self.open_help_window()
            self.add_to_history("AYUDA (abrir)")
            return
            
        # CERRAR AYUDA
        if command_lower == "cerrar ayuda" or command_lower == "cerrar ventana":
            self.close_help_window()
            self.add_to_history("AYUDA (cerrar)")
            return
            
        # MINIMIZAR
        if command_lower == "minimizar":
            self.showMinimized()
            self.add_to_history("MINIMIZAR")
            return
            
        # MAXIMIZAR
        if command_lower == "maximizar":
            if self.isMaximized():
                self.showNormal()
                self.add_to_history("RESTAURAR")
            else:
                self.showMaximized()
                self.add_to_history("MAXIMIZAR")
            return
            
        # CERRAR PROGRAMA
        if command_lower == "cerrar programa" or command_lower == "cerrar app" or command_lower == "salir":
            self.add_to_history("CERRAR PROGRAMA")
            self.close()
            return
            
        # SUBIR en historial - desplaza 5 líneas hacia arriba
        if command_lower == "subir" or command_lower == "arriba":
            self.scroll_history(up=True)
            return
            
        # BAJAR en historial - desplaza 5 líneas hacia abajo
        if command_lower == "bajar" or command_lower == "abajo":
            self.scroll_history(up=False)
            return
            
        # COMANDOS TÉCNICOS
        if "linea" in command_lower or "línea" in command_lower:
            self.execute_command("dibujar linea", from_voice=True)
        elif "circulo" in command_lower or "círculo" in command_lower:
            self.execute_command("dibujar circulo", from_voice=True)
        elif "acercar" in command_lower:
            self.execute_command("acercar", from_voice=True)
        elif "guardar" in command_lower:
            self.execute_command("guardar archivo", from_voice=True)
        elif "limpiar" in command_lower or "borrar" in command_lower:
            self.execute_command("limpiar pantalla", from_voice=True)
        else:
            self.add_to_history(f"❌ No entendí: '{command}'")
            
    def scroll_history(self, up=True):
        """Desplaza el historial 5 líneas hacia arriba o abajo"""
        scrollbar = self.history_list.verticalScrollBar()
        current_value = scrollbar.value()
        
        # Obtener el paso de desplazamiento (aproximadamente 5 líneas)
        step = scrollbar.singleStep() * 5
        
        if up:
            new_value = current_value - step
            self.add_to_history("🔍 Subir 5 comandos")
        else:
            new_value = current_value + step
            self.add_to_history("🔍 Bajar 5 comandos")
        
        # Asegurar que no se salga de los límites
        new_value = max(scrollbar.minimum(), min(scrollbar.maximum(), new_value))
        scrollbar.setValue(new_value)
        
        # Mostrar feedback visual en el recuadro de texto actual
        direccion = "arriba" if up else "abajo"
        self.current_text.setText(f"📜 Desplazando historial {direccion}")
        
    def open_help_window(self):
        if self.help_window is None:
            self.help_window = HelpWindow(self)
            self.help_window.finished.connect(self.on_help_closed)
        self.help_window.show()
        self.help_window.raise_()
        self.help_window.activateWindow()
        self.status_label.setText("🎤 Ayuda abierta (decí 'cerrar ayuda')")
        
    def close_help_window(self):
        if self.help_window and self.help_window.isVisible():
            self.help_window.close()
            self.add_to_history("❓ Ventana de ayuda cerrada")
            self.status_label.setText("🎤 Escuchando...")
        
    def on_help_closed(self):
        self.help_window = None
        self.status_label.setText("🎤 Escuchando...")
            
    def execute_command(self, command, from_voice=True):
        source = "🎤 Voz" if from_voice else "🖱️ Botón"
        
        nombres = {
            "dibujar linea": "DIBUJAR LÍNEA",
            "dibujar circulo": "DIBUJAR CÍRCULO",
            "acercar": "ACERCAR VISTA",
            "guardar archivo": "GUARDAR ARCHIVO",
            "limpiar pantalla": "LIMPIAR PANTALLA"
        }
        
        nombre_comando = nombres.get(command, command.upper())
        self.add_to_history(f"{nombre_comando} ({source})")
        print(f"🔧 EJECUTANDO: {command}")
        
        if command == "limpiar pantalla":
            self.history_list.clear()
            self.add_to_history("🧹 Historial limpiado")
            
    def add_to_history(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_text = f"[{timestamp}] {text}"
        self.history_list.append(formatted_text)
        
        # Auto-scroll al final SOLO cuando agregamos un comando nuevo
        cursor = self.history_list.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.history_list.setTextCursor(cursor)
        
    def closeEvent(self, event):
        if hasattr(self, 'voice_worker'):
            self.voice_worker.stop()
        if hasattr(self, 'voice_thread'):
            self.voice_thread.join(timeout=1)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())