import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
                             QLabel, QMessageBox, QToolTip)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon


class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.parent().search_files()
        else:
            super().keyPressEvent(event)

class ImageButton(QPushButton):
    """마우스 롤오버 시 이미지를 툴팁으로 보여주는 커스텀 버튼"""
    def __init__(self, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path
        # 마우스 추적 활성화 (툴팁용)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        # 마우스가 버튼 위에 올라왔을 때 이미지 툴팁 표시
        pixmap = QPixmap(self.file_path)
        if not pixmap.isNull():
            # 이미지 크기 조절 (미리보기 사이즈)
            pixmap = pixmap.scaled(QSize(300, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # HTML 형식을 사용하여 툴팁에 이미지 삽입 (메모리 내 경로 사용)
            # PyQt 툴팁은 제한적인 HTML을 지원하므로 파일 경로를 직접 넣습니다.
            self.setToolTip(f'<img src="{self.file_path}" width="250">')
        super().enterEvent(event)

class FileCleanerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.base_path = r'C:\ncnc'
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        
        self.search_layout = QHBoxLayout()
        self.search_input = CustomLineEdit(self)
        self.search_input.setPlaceholderText("파일명 입력 (엔터/스페이스 검색)")
        
        self.search_btn = QPushButton("검색")
        self.search_btn.clicked.connect(self.search_files)
        
        self.current_search_label = QLabel("")
        self.current_search_label.setStyleSheet("color: blue; font-weight: bold;")
        
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_btn)
        self.search_layout.addWidget(self.current_search_label)
        
        self.result_list = QListWidget()
        
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addWidget(QLabel(f"기본 경로: {self.base_path}"))
        self.main_layout.addWidget(self.result_list)
        
        self.setLayout(self.main_layout)
        self.setWindowTitle('NCNC 파일 관리자 - 이미지 미리보기 지원')
        self.setGeometry(300, 300, 600, 400)

    def search_files(self):
        query = self.search_input.text().strip()
        if not query:
            self.search_input.clear()
            return
        
        self.search_input.clear()
        self.current_search_label.setText(f"조회: {query}")
        self.result_list.clear()

        try:
            for root, dirs, files in os.walk(self.base_path):
                for file in files:
                    if query in file:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(root, self.base_path)
                        folder_display = rel_path.split('\\')[-1] if rel_path != "." else "Root"
                        self.add_file_item(folder_display, file, file_path, root)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"검색 중 오류 발생: {e}")

    def add_file_item(self, folder_name, file_name, full_path, folder_path):
        item = QListWidgetItem(self.result_list)
        custom_widget = QWidget()
        layout = QHBoxLayout()
        brand_name   = folder_path.split('\\')[2]
        prod_name    = folder_path.split('\\')[3]
        try:
            Period_name  = folder_path.split('\\')[4]
        except Exception as e:
            print(e)
            Period_name = ''        
        
        # 1. 삭제 버튼
        del_btn = QPushButton("삭제")
        del_btn.setFixedWidth(50)
        del_btn.setStyleSheet("background-color: #ff4d4d; color: white;")
        del_btn.clicked.connect(lambda: self.delete_file(full_path, item))
        layout.addWidget(del_btn)

       
        # 3. 정보 표시
        info_label = QLabel(f"{brand_name} \n{prod_name} \n{Period_name} \n{file_name}")
        info_label.setStyleSheet("margin-left: 10px;font-size:14px")
        layout.addWidget(info_label)
        
        layout.addStretch()

        # 2. 이미지 보기 버튼 (파일이 이미지인 경우만 추가)
        if file_name.lower().endswith(self.image_extensions):
            view_btn = ImageButton(full_path, "이미지")
            view_btn.setFixedWidth(60)
            view_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            # 클릭 시 시스템 뷰어로 열기
            view_btn.clicked.connect(lambda: os.startfile(full_path))
            layout.addWidget(view_btn)        

        # 4. 경로 복사 버튼
        copy_btn = QPushButton("경로 복사")
        copy_btn.setFixedWidth(80)
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(folder_path))
        layout.addWidget(copy_btn)
        
        layout.setContentsMargins(5, 5, 5, 5)
        custom_widget.setLayout(layout)
        item.setSizeHint(custom_widget.sizeHint())
        
        self.result_list.addItem(item)
        self.result_list.setItemWidget(item, custom_widget)

    def copy_to_clipboard(self, path):
        clipboard = QApplication.clipboard()
        clipboard.setText(path)

    def delete_file(self, path, item):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("삭제 확인")
        msg_box.setText(f"파일을 삭제하시겠습니까?\n{os.path.basename(path)}")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        
        if msg_box.exec_() == QMessageBox.Yes:
            try:
                os.remove(path)
                row = self.result_list.row(item)
                self.result_list.takeItem(row)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {e}")

if __name__ == '__main__':
    # 툴팁 스타일 설정 (배경색 등)
    app = QApplication(sys.argv)
    QToolTip.setFont(app.font())
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a2a2a; border: 1px solid white; }")
    
    ex = FileCleanerApp()
    ex.show()
    sys.exit(app.exec_())