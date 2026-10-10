import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont

class PingPongPrototipo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prototipo del videojuego Ping-Pong")
        self.resize(800, 600)
        
        # Habilitar el enfoque de teclado explícito en la ventana
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Parámetros de la pelota
        self.ball_x = 400
        self.ball_y = 300
        self.ball_speed_x = 6
        self.ball_speed_y = 4
        self.ball_radius = 15

        # Parámetros de las paletas
        self.paddle_width = 20
        self.paddle_height = 100
        self.paddle_speed = 10
        
        self.paddle_left_x = 50
        self.paddle_left_y = 250
        
        self.paddle_right_x = 730
        self.paddle_right_y = 250

        # Control del estado inicial (Comienza pausado)
        self.juego_iniciado = False
        self.keys_pressed = set()

        # Temporizador del bucle principal
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo celeste claro
        painter.fillRect(self.rect(), QColor("#D0F4DE"))

        # Dibujar Paleta Izquierda (Teclas W / S)
        painter.setBrush(QBrush(QColor("black")))
        painter.drawRoundedRect(self.paddle_left_x, self.paddle_left_y, 
                                 self.paddle_width, self.paddle_height, 5, 5)

        # Dibujar Paleta Derecha (Teclas Flecha Arriba / Abajo)
        painter.drawRoundedRect(self.paddle_right_x, self.paddle_right_y, 
                                 self.paddle_width, self.paddle_height, 5, 5)

        # Dibujar Pelota
        painter.setBrush(QBrush(QColor("#CCFF00")))
        painter.drawEllipse(int(self.ball_x - self.ball_radius), 
                            int(self.ball_y - self.ball_radius), 
                            self.ball_radius * 2, self.ball_radius * 2)

        # Mensaje superpuesto si el juego no ha iniciado
        if not self.juego_iniciado:
            painter.setPen(QColor("black"))
            painter.setFont(QFont("Arial", 16, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "Presiona ESPACIO para lanzar la pelota\n\n[W / S] Izquierda  │  [▲ / ▼] Derecha")

    def keyPressEvent(self, event):
        # Iniciar/Pausar con la barra espaciadora
        if event.key() == Qt.Key_Space:
            self.juego_iniciado = True
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.keys_pressed.discard(event.key())

    def game_loop(self):
        # 1. Movimiento de las paletas (Funciona incluso antes de lanzar la pelota para acomodarse)
        if Qt.Key_W in self.keys_pressed and self.paddle_left_y > 0:
            self.paddle_left_y -= self.paddle_speed
        if Qt.Key_S in self.keys_pressed and self.paddle_left_y < self.height() - self.paddle_height:
            self.paddle_left_y += self.paddle_speed

        if Qt.Key_Up in self.keys_pressed and self.paddle_right_y > 0:
            self.paddle_right_y -= self.paddle_speed
        if Qt.Key_Down in self.keys_pressed and self.paddle_right_y < self.height() - self.paddle_height:
            self.paddle_right_y += self.paddle_speed

        # 2. Lógica de la pelota (Solo si ya se presionó espacio)
        if self.juego_iniciado:
            self.ball_x += self.ball_speed_x
            self.ball_y += self.ball_speed_y

            # Rebote superior e inferior
            if self.ball_y - self.ball_radius <= 0 or self.ball_y + self.ball_radius >= self.height():
                self.ball_speed_y = -self.ball_speed_y

            # Caja de colisiones virtuales
            ball_rect = QRectF(self.ball_x - self.ball_radius, self.ball_y - self.ball_radius, 
                               self.ball_radius * 2, self.ball_radius * 2)
            left_p_rect = QRectF(self.paddle_left_x, self.paddle_left_y, self.paddle_width, self.paddle_height)
            right_p_rect = QRectF(self.paddle_right_x, self.paddle_right_y, self.paddle_width, self.paddle_height)

            # Rebotes horizontales con paletas
            if ball_rect.intersects(left_p_rect) and self.ball_speed_x < 0:
                self.ball_speed_x = -self.ball_speed_x
            if ball_rect.intersects(right_p_rect) and self.ball_speed_x > 0:
                self.ball_speed_x = -self.ball_speed_x

            # Validación de pérdida / Derrota
            if self.ball_x < 0:
                print("¡Punto! El jugador Izquierdo falló.")
                self.reiniciar_pelota()
            elif self.ball_x > self.width():
                print("¡Punto! El jugador Derecho falló.")
                self.reiniciar_pelota()

        self.update()

    def reiniciar_pelota(self):
        """Regresa la pelota al centro y pausa el juego para la siguiente ronda."""
        self.ball_x = 400
        self.ball_y = 300
        self.ball_speed_x = -self.ball_speed_x  # Saca hacia el jugador que ganó el punto
        self.juego_iniciado = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PingPongPrototipo()
    ventana.show()
    sys.exit(app.exec_())
