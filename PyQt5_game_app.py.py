import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtCore import QTimer, Qt, QRectF, QSizeF, QUrl
from PyQt5.QtGui import QBrush
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem

class BallGame(QGraphicsView):
    def __init__(self, parent=None):
        super(BallGame, self).__init__(parent)

        # Set up the scene and view
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setFixedSize(800, 600)

        # Set up video background
        self.video_item = QGraphicsVideoItem()
        self.video_item.setSize(QSizeF(800, 600))  # Use QSizeF instead of QSize
        self.scene.addItem(self.video_item)
        
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_item)
        video_url = QUrl.fromLocalFile('video')
        self.media_player.setMedia(QMediaContent(video_url))
        self.media_player.play()

        # Connect the mediaStatusChanged signal to a slot to loop the video
        self.media_player.mediaStatusChanged.connect(self.loop_video)

        # Add paddle (player)
        self.paddle = QGraphicsRectItem(0, 0, 100, 20)
        self.paddle.setBrush(QBrush(Qt.blue))
        self.paddle.setPos(350, 550)
        self.scene.addItem(self.paddle)

        # Add ball
        self.ball = QGraphicsEllipseItem(0, 0, 20, 20)
        self.ball.setBrush(QBrush(Qt.red))
        self.ball.setPos(390, 300)
        self.scene.addItem(self.ball)

        # Timer for ball movement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)

        # Ball movement direction
        self.dx = 2
        self.dy = 2

    def loop_video(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def update_position(self):
        # Move the ball
        new_x = self.ball.x() + self.dx
        new_y = self.ball.y() + self.dy

        # Bounce the ball off walls
        if new_x < 0 or new_x > 780:
            self.dx = -self.dx
        if new_y < 0 or new_y > 580:
            self.dy = -self.dy

        # Check if the ball hits the paddle
        if self.ball.collidesWithItem(self.paddle):
            self.dy = -self.dy

        self.ball.setPos(new_x, new_y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if self.paddle.x() > 0:
                self.paddle.moveBy(-20, 0)
        elif event.key() == Qt.Key_Right:
            if self.paddle.x() + 100 < 800:
                self.paddle.moveBy(20, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BallGame()
    window.show()
    sys.exit(app.exec_())
