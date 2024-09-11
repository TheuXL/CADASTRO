import sys
from PyQt5 import uic, QtWidgets, QtCore
import pandas as pd
import os  

class CadastroProduto(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
       
        script_dir = os.path.dirname(os.path.abspath(__file__))
       
        ui_path = os.path.join(script_dir, "formulario2.ui")
        uic.loadUi(ui_path, self)
        self.df = pd.DataFrame(columns=["Nome", "Valor"])
        self.pushButton_cadastrar.clicked.connect(self.cadastrar_produto)
        self.pushButton_novo_produto.clicked.connect(self.abrir_cadastro)
        self.comboBox_disponibilidade.addItems(["Sim", "Não"])
        self.ordenacao_ascendente = True 

        self.tableWidget_produtos.setColumnCount(2)
        self.tableWidget_produtos.setHorizontalHeaderLabels(["Nome", "Valor"])
        self.tableWidget_produtos.horizontalHeader().sectionClicked.connect(self.ordenar_por_coluna)  
        self.atualizar_tabela()

        style_path = os.path.join(script_dir, "style.css")  
        with open(style_path, "r") as f:
            self.setStyleSheet(f.read())

    def cadastrar_produto(self):
        nome = self.lineEdit_nome.text()
        descricao = self.lineEdit_descricao.text()  
        valor = self.doubleSpinBox_valor.value()
        disponivel = self.comboBox_disponibilidade.currentText()

        self.df.loc[len(self.df)] = [nome, valor]
        self.df = self.df.sort_values("Valor", ascending=self.ordenacao_ascendente)  
       
        self.atualizar_tabela()

        self.lineEdit_nome.clear()
        self.lineEdit_descricao.clear()
        self.doubleSpinBox_valor.setValue(0.0)
        self.comboBox_disponibilidade.setCurrentIndex(0)

        self.tabWidget.setCurrentIndex(1) 

    def abrir_cadastro(self):
        self.tabWidget.setCurrentIndex(0)  

    def ordenar_por_coluna(self, coluna):
        if coluna == 1: 
            self.ordenacao_ascendente = not self.ordenacao_ascendente 
            self.df = self.df.sort_values("Valor", ascending=self.ordenacao_ascendente)
            self.atualizar_tabela()

    def atualizar_tabela(self):
        self.tableWidget_produtos.setRowCount(0)  
        for i, row in self.df.iterrows():
            row_position = self.tableWidget_produtos.rowCount()
            self.tableWidget_produtos.insertRow(row_position)
            self.tableWidget_produtos.setItem(row_position, 0, QtWidgets.QTableWidgetItem(row["Nome"]))
            self.tableWidget_produtos.setItem(row_position, 1, QtWidgets.QTableWidgetItem(f'{row["Valor"]:.2f}')) 



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CadastroProduto()
    window.show()
    sys.exit(app.exec())
