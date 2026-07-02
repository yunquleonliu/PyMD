from __future__ import annotations

import fitz  # PyMuPDF
from pdf2docx import Converter
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QScrollArea, QFileDialog, QMessageBox,
    QProgressBar, QSpinBox, QDialog, QListWidget,
    QListWidgetItem, QGroupBox, QRadioButton,
    QLineEdit, QApplication, QDialogButtonBox,
    QButtonGroup, QSizePolicy
)
from PyQt6.QtGui import QImage, QPixmap, QAction
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot

class PDFConverter:
    """Handles PDF conversion tasks."""
    
    @staticmethod
    def to_docx(pdf_path: str, docx_path: str, callback=None):
        """Convert PDF to DOCX."""
        try:
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
            return True
        except Exception as e:
            print(f"Conversion error: {e}")
            return False

    @staticmethod
    def to_markdown(pdf_path: str) -> str:
        """Extract text from PDF and format as basic Markdown."""
        try:
            doc = fitz.open(pdf_path)
            md_text = ""
            for i, page in enumerate(doc):
                # Basic text extraction
                # In the future, we can use smarter extraction for headers/tables
                text = page.get_text("text") 
                md_text += f"## Page {i+1}\n\n"
                md_text += text + "\n\n---\n\n"
            doc.close()
            return md_text
        except Exception as e:
            print(f"Extraction error: {e}")
            return ""

    @staticmethod
    def merge_pdfs(pdf_paths: list[str], output_path: str) -> bool:
        """Merge multiple PDF files into one."""
        try:
            merged = fitz.open()
            for path in pdf_paths:
                doc = fitz.open(path)
                merged.insert_pdf(doc)
                doc.close()
            merged.save(output_path)
            merged.close()
            return True
        except Exception as e:
            print(f"Merge error: {e}")
            return False

    @staticmethod
    def split_pdf_by_ranges(pdf_path: str, ranges: list[tuple[int, int]], output_dir: str) -> list[str]:
        """Split PDF by page ranges. Each range is (start, end) 1-based inclusive.
        Returns list of created file paths."""
        created = []
        try:
            doc = fitz.open(pdf_path)
            stem = Path(pdf_path).stem
            for i, (start, end) in enumerate(ranges):
                out_doc = fitz.open()
                out_doc.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
                out_path = str(Path(output_dir) / f"{stem}_part{i+1}.pdf")
                out_doc.save(out_path)
                out_doc.close()
                created.append(out_path)
            doc.close()
        except Exception as e:
            print(f"Split error: {e}")
        return created

    @staticmethod
    def split_pdf_every_n(pdf_path: str, n: int, output_dir: str) -> list[str]:
        """Split PDF into chunks of n pages each. Returns list of created file paths."""
        created = []
        try:
            doc = fitz.open(pdf_path)
            total = len(doc)
            stem = Path(pdf_path).stem
            chunk = 0
            for start in range(0, total, n):
                end = min(start + n - 1, total - 1)
                out_doc = fitz.open()
                out_doc.insert_pdf(doc, from_page=start, to_page=end)
                out_path = str(Path(output_dir) / f"{stem}_part{chunk+1}.pdf")
                out_doc.save(out_path)
                out_doc.close()
                created.append(out_path)
                chunk += 1
            doc.close()
        except Exception as e:
            print(f"Split error: {e}")
        return created


class PDFMergeDialog(QDialog):
    """Dialog for merging multiple PDF files."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("合并 PDF / Merge PDFs")
        self.setMinimumWidth(560)
        self.setMinimumHeight(420)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # File list group
        list_group = QGroupBox("待合并的 PDF 文件 / PDF files to merge")
        list_layout = QVBoxLayout(list_group)

        self.file_list = QListWidget()
        self.file_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.file_list.setToolTip("可拖拽调整顺序 / Drag to reorder")
        list_layout.addWidget(self.file_list)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("➕ 添加文件")
        self.add_btn.clicked.connect(self._add_files)
        self.remove_btn = QPushButton("➖ 移除所选")
        self.remove_btn.clicked.connect(self._remove_selected)
        self.up_btn = QPushButton("▲ 上移")
        self.up_btn.clicked.connect(self._move_up)
        self.down_btn = QPushButton("▼ 下移")
        self.down_btn.clicked.connect(self._move_down)
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.remove_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.up_btn)
        btn_row.addWidget(self.down_btn)
        list_layout.addLayout(btn_row)
        layout.addWidget(list_group)

        # Output file
        out_group = QGroupBox("输出文件 / Output file")
        out_layout = QHBoxLayout(out_group)
        self.out_path_edit = QLineEdit()
        self.out_path_edit.setPlaceholderText("选择保存路径… / Choose save path…")
        browse_btn = QPushButton("浏览…")
        browse_btn.clicked.connect(self._browse_output)
        out_layout.addWidget(self.out_path_edit)
        out_layout.addWidget(browse_btn)
        layout.addWidget(out_group)

        # Dialog buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("合并 / Merge")
        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def _add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "选择 PDF 文件", str(Path.home()), "PDF Files (*.pdf)"
        )
        for p in paths:
            item = QListWidgetItem(p)
            item.setToolTip(p)
            self.file_list.addItem(item)

    def _remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def _move_up(self):
        row = self.file_list.currentRow()
        if row > 0:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row - 1, item)
            self.file_list.setCurrentRow(row - 1)

    def _move_down(self):
        row = self.file_list.currentRow()
        if row < self.file_list.count() - 1:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row + 1, item)
            self.file_list.setCurrentRow(row + 1)

    def _browse_output(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "保存合并后的 PDF", str(Path.home()), "PDF Files (*.pdf)"
        )
        if path:
            self.out_path_edit.setText(path)

    def _on_accept(self):
        paths = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if len(paths) < 2:
            QMessageBox.warning(self, "文件不足", "请至少添加两个 PDF 文件。\nPlease add at least two PDF files.")
            return
        out = self.out_path_edit.text().strip()
        if not out:
            QMessageBox.warning(self, "未选择输出路径", "请指定输出文件路径。\nPlease specify an output file path.")
            return
        if not out.lower().endswith(".pdf"):
            out += ".pdf"
            self.out_path_edit.setText(out)

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            ok = PDFConverter.merge_pdfs(paths, out)
        finally:
            QApplication.restoreOverrideCursor()

        if ok:
            QMessageBox.information(self, "合并成功", f"已成功合并 {len(paths)} 个文件：\n{out}")
            self.accept()
        else:
            QMessageBox.critical(self, "合并失败", "PDF 合并失败，请检查文件是否有效。\nMerge failed. Please check the input files.")

    def get_output_path(self) -> str:
        return self.out_path_edit.text().strip()


class PDFSplitDialog(QDialog):
    """Dialog for splitting a PDF file."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("拆分 PDF / Split PDF")
        self.setMinimumWidth(500)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Input file
        in_group = QGroupBox("源 PDF 文件 / Source PDF file")
        in_layout = QHBoxLayout(in_group)
        self.in_path_edit = QLineEdit()
        self.in_path_edit.setPlaceholderText("选择 PDF 文件… / Choose PDF file…")
        self.in_path_edit.textChanged.connect(self._update_page_info)
        browse_in_btn = QPushButton("浏览…")
        browse_in_btn.clicked.connect(self._browse_input)
        in_layout.addWidget(self.in_path_edit)
        in_layout.addWidget(browse_in_btn)
        layout.addWidget(in_group)

        self.page_info_label = QLabel("")
        self.page_info_label.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(self.page_info_label)

        # Split mode
        mode_group = QGroupBox("拆分方式 / Split mode")
        mode_layout = QVBoxLayout(mode_group)

        self._btn_group = QButtonGroup(self)

        # Mode 1: by page ranges
        self.radio_ranges = QRadioButton("按页码范围 / By page ranges (e.g. 1-3, 4-6, 7-9)")
        self.radio_ranges.setChecked(True)
        self._btn_group.addButton(self.radio_ranges, 0)
        mode_layout.addWidget(self.radio_ranges)

        ranges_row = QHBoxLayout()
        ranges_row.addSpacing(20)
        ranges_row.addWidget(QLabel("页码范围 / Ranges:"))
        self.ranges_edit = QLineEdit()
        self.ranges_edit.setPlaceholderText("例如: 1-3, 4-6, 7  / e.g. 1-3, 4-6, 7")
        ranges_row.addWidget(self.ranges_edit)
        mode_layout.addLayout(ranges_row)

        # Mode 2: every N pages
        self.radio_every_n = QRadioButton("每 N 页拆分 / Every N pages")
        self._btn_group.addButton(self.radio_every_n, 1)
        mode_layout.addWidget(self.radio_every_n)

        n_row = QHBoxLayout()
        n_row.addSpacing(20)
        n_row.addWidget(QLabel("N ="))
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setMaximum(9999)
        self.n_spinbox.setValue(1)
        n_row.addWidget(self.n_spinbox)
        n_row.addStretch()
        mode_layout.addLayout(n_row)

        # Mode 3: each page separately
        self.radio_each = QRadioButton("每页单独拆分 / Each page as a separate file")
        self._btn_group.addButton(self.radio_each, 2)
        mode_layout.addWidget(self.radio_each)

        layout.addWidget(mode_group)

        # Toggle enabled state
        self._btn_group.idToggled.connect(self._on_mode_changed)
        self._on_mode_changed(0, True)

        # Output directory
        out_group = QGroupBox("输出目录 / Output directory")
        out_layout = QHBoxLayout(out_group)
        self.out_dir_edit = QLineEdit()
        self.out_dir_edit.setPlaceholderText("选择保存目录… / Choose output directory…")
        browse_out_btn = QPushButton("浏览…")
        browse_out_btn.clicked.connect(self._browse_output_dir)
        out_layout.addWidget(self.out_dir_edit)
        out_layout.addWidget(browse_out_btn)
        layout.addWidget(out_group)

        # Dialog buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("拆分 / Split")
        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def _on_mode_changed(self, btn_id: int, checked: bool):
        if not checked:
            return
        self.ranges_edit.setEnabled(btn_id == 0)
        self.n_spinbox.setEnabled(btn_id == 1)

    def _browse_input(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择 PDF 文件", str(Path.home()), "PDF Files (*.pdf)"
        )
        if path:
            self.in_path_edit.setText(path)
            # Auto-set output dir to same folder
            if not self.out_dir_edit.text():
                self.out_dir_edit.setText(str(Path(path).parent))

    def _browse_output_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录", str(Path.home()))
        if d:
            self.out_dir_edit.setText(d)

    def _update_page_info(self, path: str):
        """Show total page count of the selected PDF."""
        try:
            doc = fitz.open(path)
            total = len(doc)
            doc.close()
            self.page_info_label.setText(f"共 {total} 页 / Total: {total} pages")
        except Exception:
            self.page_info_label.setText("")

    def _parse_ranges(self, text: str, total_pages: int) -> list[tuple[int, int]] | None:
        """Parse range string like '1-3, 4-6, 7' into list of (start, end) tuples."""
        ranges = []
        for part in text.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                halves = part.split("-", 1)
                try:
                    s, e = int(halves[0].strip()), int(halves[1].strip())
                except ValueError:
                    return None
            else:
                try:
                    s = e = int(part)
                except ValueError:
                    return None
            if s < 1 or e < s or e > total_pages:
                return None
            ranges.append((s, e))
        return ranges if ranges else None

    def _on_accept(self):
        in_path = self.in_path_edit.text().strip()
        if not in_path or not Path(in_path).is_file():
            QMessageBox.warning(self, "文件无效", "请选择有效的 PDF 文件。\nPlease select a valid PDF file.")
            return

        out_dir = self.out_dir_edit.text().strip()
        if not out_dir:
            QMessageBox.warning(self, "未选择目录", "请选择输出目录。\nPlease choose an output directory.")
            return
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        try:
            doc = fitz.open(in_path)
            total = len(doc)
            doc.close()
        except Exception as e:
            QMessageBox.critical(self, "打开失败", f"无法打开 PDF：{e}")
            return

        mode = self._btn_group.checkedId()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            if mode == 0:
                ranges = self._parse_ranges(self.ranges_edit.text(), total)
                if not ranges:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.warning(
                        self, "页码范围无效",
                        f"请输入有效的页码范围（共 {total} 页）。\n"
                        f"Please enter valid page ranges (total {total} pages)."
                    )
                    return
                created = PDFConverter.split_pdf_by_ranges(in_path, ranges, out_dir)
            elif mode == 1:
                n = self.n_spinbox.value()
                created = PDFConverter.split_pdf_every_n(in_path, n, out_dir)
            else:
                created = PDFConverter.split_pdf_every_n(in_path, 1, out_dir)
        finally:
            QApplication.restoreOverrideCursor()

        if created:
            QMessageBox.information(
                self, "拆分成功",
                f"已生成 {len(created)} 个文件，保存至：\n{out_dir}"
            )
            self.accept()
        else:
            QMessageBox.critical(self, "拆分失败", "拆分过程中出现错误。\nSplit failed. Please check the input file.")


class PDFViewer(QWidget):
    """A simple read-only PDF Viewer using PyMuPDF."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._doc = None
        self._current_page = 0
        self._scale = 1.0
        self._setup_ui()
        
    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        
        # Toolbar
        self.toolbar_layout = QHBoxLayout()
        
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.clicked.connect(self.prev_page)
        
        self.page_label = QLabel("Page: 0/0")
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(self.next_page)
        
        self.zoom_in = QPushButton("+")
        self.zoom_in.clicked.connect(self.zoom_in_action)
        
        self.zoom_out = QPushButton("-")
        self.zoom_out.clicked.connect(self.zoom_out_action)
        
        self.toolbar_layout.addWidget(self.btn_prev)
        self.toolbar_layout.addWidget(self.page_label)
        self.toolbar_layout.addWidget(self.btn_next)
        self.toolbar_layout.addStretch()
        self.toolbar_layout.addWidget(QLabel("Zoom:"))
        self.toolbar_layout.addWidget(self.zoom_out)
        self.toolbar_layout.addWidget(self.zoom_in)
        
        self.layout.addLayout(self.toolbar_layout)
        
        # Scroll Area for Page Display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.image_label)
        
        self.layout.addWidget(self.scroll_area)
        
        # Actions for context menu or external usage
        self.convert_docx_btn = QPushButton("Convert to Word")
        self.convert_docx_btn.clicked.connect(self.convert_to_word_dialog)
        self.toolbar_layout.addStretch()
        self.toolbar_layout.addWidget(self.convert_docx_btn)

    def load_file(self, path: str):
        try:
            self._doc = fitz.open(path)
            self._current_page = 0
            self._update_page_label()
            self._render_page()
            self.convert_docx_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open PDF: {str(e)}")

    def _render_page(self):
        if not self._doc:
            return
            
        page = self._doc.load_page(self._current_page)
        mat = fitz.Matrix(self._scale, self._scale)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert fitz pixmap to QImage
        qt_img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_img))

    def prev_page(self):
        if self._doc and self._current_page > 0:
            self._current_page -= 1
            self._update_page_label()
            self._render_page()

    def next_page(self):
        if self._doc and self._current_page < len(self._doc) - 1:
            self._current_page += 1
            self._update_page_label()
            self._render_page()
            
    def zoom_in_action(self):
        self._scale += 0.25
        self._render_page()
        
    def zoom_out_action(self):
        if self._scale > 0.5:
            self._scale -= 0.25
            self._render_page()

    def _update_page_label(self):
        if self._doc:
            self.page_label.setText(f"Page: {self._current_page + 1}/{len(self._doc)}")
        else:
            self.page_label.setText("Page: 0/0")

    def convert_to_word_dialog(self):
        if not self._doc:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Word Document", "", "Word Documents (*.docx)"
        )
        if file_path:
            # Show progress (blocking for simplicity in MVP)
            # In production, use QThread
            QMessageBox.information(self, "Converting", "Starting conversion... This may take a moment.")
            success = PDFConverter.to_docx(self._doc.name, file_path)
            if success:
                QMessageBox.information(self, "Success", "Conversion complete!")
            else:
                QMessageBox.critical(self, "Error", "Conversion failed.")

