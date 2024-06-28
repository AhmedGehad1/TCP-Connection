import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import deque
import redis
import json

# Import the UI form generated from the .ui file
from ui_form import Ui_MainWindow

class LivePlotWidget(FigureCanvas):
    def __init__(self, id, index, parent=None):
        self.index= index
        self.id=id
        self.figure = Figure()
        super().__init__(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.x_data = deque(maxlen=10)
        self.x_counter = 0

        if index == 0:
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Heart Rate')
            self.ax.set_title('Live Heart Rate Monitor')
            self.y_data = deque(maxlen=10)
            self.line, = self.ax.plot([], [], label='Heart Rate')
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_plot_h)
            self.timer.start(1000)  # Update plot every 1000 milliseconds

        else:
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Blood Pressure')
            self.ax.set_title('Live Blood Pressure Monitor')
            self.y_data_systolic = deque(maxlen=10)  # Data for systolic blood pressure
            self.y_data_diastolic = deque(maxlen=10)  # Data for diastolic blood pressure
            self.line_systolic, = self.ax.plot([], [], color='red', label='Systolic BP')  # Red line for systolic BP
            self.line_diastolic, = self.ax.plot([], [], color='blue', label='Diastolic BP')  # Blue line for diastolic BP
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_plot_b)
            self.timer.start(1000)  # Update plot every 1000 milliseconds

        # Redis connection
        self.r = redis.Redis(
            host='redis-16661.c55.eu-central-1-1.ec2.redns.redis-cloud.com',
            port=16661,
            password='iLi2QxUtJwj9PPVG9AbXWNOTF5aD5qO2',
            decode_responses=True
        )

    def fetch_from_redis(self, key):
        # Fetch blood pressure data from Redis
        data = self.r.get(key)
        if data:
            vital_signs = json.loads(data)
            print(json.dumps(vital_signs, indent=4))
            heart_rate = vital_signs.get('Heart Rate', None)
            systolic_bp = vital_signs.get('Systolic BP', None)
            diastolic_bp = vital_signs.get('Diastolic BP', None)
            return heart_rate,systolic_bp, diastolic_bp
        else:
            return None, None, None


    def update_plot_h(self):
        key = "vital_signs:" + self.id  # Replace 'patient_name' with the actual patient name
        heart_rate, _, _ = self.fetch_from_redis(key)
        if heart_rate is not None:
            # Update plot with new heart rate data from Redis
            self.y_data.append(heart_rate)
            self.x_counter += 1
            self.x_data.append(self.x_counter)

            self.line.set_data(list(self.x_data), list(self.y_data))

            self.ax.relim()
            self.ax.autoscale_view()
            self.draw()

    def update_plot_b(self):
        key = "vital_signs:" + self.id
        _, systolic_bp, diastolic_bp = self.fetch_from_redis(key)
        if systolic_bp is not None and diastolic_bp is not None:
            self.y_data_systolic.append(systolic_bp)
            self.y_data_diastolic.append(diastolic_bp)
            self.x_counter += 1
            self.x_data.append(self.x_counter)
            self.line_systolic.set_data(list(self.x_data), list(self.y_data_systolic))
            self.line_diastolic.set_data(list(self.x_data), list(self.y_data_diastolic))
            self.ax.relim()
            self.ax.autoscale_view()
            self.draw()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # submit button handling to get patient id
        self.ui.pushButton.clicked.connect(lambda: self.id_submit_VER2())

        # Initialize live_plot_widget to None
        self.live_plot_widget = None
        self.live_plot_widget_2 = None

        #combobox
        self.ui.comboBox.currentIndexChanged.connect(lambda: self.handle_Selector_Method())


    #Combobox choosing which detection we want 
    def handle_Selector_Method(self):
        index = self.ui.comboBox.currentIndex()
        if index == 0:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page1)
        if index == 1:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page2)
        self.id_submit_VER2()


    def id_submit_VER2(self):

        id = str(self.ui.lineEdit.text())

        index = self.ui.comboBox.currentIndex()

        ##heart rate
        if index == 0:
            if self.live_plot_widget:
                    self.live_plot_widget.id = id
                    self.live_plot_widget.update_plot_h()
            else:
                # Create a new instance of LivePlotWidget
                self.live_plot_widget = LivePlotWidget(id, 0)

            # Add LivePlotWidget to page pg2
            frame_layout = QVBoxLayout()
            frame_layout.addWidget(self.live_plot_widget)
            self.ui.frame_2.setLayout(frame_layout)

        ##Blood pressure 
        if index == 1:
            if self.live_plot_widget_2:
                    self.live_plot_widget_2.id = id
                    self.live_plot_widget_2.update_plot_b()
            else:
                # Create a new instance of LivePlotWidget
                self.live_plot_widget_2 = LivePlotWidget(id, 1)

            # Add LivePlotWidget to page pg2
            frame_layout = QVBoxLayout()
            frame_layout.addWidget(self.live_plot_widget_2)
            self.ui.frame_4.setLayout(frame_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())