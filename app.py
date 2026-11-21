import json

import sqlite3

import sys

from datetime import datetime

from pathlib import Path

 

from PySide6.QtCore import Qt, QDate

from PySide6.QtWidgets import (

    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,

    QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QListWidgetItem,

    QComboBox, QDialog, QDialogButtonBox, QMessageBox, QFileDialog, QSplitter,

    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit,

    QCheckBox, QAbstractItemView, QGroupBox, QInputDialog, QStackedWidget, QFrame, QScrollArea

)

 

APP_DIR = Path.home() / 'Documents' / 'ElectricalMailApp'

APP_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = APP_DIR / 'electrical_mail.db'

 

DEFAULT_TYPES = [('モータ・回転機', 'モータ解線', ['モータ容量', '解線日']),

 ('モータ・回転機', 'モータ結線', ['モータ容量', '結線日']),

 ('モータ・回転機', 'モータ解結線', ['モータ容量', '解線日', '結線日']),

 ('モータ・回転機', 'モータ整備', ['モータ容量', '希望作業日']),

 ('モータ・回転機', 'モータ交換・更新', ['モータ容量', '希望作業日']),

 ('モータ・回転機', 'モータ不具合調査', ['モータ容量', '希望作業日']),

 ('モータ・回転機', 'スリップリングブラシ交換', ['モータ容量', '希望作業日']),

 ('モータ・回転機', 'モータケーブル補修', ['ケーブル仕様', '希望作業日']),

 ('照明設備', '電灯補修', ['器具台数', '照明型式', '作業希望日']),

 ('照明設備', '照明器具交換', ['器具台数', '照明型式', '作業希望日']),

 ('照明設備', 'LED照明更新', ['器具台数', '照明型式', '作業希望日']),

 ('照明設備', '外灯補修', ['器具台数', '照明型式', '作業希望日']),

 ('照明設備', '非常灯・誘導灯補修', ['器具台数', '照明型式', '作業希望日']),

 ('照明設備', '照明スイッチ交換', ['器具台数', '照明型式', '作業希望日']),

 ('照明設備', '照明回路調査', ['器具台数', '照明型式', '作業希望日']),

 ('照明設備', '仮設照明設置', ['器具台数', '照明型式', '作業希望日']),

 ('電源・コンセント', 'コンセント補修', ['電圧', '希望作業日']),

 ('電源・コンセント', 'コンセント新設・増設', ['電圧', '希望作業日']),

 ('電源・コンセント', '電源新設', ['電圧', '希望作業日']),

 ('電源・コンセント', '電源ケーブル敷設', ['電圧', '希望作業日']),

 ('電源・コンセント', '電源回路変更', ['電圧', '希望作業日']),

 ('電源・コンセント', '仮設電源設置', ['電圧', '希望作業日']),

 ('電源・コンセント', '電源撤去', ['電圧', '希望作業日']),

 ('配電盤・MCC', 'MCC補修', ['盤名称', '停電範囲', '希望作業日']),

 ('配電盤・MCC', 'MCC盤改造', ['盤名称', '停電範囲', '希望作業日']),

 ('配電盤・MCC', '遮断器交換', ['盤名称', '遮断器型式', '停電日時']),

 ('配電盤・MCC', '電磁開閉器交換', ['盤名称', '停電範囲', '希望作業日']),

 ('配電盤・MCC', '分電盤補修・更新', ['盤名称', '停電範囲', '希望作業日']),

 ('配電盤・MCC', '盤内機器交換', ['盤名称', '停電範囲', '希望作業日']),

 ('配電盤・MCC', '盤内回路調査', ['盤名称', '停電範囲', '希望作業日']),

 ('制御・操作機器', '押しボタンスイッチ補修', ['機器番号', '希望作業日']),

 ('制御・操作機器', 'リミットスイッチ交換', ['機器番号', '希望作業日']),

 ('制御・操作機器', '近接スイッチ交換', ['機器番号', '希望作業日']),

 ('制御・操作機器', '光電管交換', ['機器番号', '希望作業日']),

 ('制御・操作機器', '電磁弁交換', ['機器番号', '希望作業日']),

 ('制御・操作機器', '制御回路補修', ['機器番号', '希望作業日']),

 ('制御・操作機器', 'シーケンス変更', ['機器番号', '希望作業日']),

 ('制御・操作機器', 'インバータ補修・交換', ['インバータ型式', 'モータ容量', '希望作業日']),

 ('ケーブル・配線', 'ケーブル敷設', ['ケーブル仕様', '敷設長', '敷設経路']),

 ('ケーブル・配線', 'ケーブル補修', ['ケーブル仕様', '敷設長', '希望作業日']),

 ('ケーブル・配線', 'ケーブル撤去', ['ケーブル仕様', '敷設長', '希望作業日']),

 ('ケーブル・配線', '電線管補修', ['ケーブル仕様', '敷設長', '希望作業日']),

 ('ケーブル・配線', 'ケーブルダクト補修', ['ケーブル仕様', '敷設長', '希望作業日']),

 ('ケーブル・配線', '配線調査', ['ケーブル仕様', '敷設長', '希望作業日']),

 ('通信・放送', '電話機補修・更新', ['対象機器', '希望作業日']),

 ('通信・放送', '電話回線工事', ['対象機器', '希望作業日']),

 ('通信・放送', 'LANケーブル敷設', ['ケーブル仕様', '敷設長', '敷設経路']),

 ('通信・放送', 'ページング補修', ['対象機器', '希望作業日']),

 ('通信・放送', '放送設備補修', ['対象機器', '希望作業日']),

 ('カメラ・監視', '監視カメラ補修', ['カメラ型式', '希望作業日']),

 ('カメラ・監視', '監視カメラ設置', ['カメラ型式', '希望作業日']),

 ('カメラ・監視', '監視カメラ移設', ['カメラ型式', '希望作業日']),

 ('カメラ・監視', 'カメラケーブル補修', ['カメラ型式', '希望作業日']),

 ('カメラ・監視', '監視モニター補修', ['カメラ型式', '希望作業日']),

 ('消防・防災', '自火報感知器交換', ['対象設備', '希望作業日']),

 ('消防・防災', '自火報発信機補修', ['対象設備', '希望作業日']),

 ('消防・防災', '自火報受信盤補修', ['対象設備', '希望作業日']),

 ('消防・防災', '火災報知設備調査', ['対象設備', '希望作業日']),

 ('消防・防災', 'サイレン・回転灯補修', ['対象設備', '希望作業日']),

 ('接地・避雷設備', 'アース線補修', ['対象設備', '希望作業日']),

 ('接地・避雷設備', 'アースリール補修', ['対象設備', '希望作業日']),

 ('接地・避雷設備', '接地抵抗測定', ['対象設備', '希望作業日']),

 ('接地・避雷設備', '避雷針補修', ['対象設備', '希望作業日']),

 ('接地・避雷設備', '静電接地補修', ['対象設備', '希望作業日']),

 ('点検・測定', '絶縁抵抗測定', ['対象設備', '測定希望日']),

 ('点検・測定', '電気回路調査', ['対象設備', '測定希望日']),

 ('点検・測定', '漏電調査', ['対象設備', '測定希望日']),

 ('点検・測定', '設備点検', ['対象設備', '測定希望日']),

 ('点検・測定', '高圧電気保護具点検', ['対象設備', '測定希望日']),

 ('その他', '電気設備撤去', ['希望作業日']),

 ('その他', '工事用仮設対応', ['希望作業日']),

 ('その他', '設備移設', ['希望作業日']),

 ('その他', '現地調査', ['希望作業日']),

 ('その他', 'その他電気工事', ['希望作業日'])]

 

def db():

    con = sqlite3.connect(DB_PATH)

    con.row_factory = sqlite3.Row

    return con

 

def init_db():

    with db() as con:

        con.execute('CREATE TABLE IF NOT EXISTS work_types (id INTEGER PRIMARY KEY, category TEXT NOT NULL, name TEXT NOT NULL, fields_json TEXT NOT NULL, UNIQUE(category, name))')

        con.execute('CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, name TEXT NOT NULL, contact TEXT, email TEXT, cc TEXT)')

        con.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)')

        con.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, company TEXT, subject TEXT, body TEXT, items_json TEXT, attachments_json TEXT, status TEXT)')

        # バージョン単位で一度だけ不足分を追加。利用者が後で削除した種類は復活させない。

        marker = con.execute("SELECT value FROM settings WHERE key='seed_catalog_v2'").fetchone()

        if marker is None:

            con.executemany('INSERT OR IGNORE INTO work_types(category,name,fields_json) VALUES (?,?,?)',

                            [(c, n, json.dumps(f, ensure_ascii=False)) for c, n, f in DEFAULT_TYPES])

            con.execute("INSERT INTO settings(key,value) VALUES ('seed_catalog_v2','2026-10-30')")

        if not con.execute('SELECT COUNT(*) FROM settings').fetchone()[0]:

            defaults = {

                'subject': '【工事依頼】{工事概要}',

                'intro': '{会社名}\n{担当者}様\n\nいつもお世話になっております。\n電計課の〇〇です。\n\n下記内容にて電気工事をお願いいたします。',

                'outro': 'ご対応の可否および日程について、ご確認いただけますと幸いです。\n\nよろしくお願いいたします。'

            }

            con.executemany('INSERT INTO settings(key,value) VALUES (?,?)', list(defaults.items()))

 

CATEGORY_ORDER = [

    'モータ・回転機', '照明設備', '電源・コンセント', '配電盤・MCC',

    '制御・操作機器', 'ケーブル・配線', '通信・放送', 'カメラ・監視',

    '消防・防災', '接地・避雷設備', '点検・測定', 'その他',

]

 

def fetch_types():

    """既存DBは変更せず、工事分類を指定順に表示する。"""

    with db() as con:

        records = [dict(row) for row in con.execute('SELECT * FROM work_types')]

    positions = {category: index for index, category in enumerate(CATEGORY_ORDER)}

    records.sort(key=lambda row: (

        positions.get(row['category'], len(CATEGORY_ORDER)),

        row['category'] if row['category'] not in positions else '',

        row['id'],

    ))

    return records

 

def fetch_companies():

    with db() as con:

        return [dict(x) for x in con.execute('SELECT * FROM companies ORDER BY name')]

 

def settings():

    with db() as con:

        return {x['key']: x['value'] for x in con.execute('SELECT * FROM settings')}

 

def alert(parent, message):

    QMessageBox.warning(parent, '確認', message)

 

class WorkTypeDialog(QDialog):

    def __init__(self, parent=None, record=None):

        super().__init__(parent)

        self.setWindowTitle('工事種類の登録・編集')

        self.resize(520, 340)

        layout = QFormLayout(self)

        self.category = QLineEdit(record['category'] if record else '')

        self.name = QLineEdit(record['name'] if record else '')

        self.fields = QTextEdit()

        self.fields.setPlaceholderText('1行につき1項目（例：解線日）')

        if record:

            self.fields.setPlainText('\n'.join(json.loads(record['fields_json'])))

        layout.addRow('工事分類', self.category)

        layout.addRow('工事種類', self.name)

        layout.addRow('専用入力項目（1行1項目）', self.fields)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)

        self.buttons.accepted.connect(self.validate)

        self.buttons.rejected.connect(self.reject)

        layout.addRow(self.buttons)

 

    def validate(self):

        fields = [x.strip() for x in self.fields.toPlainText().splitlines() if x.strip()]

        if not self.category.text().strip() or not self.name.text().strip():

            return alert(self, '分類と工事種類を入力してください。')

        if len(fields) != len(set(fields)):

            return alert(self, '専用入力項目に重複があります。')

        if any(x in ('工事場所', '設備名称', '作業内容') for x in fields):

            return alert(self, '工事場所・設備名称・作業内容は共通項目のため登録不要です。')

        self.accept()

 

    def values(self):

        return (self.category.text().strip(), self.name.text().strip(), json.dumps([x.strip() for x in self.fields.toPlainText().splitlines() if x.strip()], ensure_ascii=False))

 

class WorkTypeManager(QWidget):

    def __init__(self, changed):

        super().__init__()

        self.changed = changed

        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 3)

        self.table.setHorizontalHeaderLabels(['分類', '工事種類', '専用入力項目'])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table)

        buttons = QHBoxLayout()

        for title, fn in [('追加', self.add), ('編集', self.edit), ('削除', self.remove)]:

            b = QPushButton(title)

            b.clicked.connect(fn)

            buttons.addWidget(b)

        layout.addLayout(buttons)

        self.refresh()

 

    def refresh(self):

        self.records = fetch_types()

        self.table.setRowCount(len(self.records))

        for row, r in enumerate(self.records):

            for col, text in enumerate([r['category'], r['name'], ', '.join(json.loads(r['fields_json']))]):

                self.table.setItem(row, col, QTableWidgetItem(text))

 

    def selected(self):

        row = self.table.currentRow()

        return self.records[row] if 0 <= row < len(self.records) else None

 

    def add(self):

        d = WorkTypeDialog(self)

        if d.exec() == QDialog.DialogCode.Accepted:

            try:

                with db() as con:

                    con.execute('INSERT INTO work_types(category,name,fields_json) VALUES (?,?,?)', d.values())

            except sqlite3.IntegrityError:

                return alert(self, '同じ分類に同名の工事種類が登録されています。')

            self.refresh(); self.changed()

 

    def edit(self):

        r = self.selected()

        if not r:

            return alert(self, '編集する工事種類を選択してください。')

        d = WorkTypeDialog(self, r)

        if d.exec() == QDialog.DialogCode.Accepted:

            try:

                with db() as con:

                    con.execute('UPDATE work_types SET category=?,name=?,fields_json=? WHERE id=?', (*d.values(), r['id']))

            except sqlite3.IntegrityError:

                return alert(self, '同じ分類に同名の工事種類が登録されています。')

            self.refresh(); self.changed()

 

    def remove(self):

        r = self.selected()

        if not r:

            return alert(self, '削除する工事種類を選択してください。')

        if QMessageBox.question(self, '削除確認', f"「{r['name']}」を削除しますか？\n既存の依頼履歴は残ります。") == QMessageBox.StandardButton.Yes:

            with db() as con:

                con.execute('DELETE FROM work_types WHERE id=?', (r['id'],))

            self.refresh(); self.changed()

 

class CompanyDialog(QDialog):

    def __init__(self, parent=None, record=None):

        super().__init__(parent)

        self.setWindowTitle('協力会社登録・編集')

        layout = QFormLayout(self)

        self.widgets = {}

        for key, label in [('name','会社名'), ('contact','担当者名'), ('email','宛先（複数は ; 区切り）'), ('cc','CC（複数は ; 区切り）')]:

            w = QLineEdit((record or {}).get(key, '') or '')

            self.widgets[key] = w

            layout.addRow(label, w)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)

        buttons.accepted.connect(self.validate)

        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

 

    def validate(self):

        if not self.widgets['name'].text().strip():

            return alert(self, '会社名を入力してください。')

        self.accept()

 

    def values(self):

        return tuple(self.widgets[k].text().strip() for k in ('name','contact','email','cc'))

 

class CompanyManager(QWidget):

    def __init__(self, changed):

        super().__init__()

        self.changed = changed

        layout = QVBoxLayout(self)

        self.table = QTableWidget(0,4)

        self.table.setHorizontalHeaderLabels(['会社名','担当者','宛先','CC'])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table)

        row = QHBoxLayout()

        for title, fn in [('追加',self.add),('編集',self.edit),('削除',self.remove)]:

            b=QPushButton(title); b.clicked.connect(fn); row.addWidget(b)

        layout.addLayout(row)

        self.refresh()

 

    def refresh(self):

        self.records=fetch_companies()

        self.table.setRowCount(len(self.records))

        for i,r in enumerate(self.records):

            for j,key in enumerate(('name','contact','email','cc')):

                self.table.setItem(i,j,QTableWidgetItem(r[key] or ''))

 

    def selected(self):

        i=self.table.currentRow()

        return self.records[i] if 0<=i<len(self.records) else None

 

    def add(self):

        d=CompanyDialog(self)

        if d.exec()==QDialog.DialogCode.Accepted:

            with db() as con: con.execute('INSERT INTO companies(name,contact,email,cc) VALUES (?,?,?,?)',d.values())

            self.refresh();self.changed()

 

    def edit(self):

        r=self.selected()

        if not r: return alert(self,'会社を選択してください。')

        d=CompanyDialog(self,r)

        if d.exec()==QDialog.DialogCode.Accepted:

            with db() as con: con.execute('UPDATE companies SET name=?,contact=?,email=?,cc=? WHERE id=?',(*d.values(),r['id']))

            self.refresh();self.changed()

 

    def remove(self):

        r=self.selected()

        if not r: return alert(self,'会社を選択してください。')

        if QMessageBox.question(self,'確認',f"{r['name']} を削除しますか？")==QMessageBox.StandardButton.Yes:

            with db() as con: con.execute('DELETE FROM companies WHERE id=?',(r['id'],))

            self.refresh();self.changed()

 

class TemplateManager(QWidget):

    def __init__(self):

        super().__init__()

        form=QFormLayout(self)

        s=settings()

        self.subject=QLineEdit(s.get('subject',''))

        self.intro=QTextEdit(s.get('intro',''))

        self.outro=QTextEdit(s.get('outro',''))

        form.addRow('件名テンプレート',self.subject)

        form.addRow('冒頭文',self.intro)

        form.addRow('末尾文',self.outro)

        form.addRow(QLabel('使用可能な変数：{会社名}、{担当者}、{工事概要}（工事詳細は自動挿入）'))

        b=QPushButton('定型文を保存');b.clicked.connect(self.save);form.addRow(b)

 

    def save(self):

        values={'subject':self.subject.text(),'intro':self.intro.toPlainText(),'outro':self.outro.toPlainText()}

        with db() as con:

            for k,v in values.items(): con.execute('INSERT OR REPLACE INTO settings(key,value) VALUES (?,?)',(k,v))

        QMessageBox.information(self,'保存','定型文を保存しました。')

 

def suggest_work_type(title, records):

    """過去の件名に含まれる明確な語句だけで候補を返す。曖昧ならNone。"""

    import unicodedata

    t = unicodedata.normalize('NFKC', title).upper()

    # 詳細な語句を優先。機械補修か電気補修か不明な「ポンプ補修」等は推定しない。

    rules = [

        (('モータ', '解結線'), 'モータ解結線'),

        (('MOTOR', '解結線'), 'モータ解結線'),

        (('モータ', '整備'), 'モータ整備'),

        (('MOTOR', '交換'), 'モータ交換・更新'),

        (('ブラシ', '交換'), 'スリップリングブラシ交換'),

        (('MCC', 'ブレーカ'), '遮断器交換'),

        (('MCC', '補修'), 'MCC補修'),

        (('LED', '更新'), 'LED照明更新'),

        (('LED', '交換'), 'LED照明更新'),

        (('外灯', '補修'), '外灯補修'),

        (('照明', '補修'), '電灯補修'),

        (('電灯', '補修'), '電灯補修'),

        (('コンセント', '補修'), 'コンセント補修'),

        (('コンセント', '設置'), 'コンセント新設・増設'),

        (('コンセント', '増設'), 'コンセント新設・増設'),

        (('シーケンス', '変更'), 'シーケンス変更'),

        (('カメラ', '移設'), '監視カメラ移設'),

        (('カメラ', '設置'), '監視カメラ設置'),

        (('カメラ', '補修'), '監視カメラ補修'),

        (('ページング', '補修'), 'ページング補修'),

        (('自火報', '感知器'), '自火報感知器交換'),

        (('接地抵抗', '測定'), '接地抵抗測定'),

        (('絶縁抵抗', '測定'), '絶縁抵抗測定'),

        (('漏電', '調査'), '漏電調査'),

        (('ケーブル', '敷設'), 'ケーブル敷設'),

        (('電線管', '補修'), '電線管補修'),

        (('インバータ', '交換'), 'インバータ補修・交換'),

        (('インバーター', '補修'), 'インバータ補修・交換'),

    ]

    for terms, name in rules:

        if all(term in t for term in terms):

            return next((r for r in records if r['name'] == name), None)

    return None

 

class WorkItemDialog(QDialog):

    def __init__(self,parent=None, item=None):

        super().__init__(parent)

        self.setWindowTitle('工事内容の追加・編集')

        self.resize(610,580)

        layout=QVBoxLayout(self)

        form=QFormLayout()

        self.type_combo=QComboBox()

        self.types=fetch_types()

        for r in self.types:

            self.type_combo.addItem(f"{r['category']} / {r['name']}",r['id'])

        self.past_title = QLineEdit()

        self.past_title.setPlaceholderText('過去の工事件名を貼り付けて候補を検索（任意）')

        suggest_row = QHBoxLayout()

        suggest_row.addWidget(self.past_title, 1)

        suggest_button = QPushButton('分類候補を提案')

        suggest_button.clicked.connect(self.apply_suggestion)

        suggest_row.addWidget(suggest_button)

        layout.addLayout(suggest_row)

        self.suggest_info = QLabel('※ 自動判定は候補表示のみ。曖昧な件名は手動で選択してください。')

        layout.addWidget(self.suggest_info)

        self.place=QLineEdit()

        self.equipment=QLineEdit()

        self.description=QTextEdit()

        self.description.setMaximumHeight(90)

        form.addRow('工事種類',self.type_combo)

        form.addRow('工事場所',self.place)

        form.addRow('設備名称',self.equipment)

        form.addRow('作業内容・特記事項',self.description)

        layout.addLayout(form)

        group=QGroupBox('工事種類別の入力項目')

        self.dynamic_form=QFormLayout(group)

        layout.addWidget(group)

        self.dynamic_widgets={}

        self.type_combo.currentIndexChanged.connect(self.rebuild_fields)

        if item:

            idx=self.type_combo.findData(item['type_id'])

            if idx>=0:self.type_combo.setCurrentIndex(idx)

            self.place.setText(item['place'])

            self.equipment.setText(item['equipment'])

            self.description.setPlainText(item['description'])

        self.rebuild_fields()

        if item:

            for name,value in item['fields'].items():

                if name in self.dynamic_widgets:self.dynamic_widgets[name].setText(value)

        layout.addStretch()

        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)

        buttons.accepted.connect(self.validate);buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

 

    def apply_suggestion(self):

        record = suggest_work_type(self.past_title.text(), self.types)

        if record is None:

            self.suggest_info.setText('判定できませんでした。工事種類を手動で選択してください。')

            return

        index = self.type_combo.findData(record['id'])

        if index >= 0:

            self.type_combo.setCurrentIndex(index)

            self.suggest_info.setText(f"候補：{record['category']} / {record['name']}（確認してから登録してください）")

 

    def rebuild_fields(self):

        while self.dynamic_form.rowCount(): self.dynamic_form.removeRow(0)

        self.dynamic_widgets={}

        r=self.current_type()

        if not r:return

        for name in json.loads(r['fields_json']):

            w=QLineEdit()

            if '日' in name: w.setPlaceholderText('例：2026/11/07 午前（未定も可）')

            self.dynamic_form.addRow(name,w)

            self.dynamic_widgets[name]=w

 

    def current_type(self):

        id_=self.type_combo.currentData()

        return next((r for r in self.types if r['id']==id_),None)

 

    def validate(self):

        if not self.current_type(): return alert(self,'工事種類を登録してください。')

        if not self.place.text().strip():return alert(self,'工事場所を入力してください。')

        self.accept()

 

    def value(self):

        r=self.current_type()

        return {'type_id':r['id'],'category':r['category'],'type_name':r['name'],

                'place':self.place.text().strip(),'equipment':self.equipment.text().strip(),

                'description':self.description.toPlainText().strip(),

                'fields':{k:w.text().strip() for k,w in self.dynamic_widgets.items()}}

 

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle('電気工事依頼メール作成アプリ')

        self.resize(1440, 850)

        self.setMinimumSize(1080, 660)

        self.items = []

        self.attachments = []

        self._updating = False

        self._preview_dirty = False

        self.preview_dialog = None

        self.build_ui()

        self.refresh_companies()

        self.refresh_history()

        self.setStyleSheet("""

            QWidget { font-family: 'Yu Gothic UI', 'Meiryo'; font-size: 13px; color: #243248; }

            QMainWindow, QStackedWidget { background: #f5f7fb; }

            QFrame#Sidebar { background: #eaf0f8; border-radius: 12px; }

            QFrame#Panel { background: white; border: 1px solid #e0e6ef; border-radius: 12px; }

            QLabel#Title { font-size: 20px; font-weight: 700; }

            QLabel#Section { font-size: 15px; font-weight: 700; }

            QLabel#Hint { color: #68788e; font-size: 12px; }

            QPushButton { padding: 9px 13px; border: 1px solid #d6deea; border-radius: 7px; background: white; }

            QPushButton:hover { background: #e9f2ff; }

            QPushButton#Primary { background: #2463b5; color: white; border-color: #2463b5; font-weight: 700; }

            QPushButton#Primary:hover { background: #1a4e92; }

            QPushButton#Nav { text-align: left; padding: 13px 12px; border: none; background: transparent; }

            QPushButton#Nav:checked { background: #d6e5fa; color: #174f97; font-weight: 700; }

            QLineEdit, QComboBox, QTextEdit, QListWidget, QTableWidget { background: white; border: 1px solid #cfd8e5; border-radius: 6px; padding: 7px; }

            QLineEdit, QComboBox { min-height: 27px; }

            QTableWidget { gridline-color: #edf0f5; }

            QHeaderView::section { background: #eef3fa; padding: 9px; border: none; font-weight: 700; }

        """)

 

    def panel(self, title):

        frame = QFrame()

        frame.setObjectName('Panel')

        lay = QVBoxLayout(frame)

        lay.setContentsMargins(20, 20, 20, 20)

        lay.setSpacing(13)

        heading = QLabel(title)

        heading.setObjectName('Section')

        lay.addWidget(heading)

        return frame, lay

 

    def build_ui(self):

        root = QWidget()

        self.setCentralWidget(root)

        outer = QHBoxLayout(root)

        outer.setContentsMargins(14, 14, 14, 14)

        outer.setSpacing(14)

        side = QFrame()

        side.setObjectName('Sidebar')

        side.setFixedWidth(185)

        nav = QVBoxLayout(side)

        nav.setContentsMargins(12, 18, 12, 12)

        nav.setSpacing(7)

        title = QLabel('電気工事依頼')

        title.setObjectName('Title')

        nav.addWidget(title)

        nav.addSpacing(16)

        self.stack = QStackedWidget()

        names = ['工事依頼作成', '工事種類管理', '協力会社管理', 'メール定型文', '作成履歴']

        self.nav_buttons = []

        for i, name in enumerate(names):

            btn = QPushButton(name)

            btn.setObjectName('Nav')

            btn.setCheckable(True)

            btn.clicked.connect(lambda checked=False, index=i: self.switch_page(index))

            nav.addWidget(btn)

            self.nav_buttons.append(btn)

        nav.addStretch()

        hint = QLabel('登録データは各PCの\nDocumentsに保存')

        hint.setObjectName('Hint')

        nav.addWidget(hint)

        outer.addWidget(side)

        outer.addWidget(self.stack, 1)

        self.create_tab = QWidget()

        self.stack.addWidget(self.create_tab)

        self.build_create_tab()

        self.type_manager = WorkTypeManager(self.refresh_types)

        self.stack.addWidget(self.type_manager)

        self.company_manager = CompanyManager(self.refresh_companies)

        self.stack.addWidget(self.company_manager)

        self.template_manager = TemplateManager()

        self.stack.addWidget(self.template_manager)

        self.history_tab = QWidget()

        self.stack.addWidget(self.history_tab)

        self.build_history()

        self.switch_page(0)

 

    def switch_page(self, index):

        self.stack.setCurrentIndex(index)

        for i, btn in enumerate(self.nav_buttons):

            btn.setChecked(i == index)

        if index == 4:

            self.refresh_history()

 

    def build_create_tab(self):

        root = QVBoxLayout(self.create_tab)

        root.setContentsMargins(0, 0, 0, 0)

        root.setSpacing(12)

        header = QLabel('新規工事依頼')

        header.setObjectName('Title')

        root.addWidget(header)

        hint = QLabel('中央の工事を選ぶと右側に詳細が表示されます。複数工事を1通にまとめられます。')

        hint.setObjectName('Hint')

        root.addWidget(hint)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        root.addWidget(splitter, 1)

 

        left, left_layout = self.panel('依頼する工事')

        left_layout.addWidget(QLabel('依頼先協力会社'))

        self.company_combo = QComboBox()

        left_layout.addWidget(self.company_combo)

        self.work_table = QTableWidget(0, 3)

        self.work_table.setHorizontalHeaderLabels(['工事種類', '工事場所', '設備名称'])

        self.work_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.work_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.work_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.work_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.work_table.verticalHeader().setVisible(False)

        self.work_table.itemSelectionChanged.connect(self.load_detail)

        left_layout.addWidget(self.work_table, 1)

        row = QHBoxLayout()

        for label, fn in [('＋ 工事追加', self.add_item), ('複製', self.duplicate_item), ('削除', self.delete_item)]:

            button = QPushButton(label)

            button.clicked.connect(fn)

            row.addWidget(button)

        left_layout.addLayout(row)

        left_layout.addWidget(QLabel('添付資料'))

        self.attachment_list = QListWidget()

        self.attachment_list.setMaximumHeight(95)

        left_layout.addWidget(self.attachment_list)

        attach = QHBoxLayout()

        for label, fn in [('ファイル追加', self.add_attachments), ('選択削除', self.delete_attachment)]:

            button = QPushButton(label)

            button.clicked.connect(fn)

            attach.addWidget(button)

        left_layout.addLayout(attach)

        splitter.addWidget(left)

 

        right, right_layout = self.panel('選択した工事の詳細')

        self.empty_hint = QLabel('左側の「＋ 工事追加」から工事を登録してください。')

        self.empty_hint.setObjectName('Hint')

        right_layout.addWidget(self.empty_hint)

        self.detail_scroll = QScrollArea()

        self.detail_scroll.setWidgetResizable(True)

        self.detail_scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()

        form_layout = QVBoxLayout(content)

        form_layout.setContentsMargins(4, 8, 12, 8)

        form_layout.setSpacing(16)

        self.type_combo = QComboBox()

        self.place = QLineEdit()

        self.equipment = QLineEdit()

        self.description = QTextEdit()

        self.description.setMinimumHeight(100)

        self.description.setMaximumHeight(170)

        for name, widget in [('工事種類', self.type_combo), ('工事場所', self.place), ('設備名称', self.equipment), ('作業内容・特記事項', self.description)]:

            form_layout.addWidget(QLabel(name))

            form_layout.addWidget(widget)

        self.dynamic_group = QGroupBox('工事種類別の入力項目')

        self.dynamic_form = QFormLayout(self.dynamic_group)

        self.dynamic_form.setSpacing(13)

        form_layout.addWidget(self.dynamic_group)

        form_layout.addStretch()

        self.detail_scroll.setWidget(content)

        right_layout.addWidget(self.detail_scroll, 1)

        splitter.addWidget(right)

        splitter.setSizes([490, 680])

        self.dynamic_widgets = {}

        self.type_combo.currentIndexChanged.connect(self.change_type)

        self.place.textChanged.connect(lambda v: self.save_field('place', v))

        self.equipment.textChanged.connect(lambda v: self.save_field('equipment', v))

        self.description.textChanged.connect(lambda: self.save_field('description', self.description.toPlainText()))

        self.detail_scroll.setEnabled(False)

        footer = QHBoxLayout()

        footer.addStretch()

        preview = QPushButton('メールプレビューを開く')

        preview.setObjectName('Primary')

        preview.clicked.connect(self.open_preview)

        footer.addWidget(preview)

        root.addLayout(footer)

 

    def refresh_types(self):

        current = self.type_combo.currentData()

        self._updating = True

        self.type_combo.clear()

        for record in fetch_types():

            self.type_combo.addItem(f"{record['category']} / {record['name']}", record['id'])

        index = self.type_combo.findData(current)

        if index >= 0:

            self.type_combo.setCurrentIndex(index)

        self._updating = False

        self.load_detail()

 

    def load_detail(self):

        row = self.work_table.currentRow()

        exists = 0 <= row < len(self.items)

        self.detail_scroll.setEnabled(exists)

        self.empty_hint.setVisible(not exists)

        if not exists:

            return

        item = self.items[row]

        self._updating = True

        self.type_combo.clear()

        for record in fetch_types():

            self.type_combo.addItem(f"{record['category']} / {record['name']}", record['id'])

        idx = self.type_combo.findData(item['type_id'])

        if idx >= 0:

            self.type_combo.setCurrentIndex(idx)

        else:

            self.type_combo.insertItem(0, f"{item['category']} / {item['type_name']}（削除済み）", item['type_id'])

            self.type_combo.setCurrentIndex(0)

        self.place.setText(item['place'])

        self.equipment.setText(item['equipment'])

        self.description.setPlainText(item['description'])

        self.rebuild_dynamic(item)

        self._updating = False

 

    def rebuild_dynamic(self, item):

        while self.dynamic_form.rowCount():

            self.dynamic_form.removeRow(0)

        self.dynamic_widgets = {}

        record = next((r for r in fetch_types() if r['id'] == item['type_id']), None)

        names = json.loads(record['fields_json']) if record else list(item['fields'])

        for name in names:

            widget = QLineEdit(item['fields'].get(name, ''))

            if '日' in name:

                widget.setPlaceholderText('例：2026/11/07 午前（未定も可）')

            widget.textChanged.connect(lambda value, key=name: self.save_dynamic(key, value))

            self.dynamic_form.addRow(name, widget)

            self.dynamic_widgets[name] = widget

 

    def save_field(self, key, value):

        row = self.work_table.currentRow()

        if self._updating or not 0 <= row < len(self.items):

            return

        self.items[row][key] = value

        if key in ('place', 'equipment'):

            self.work_table.blockSignals(True)

            self.work_table.item(row, 1 if key == 'place' else 2).setText(value)

            self.work_table.blockSignals(False)

        self._preview_dirty = True

 

    def save_dynamic(self, key, value):

        row = self.work_table.currentRow()

        if not self._updating and 0 <= row < len(self.items):

            self.items[row]['fields'][key] = value

            self._preview_dirty = True

 

    def change_type(self):

        row = self.work_table.currentRow()

        if self._updating or not 0 <= row < len(self.items):

            return

        record = next((r for r in fetch_types() if r['id'] == self.type_combo.currentData()), None)

        if not record:

            return

        item = self.items[row]

        item.update(type_id=record['id'], category=record['category'], type_name=record['name'])

        item['fields'] = {name: item['fields'].get(name, '') for name in json.loads(record['fields_json'])}

        self.work_table.item(row, 0).setText(item['type_name'])

        self._updating = True

        self.rebuild_dynamic(item)

        self._updating = False

        self._preview_dirty = True

 

    def open_preview(self):

        if not self.items:

            return alert(self, '工事を1件以上追加してください。')

        if not self.selected_company():

            return alert(self, '協力会社を登録・選択してください。')

        dialog = QDialog(self)

        dialog.setWindowTitle('メールプレビュー・Outlook作成')

        dialog.resize(900, 700)

        layout = QVBoxLayout(dialog)

        layout.setContentsMargins(22, 22, 22, 22)

        layout.setSpacing(12)

        layout.addWidget(QLabel('件名（編集可能）'))

        self.subject = QLineEdit()

        layout.addWidget(self.subject)

        layout.addWidget(QLabel('本文（編集可能）'))

        self.body = QTextEdit()

        layout.addWidget(self.body, 1)

        self.generate_preview()

        bar = QHBoxLayout()

        regen = QPushButton('定型文から再生成')

        regen.clicked.connect(self.confirm_regenerate)

        bar.addWidget(regen)

        bar.addStretch()

        outlook = QPushButton('Outlookメールを作成')

        outlook.setObjectName('Primary')

        outlook.clicked.connect(self.create_outlook)

        bar.addWidget(outlook)

        layout.addLayout(bar)

        layout.addWidget(QLabel('※ Outlook画面を表示するだけで、自動送信はしません。'))

        self.preview_dialog = dialog

        dialog.exec()

        self.preview_dialog = None

 

    def confirm_regenerate(self):

        if QMessageBox.question(self, '確認', '編集中の件名・本文を上書きして再生成しますか？') == QMessageBox.StandardButton.Yes:

            self.generate_preview()

 

    def refresh_companies(self):

        old=self.company_combo.currentData()

        self.company_combo.clear()

        for r in fetch_companies():self.company_combo.addItem(r['name'],r['id'])

        if old is not None:

            idx=self.company_combo.findData(old)

            if idx>=0:self.company_combo.setCurrentIndex(idx)

 

    def selected_company(self):

        id_=self.company_combo.currentData()

        return next((r for r in fetch_companies() if r['id']==id_),None)

 

    def refresh_items(self, select_row=None):

        self.work_table.blockSignals(True)

        previous = self.work_table.currentRow() if select_row is None else select_row

        self.work_table.setRowCount(len(self.items))

        for i,r in enumerate(self.items):

            details=' / '.join(f'{k}:{v}' for k,v in r['fields'].items() if v)

            for j,text in enumerate((r['type_name'],r['place'],r['equipment'])):

                self.work_table.setItem(i,j,QTableWidgetItem(text))

        self.work_table.blockSignals(False)

        if self.items:

            self.work_table.selectRow(min(max(previous, 0), len(self.items)-1))

        else:

            self.load_detail()

 

    def add_item(self):

        d=WorkItemDialog(self)

        if not d.types:return alert(self,'先に工事種類を登録してください。')

        if d.exec()==QDialog.DialogCode.Accepted:

            self.items.append(d.value());self.refresh_items(len(self.items)-1)

 

    def edit_item(self):

        i=self.work_table.currentRow()

        if not 0<=i<len(self.items):return alert(self,'編集する工事を選択してください。')

        d=WorkItemDialog(self,self.items[i])

        if d.exec()==QDialog.DialogCode.Accepted:

            self.items[i]=d.value();self.refresh_items()

 

    def duplicate_item(self):

        i=self.work_table.currentRow()

        if not 0<=i<len(self.items):return alert(self,'複製する工事を選択してください。')

        self.items.append(json.loads(json.dumps(self.items[i],ensure_ascii=False)))

        self.refresh_items(len(self.items)-1)

 

    def delete_item(self):

        i=self.work_table.currentRow()

        if not 0<=i<len(self.items):return alert(self,'削除する工事を選択してください。')

        self.items.pop(i);self.refresh_items(i)

 

    def add_attachments(self):

        paths,_=QFileDialog.getOpenFileNames(self,'添付ファイルを選択')

        for path in paths:

            if path not in self.attachments:self.attachments.append(path)

        self.refresh_attachments()

 

    def delete_attachment(self):

        i=self.attachment_list.currentRow()

        if 0<=i<len(self.attachments):self.attachments.pop(i)

        self.refresh_attachments()

 

    def refresh_attachments(self):

        self.attachment_list.clear();self.attachment_list.addItems(self.attachments)

 

    @staticmethod

    def replace_tokens(text, tokens):

        for k,v in tokens.items():text=text.replace('{'+k+'}',str(v))

        return text

 

    def generate_preview(self):

        if not self.items:return alert(self,'工事を1件以上追加してください。')

        c=self.selected_company()

        if not c:return alert(self,'協力会社を登録・選択してください。')

        s=settings()

        overview=self.items[0]['type_name'] if len(self.items)==1 else f"{self.items[0]['type_name']}ほか{len(self.items)-1}件"

        tokens={'会社名':c['name'],'担当者':c['contact'] or 'ご担当者','工事概要':overview}

        subject=self.replace_tokens(s.get('subject','【工事依頼】{工事概要}'),tokens)

        intro=self.replace_tokens(s.get('intro',''),tokens)

        outro=self.replace_tokens(s.get('outro',''),tokens)

        sections=[]

        for n,item in enumerate(self.items,1):

            lines=[f'【工事{n}】{item["type_name"]}',f'工事場所：{item["place"]}']

            if item['equipment']:lines.append(f'設備名称：{item["equipment"]}')

            for k,v in item['fields'].items():

                if v:lines.append(f'{k}：{v}')

            if item['description']:lines.append(f'作業内容・特記事項：\n{item["description"]}')

            sections.append('\n'.join(lines))

        self.subject.setText(subject)

        self.body.setPlainText(intro+'\n\n'+'\n\n'.join(sections)+'\n\n'+outro)

 

    def create_outlook(self):

        if not self.items:

            return alert(self, '工事を1件以上追加してください。')

        c = self.selected_company()

        if not c or not (c['email'] or '').strip():

            return alert(self, '協力会社の宛先メールアドレスを登録してください。')

        if not self.preview_dialog or not self.subject.text().strip() or not self.body.toPlainText().strip():

            return alert(self, 'プレビューで件名・本文を確認してください。')

        missing = [p for p in self.attachments if not Path(p).is_file()]

        if missing:

            return alert(self, '添付ファイルが見つかりません：\n' + '\n'.join(missing))

        try:

            import html

            import re

            import win32com.client

 

            outlook = win32com.client.Dispatch('Outlook.Application')

            mail = outlook.CreateItem(0)

            # Outlookの新規メール画面を先に表示し、既定の署名を読み込む。

            mail.Display()

            signature_html = mail.HTMLBody or ''

 

            # HTMLを安全にエスケープして、署名の前へ本文を挿入する。

            body_html = html.escape(self.body.toPlainText()).replace('\n', '<br>')

            new_content = (

                '<div style="font-family:Meiryo, sans-serif;font-size:11pt;">'

                + body_html + '</div><br>'

            )

            body_tag = re.search(r'<body\b[^>]*>', signature_html, re.IGNORECASE)

            if body_tag:

                pos = body_tag.end()

                mail.HTMLBody = signature_html[:pos] + new_content + signature_html[pos:]

            else:

                mail.HTMLBody = '<html><body>' + new_content + signature_html + '</body></html>'

 

            mail.To = c['email']

            mail.CC = c['cc'] or ''

            mail.Subject = self.subject.text()

            for p in self.attachments:

                mail.Attachments.Add(str(Path(p).resolve()))

        except Exception as e:

            return QMessageBox.critical(

                self, 'Outlook連携エラー',

                f'従来版Outlookが利用可能か確認してください。\n\n{e}'

            )

        try:

            with db() as con:

                con.execute(

                    'INSERT INTO history(created_at,company,subject,body,items_json,attachments_json,status) VALUES (?,?,?,?,?,?,?)',

                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), c['name'],

                     self.subject.text(), self.body.toPlainText(),

                     json.dumps(self.items, ensure_ascii=False),

                     json.dumps(self.attachments, ensure_ascii=False),

                     'Outlook画面を表示（送信未確認）')

                )

            self.refresh_history()

        except Exception as e:

            QMessageBox.warning(

                self, '履歴保存エラー',

                f'Outlook画面は開きましたが履歴を保存できませんでした。\n{e}'

            )

 

    def build_history(self):

        layout=QVBoxLayout(self.history_tab)

        self.history_table=QTableWidget(0,4)

        self.history_table.setHorizontalHeaderLabels(['作成日時','協力会社','件名','状態'])

        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        layout.addWidget(self.history_table)

        b=QPushButton('選択履歴の本文を表示');b.clicked.connect(self.show_history);layout.addWidget(b)

        self.refresh_history()

 

    def refresh_history(self):

        with db() as con:self.history_records=[dict(r) for r in con.execute('SELECT * FROM history ORDER BY id DESC LIMIT 500')]

        self.history_table.setRowCount(len(self.history_records))

        for i,r in enumerate(self.history_records):

            for j,key in enumerate(('created_at','company','subject','status')):

                self.history_table.setItem(i,j,QTableWidgetItem(r[key] or ''))

 

    def show_history(self):

        i=self.history_table.currentRow()

        if not 0<=i<len(self.history_records):return alert(self,'履歴を選択してください。')

        r=self.history_records[i]

        d=QDialog(self);d.setWindowTitle('依頼履歴');d.resize(700,520)

        layout=QVBoxLayout(d)

        layout.addWidget(QLabel(r['subject']))

        body=QTextEdit(r['body']);body.setReadOnly(True);layout.addWidget(body)

        b=QPushButton('閉じる');b.clicked.connect(d.accept);layout.addWidget(b)

        d.exec()

 

def main():

    init_db()

    app=QApplication(sys.argv)

    app.setStyle('Fusion')

    w=MainWindow();w.show()

    sys.exit(app.exec())

 

if __name__=='__main__':

    main()