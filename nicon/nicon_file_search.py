import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
                             QLabel, QMessageBox)
from PyQt5.QtCore import Qt

class FileCleanerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.base_path = r'C:\ncnc'
        # 기본 경로가 없을 경우 생성 (테스트 용도)
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            
        self.initUI()

    def initUI(self):
        # 레이아웃 설정
        self.main_layout = QVBoxLayout()
        
        # 상단: 검색 영역
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색할 파일명을 입력하세요...")
        self.search_input.returnPressed.connect(self.search_files) # 엔터키 지원
        
        self.search_btn = QPushButton("검색")
        self.search_btn.clicked.connect(self.search_files)
        
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_btn)
        
        # 중단: 결과 리스트
        self.result_list = QListWidget()
        
        # 레이아웃 합치기
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addWidget(QLabel(f"기본 경로: {self.base_path}"))
        self.main_layout.addWidget(self.result_list)
        
        self.setLayout(self.main_layout)
        self.setWindowTitle('파일 관리 및 삭제 프로그램')
        self.setGeometry(300, 300, 600, 400)

    def search_files(self):
        """지정된 경로에서 파일을 검색하여 리스트에 표시"""
        query = self.search_input.text().strip()
        self.result_list.clear()
        
        if not query:
            QMessageBox.warning(self, "알림", "검색어를 입력해주세요.")
            return

        try:
            for root, dirs, files in os.walk(self.base_path):
                for file in files:
                    if query in file:
                        file_path = os.path.join(root, file)
                        self.add_file_item(file, file_path)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"파일을 찾는 중 오류 발생: {e}")

    def add_file_item(self, file_name, file_path):
        """리스트에 파일 정보와 삭제 버튼을 커스텀 위젯으로 추가"""
        item = QListWidgetItem(self.result_list)
        custom_widget = QWidget()
        layout = QHBoxLayout()
        
        # 파일 정보 표시 (파일명 & 경로)
        info_label = QLabel(f"파일명: {file_name}\n경로: {file_path}")
        info_label.setWordWrap(True)
        
        # 삭제 버튼
        del_btn = QPushButton("삭제")
        del_btn.setFixedWidth(60)
        del_btn.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold;")
        del_btn.clicked.connect(lambda: self.delete_file(file_path, item))
        
        layout.addWidget(info_label)
        layout.addStretch()
        layout.addWidget(del_btn)
        
        custom_widget.setLayout(layout)
        item.setSizeHint(custom_widget.sizeHint())
        
        self.result_list.addItem(item)
        self.result_list.setItemWidget(item, custom_widget)

    def delete_file(self, path, item):
        """파일 삭제 실행 전 확인 및 삭제 후 UI 업데이트"""
        reply = QMessageBox.question(self, '삭제 확인', 
                                   f"정말로 아래 파일을 삭제하시겠습니까?\n\n{path}",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                os.remove(path)
                # 리스트에서 해당 항목 제거
                row = self.result_list.row(item)
                self.result_list.takeItem(row)
                QMessageBox.information(self, "완료", "파일이 삭제되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일 삭제 중 오류 발생: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileCleanerApp()
    ex.show()
    sys.exit(app.exec_())