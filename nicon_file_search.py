import os
import sys
import shutil  # 파일 이동을 위해 추가
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
                             QLabel, QMessageBox, QToolTip)
from PyQt5.QtCore import Qt, QSize,QEvent
from PyQt5.QtGui import QPixmap, QIcon
import time

'''
니콘 파일 스캐너 삭제/이동 편의 목적 개별 파일에 대해서 수행한다.
'''

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
    search_input = None
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
        self.search_input = CustomLineEdit()
        self.search_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding-left: 10px;
                padding-right: 10px;
            }
        """)        
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
        # ★ 1. 프로그램이 처음 실행될 때 입력창에 포커스를 줍니다.
        self.search_input.setFocus()        

    def changeEvent(self, event):
        # QEvent.ActivationChange는 창의 활성화 상태가 변경될 때 발생합니다.
        if event.type() == QEvent.ActivationChange:
            if self.isActiveWindow():
                #print("GUI 창이 포커스 되었습니다! (Focus On)")
                # ★ 여기에 창이 포커스 되었을 때 실행하고 싶은 기능을 넣으세요.
                self.search_input.setFocus() 
        #self.search_input.setFocus()
        super().changeEvent(event)

    def search_files(self):
        query = self.search_input.text().strip()
        if not query:
            self.search_input.clear()
            return
        
        self.search_input.clear()
        self.current_search_label.setText(f"조회: {query}")
        self.result_list.clear()
        self.search_input.setFocus()

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

        # ★ 2. 이동 버튼 (삭제 버튼 바로 옆에 추가)
        move_btn = QPushButton("이동")
        move_btn.setFixedWidth(50)
        move_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        move_btn.clicked.connect(lambda checked, p=full_path, i=item: self.move_file_up(p, i))
        layout.addWidget(move_btn)        

       
        # 3. 정보 표시
        info_label = QLabel(f"{brand_name} \n{prod_name} \n{Period_name} \n{file_name}")
        info_label.setStyleSheet("margin-left: 10px;font-size:14px")
        # ★ 여기 두 줄을 추가/수정합니다.
        info_label.setFixedWidth(250)  # 가로 넓이를 250픽셀로 고정 (원하는 크기로 변경 가능)
        info_label.setWordWrap(True)   # 글자가 지정된 넓이를 넘어가면 자동으로 줄바꿈        
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

    # ★ 상위 폴더로 이동하는 메서드 추가
    def move_file_up(self, src_path, item):
        if not os.path.exists(src_path):
            QMessageBox.warning(self, "경고", "파일이 존재하지 않습니다.")
            return

        current_dir = os.path.dirname(src_path)
        # os.path.dirname을 한 번 더 쓰면 바로 위(상위) 폴더가 됩니다.
        parent_dir = os.path.dirname(current_dir)
        file_name = os.path.basename(src_path)
        dest_path = os.path.join(parent_dir, file_name)

        # 예외 처리: base_path보다 더 위로 올라가지 않도록 제한 (보안 및 에러 방지)
        if len(current_dir) <= len(self.base_path):
            QMessageBox.warning(self, "경고", "최상위 경로(base_path)보다 위로 이동할 수 없습니다.")
            return

        # 예외 처리: 목적지에 이미 같은 이름의 파일이 있는 경우
        if os.path.exists(dest_path):
            QMessageBox.warning(self, "이동 실패", f"상위 폴더에 이미 동일한 이름의 파일이 존재합니다.\n\n경로: {parent_dir}")
            return

        try:
            # 파일 이동 실행
            shutil.move(src_path, dest_path)
            
            # 이동 성공 시 UI 리스트에서 제거 (성공 메시지는 따로 띄우지 않아 작업 속도 유지)
            row = self.result_list.row(item)
            self.result_list.takeItem(row)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"파일 이동 중 오류 발생: {e}")

if __name__ == '__main__':
    # 툴팁 스타일 설정 (배경색 등)
    app = QApplication(sys.argv)
    QToolTip.setFont(app.font())
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a2a2a; border: 1px solid white; }")
    
    ex = FileCleanerApp()
    ex.show()
    sys.exit(app.exec_())