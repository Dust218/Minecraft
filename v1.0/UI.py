import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,QMessageBox
import csv
import pandas as pd

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口大小和标题
        self.setGeometry(100, 100, 500, 250)
        self.setWindowTitle('投影材料翻译器')

        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建输入文件选择部分
        input_file_layout = QHBoxLayout()
        self.input_file_label = QLabel('选择输入的txt文件:', self)
        self.input_file_entry = QLineEdit(self)
        self.input_file_button = QPushButton('选择文件', self)
        self.input_file_button.clicked.connect(self.select_input_file)

        input_file_layout.addWidget(self.input_file_label)
        input_file_layout.addWidget(self.input_file_entry)
        input_file_layout.addWidget(self.input_file_button)
        main_layout.addLayout(input_file_layout)

        # 创建输出文件夹选择部分
        output_folder_layout = QHBoxLayout()
        self.output_folder_label = QLabel('选择输出文件夹:', self)
        self.output_folder_entry = QLineEdit(self)
        self.output_folder_button = QPushButton('选择文件夹', self)
        self.output_folder_button.clicked.connect(self.select_output_folder)

        output_folder_layout.addWidget(self.output_folder_label)
        output_folder_layout.addWidget(self.output_folder_entry)
        output_folder_layout.addWidget(self.output_folder_button)
        main_layout.addLayout(output_folder_layout)

        # 创建翻译按钮
        self.translate_button = QPushButton('翻译', self)
        self.translate_button.clicked.connect(self.translate)
        main_layout.addWidget(self.translate_button)

        # 应用布局
        self.setLayout(main_layout)

        self.df = pd.DataFrame(columns=['raw', 'chinese', 'number'])
        self.data_create()

    def select_input_file(self):
        # 打开文件选择对话框，只允许选择 .txt 文件
        file_selected, _ = QFileDialog.getOpenFileName(self, "选择输入的txt文件", "", "Text files (*.txt)")
        if file_selected:
            # 将选中的文件路径显示在输入框中
            self.input_file_entry.setText(file_selected)

    def select_output_folder(self):
        # 打开文件夹选择对话框
        folder_selected = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if folder_selected:
            # 将选中的文件夹路径显示在输入框中
            self.output_folder_entry.setText(folder_selected)


    def data_create(self):
        # 读取CSV文件
        data_file_path = 'blocks.csv'
        # 创建一个字典来存储英文名称和中文名称的对应关系
        self.name_mapping = {}
        # 读取CSV文件并构建映射字典
        with open(data_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 将英文名称转换为小写并用下划线替换空格
                name_processed = row['name'].strip().lower().replace(' ', '_')
                self.name_mapping[name_processed] = row['chinese']

    def read_txt(self,file_path):
        with open(file_path, 'r', encoding='utf-8') as blockfile:
            self.lines = blockfile.readlines()

    def translate(self):
        input_file = self.input_file_entry.text()
        output_folder = self.output_folder_entry.text()
        output_file = f"{output_folder}/材料表.txt"
        self.read_txt(input_file)
        # 处理每一行
        for line in self.lines:
            line = line.strip()  # 去除行末的换行符
            # 分割名称和数量
            if ':' in line:
                name, count = line.split(':', 1)
                # 将名称转换为小写并用下划线替换空格
                name_processed = name.strip().lower().replace(' ', '_')
                # 替换英文名称为中文名称
                chinese_name = self.name_mapping.get(name_processed, name.strip())
                # 输入df中
                self.df.loc[len(self.df)] = [name_processed, chinese_name, int(count.strip())]
                # print(f"中文: {chinese_name}-- 英文: {name_processed}-- 数量: {count.strip()}")
        df_sorted = self.df.sort_values(by='number',ascending=False)
        with open(output_file, 'w', encoding='utf-8') as file:
            for index, row in df_sorted.iterrows():
                file.write(f"{row['chinese']}: {row['number']}\n")
            self.show_completion_popup()

    def show_completion_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("翻译完成")
        msg.setWindowTitle("提示")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileSelector()
    ex.show()
    sys.exit(app.exec_())