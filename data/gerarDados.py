# -*- coding: utf-8 -*-

"""
Gera dados aleatórios para o arquivo de entrada.
Cria os arquivos com dados para os seguintes formatos de dados:
- CSV
- JSON
- XML
- Excel
- PostgreSQL

Para executar o script, execute o seguinte comando no terminal:
python gerarDados.py

Criado por: Maxwell Anderson Ielpo do Amaral
Data: 2019-10-01
Versão 1.0.0
Licença: Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import random

from datetime import datetime, timedelta
from faker import Faker
import faker_commerce


class Product:
    """
    Produto
    """

    def __init__(
        self,
        name: str,
        date: datetime = datetime.now(),
        warranty_days: int = 365,
        extended_warranty_days: int = 0,
        price: float = 0.0,
        discount: float = 0.0,
        quantity: int = 1,
        extended_warranty_price: float = 0.0,
    ):
        # Nome do produto
        self.name = name
        # Data de compra
        self.date = date
        # Dias de garantia
        self.warranty_days = warranty_days
        # Dias de garantia estendida
        self.extended_warranty_days = extended_warranty_days
        # Preço
        self.price = price
        # Desconto
        self.discount = discount
        # Quantidade
        self.quantity = quantity
        # Preço da garantia estendida
        self.extended_warranty_price = extended_warranty_price

    @property
    def date_final(self) -> datetime.date:
        """
        Data final da garantia
        :return: Data final da garantia
        """
        return (
            self.date
            + timedelta(days=self.warranty_days)
            + timedelta(days=self.extended_warranty_days)
        )

    @property
    def price_liquid(self) -> float:
        """
        Preço líquido
        :return: Preço líquido
        """
        return self.price - self.discount

    @property
    def price_final(self) -> float:
        """
        Preço final
        :return: Preço final
        """
        return self.price_liquid * self.quantity

    @property
    def extended_warranty_price_final(self) -> float:
        """
        Preço final com garantia estendida
        :return: Preço final com garantia estendida
        """
        return self.price_final + self.extended_warranty_price

    def __str__(self):
        """
        Representação textual do produto
        :return: Representação textual do produto
        """
        return (
            f"Nome: {self.name}\n"
            f"Data de compra: {self.date}\n"
            f"Data de final da garantia: {self.date_final}\n"
            f"Preço: {self.price}\n"
            f"Desconto: {self.discount}\n"
            f"Preço líquido: {self.price_liquid}\n"
            f"Preço final: {self.price_final}\n"
            f"Quantidade: {self.quantity}\n"
            f"Preço da garantia estendida: {self.extended_warranty_price}\n"
            f"Preço final com garantia estendida: {self.extended_warranty_price_final}\n"
        )


class DataGenerator:
    """
    Gerador de dados aleatórios
    """

    def __init__(self, seed: int = None):
        """
        Inicialização
        :param seed: Semente para a geração de números aleatórios
        """
        # Gera números aleatórios
        self.random = random.Random(seed)
        # Gera dados aleatórios
        self.fake = Faker()
        self.fake.add_provider(faker_commerce.Provider)
        # Datas de compra
        self.dates = []
        # Dias de garantia
        self.warranty_days = []
        # Dias de garantia estendida
        self.extended_warranty_days = []
        # Preços
        self.prices = []
        # Descontos
        self.discounts = []
        # Quantidades
        self.quantities = []
        # Preços da garantia estendida
        self.extended_warranty_prices = []

    def generate(self, n: int = 1):
        """
        Gera dados aleatórios
        :param n: Número de dados a serem gerados
        :return: Dados gerados
        """
        # Gera dados aleatórios
        self.dates = [
            datetime(
                self.random.randint(2010, 2019),
                self.random.randint(1, 12),
                self.random.randint(1, 28),
            )
            for _ in range(n)
        ]
        self.warranty_days = [self.random.choice([90, 180, 365]) for _ in range(n)]
        self.extended_warranty_days = [
            self.random.choice([365, 365 * 2, 365 * 3, 365 * 4]) for _ in range(n)
        ]
        self.prices = [self.random.uniform(100, 10000) for _ in range(n)]
        self.discounts = [self.random.uniform(0, 50) for _ in range(n)]
        self.quantities = [self.random.randint(1, 10) for _ in range(n)]
        self.extended_warranty_prices = [self.random.uniform(10, 100) for _ in range(n)]

        return [
            Product(
                self.fake.ecommerce_name(),
                self.dates[i],
                self.warranty_days[i],
                self.extended_warranty_days[i],
                self.prices[i],
                self.discounts[i],
                self.quantities[i],
                self.extended_warranty_prices[i],
            )
            for i in range(n)
        ]

    def generate_excel_datafile(self, n: int = 1):
        """
        Gera dados aleatórios e salva em um arquivo do Excel
        :param n: Número de dados a serem gerados
        """
        # Gera dados aleatórios
        products = self.generate(n)

        # Salva os dados em um arquivo do Excel
        import xlsxwriter

        workbook = xlsxwriter.Workbook("data.xlsx")
        worksheet = workbook.add_worksheet()

        # Escreve os dados com o cabeçalho
        worksheet.write(0, 0, "Nome")
        worksheet.write(0, 1, "Data de compra")
        worksheet.write(0, 2, "Data de final da garantia")
        worksheet.write(0, 3, "Preço")
        worksheet.write(0, 4, "Desconto")
        worksheet.write(0, 5, "Preço líquido")
        worksheet.write(0, 6, "Preço final")
        worksheet.write(0, 7, "Quantidade")
        worksheet.write(0, 8, "Preço da garantia estendida")
        worksheet.write(0, 9, "Preço final com garantia estendida")
        for i, product in enumerate(products):
            worksheet.write(i + 1, 0, product.name)
            worksheet.write(i + 1, 1, product.date)
            worksheet.write(i + 1, 2, product.date_final)
            worksheet.write(i + 1, 3, product.price)
            worksheet.write(i + 1, 4, product.discount)
            worksheet.write(i + 1, 5, product.price_liquid)
            worksheet.write(i + 1, 6, product.price_final)
            worksheet.write(i + 1, 7, product.quantity)
            worksheet.write(i + 1, 8, product.extended_warranty_price)
            worksheet.write(i + 1, 9, product.extended_warranty_price_final)

        workbook.close()

    def generate_xml_datafile(self, n: int = 1):
        """
        Gera dados aleatórios e salva em um arquivo XML
        :param n: Número de dados a serem gerados
        """
        # Gera dados aleatórios
        products = self.generate(n)

        # Salva os dados em um arquivo XML
        import xml.etree.ElementTree as ET

        root = ET.Element("root")
        for product in products:
            product_xml = ET.SubElement(root, "product")
            ET.SubElement(product_xml, "name").text = product.name
            ET.SubElement(product_xml, "date").text = str(product.date)
            ET.SubElement(product_xml, "date_final").text = str(product.date_final)
            ET.SubElement(product_xml, "price").text = str(product.price)
            ET.SubElement(product_xml, "discount").text = str(product.discount)
            ET.SubElement(product_xml, "price_liquid").text = str(product.price_liquid)
            ET.SubElement(product_xml, "price_final").text = str(product.price_final)
            ET.SubElement(product_xml, "quantity").text = str(product.quantity)
            ET.SubElement(
                product_xml, "extended_warranty_price"
            ).text = str(product.extended_warranty_price)
            ET.SubElement(
                product_xml, "extended_warranty_price_final"
            ).text = str(product.extended_warranty_price_final)

        tree = ET.ElementTree(root)
        tree.write("data.xml")

    def generate_csv_datafile(self, n: int = 1):
        """
        Gera dados aleatórios e salva em um arquivo CSV
        :param n: Número de dados a serem gerados
        """
        # Gera dados aleatórios
        products = self.generate(n)

        # Salva os dados em um arquivo CSV
        with open("data.csv", "w") as file:
            file.write(
                "Nome,Data de compra,Data de final da garantia,Preço,Desconto,Preço líquido,Preço final,Quantidade,Preço da garantia estendida,Preço final com garantia estendida\n"
            )
            for product in products:
                file.write(
                    f"{product.name},{product.date},{product.date_final},{product.price},{product.discount},{product.price_liquid},{product.price_final},{product.quantity},{product.extended_warranty_price},{product.extended_warranty_price_final}\n"
                )

    def generate_json_datafile(self, n: int = 1):
        """
        Gera dados aleatórios e salva em um arquivo JSON
        :param n: Número de dados a serem gerados
        """
        # Gera dados aleatórios
        products = self.generate(n)

        # Salva os dados em um arquivo JSON
        with open("data.json", "w") as file:
            file.write("[\n")
            for i, product in enumerate(products):
                file.write(
                    f'{{"Nome": "{product.name}", "Data de compra": "{product.date}", "Data de final da garantia": "{product.date_final}", "Preço": {product.price}, "Desconto": {product.discount}, "Preço líquido": {product.price_liquid}, "Preço final": {product.price_final}, "Quantidade": {product.quantity}, "Preço da garantia estendida": {product.extended_warranty_price}, "Preço final com garantia estendida": {product.extended_warranty_price_final}}}'
                )
                if i < len(products) - 1:
                    file.write(",\n")
                else:
                    file.write("\n")
            file.write("]")

    def generate_postgresql_script_datafile(self, n: int = 1):
        """
        Gera dados aleatórios e salva em um arquivo de script do PostgreSQL
        :param n: Número de dados a serem gerados
        """
        # Gera dados aleatórios
        products = self.generate(n)

        # Cria script para criar a tabela, sobrescrevendo caso já exista
        with open("create.sql", "w") as file:
            # Insere comentário sobre o tipo de banco de dados
            file.write("-- PostgreSQL\n")
            # Insere comando para criar a tabela
            file.write("DROP TABLE IF EXISTS products;\n")
            file.write("CREATE TABLE products (\n")
            file.write("    id SERIAL PRIMARY KEY,\n")
            file.write("    name VARCHAR(255) NOT NULL,\n")
            file.write("    date DATE NOT NULL,\n")
            file.write("    date_final DATE NOT NULL,\n")
            file.write("    price NUMERIC(10, 2) NOT NULL,\n")
            file.write("    discount NUMERIC(10, 2) NOT NULL,\n")
            file.write("    price_liquid NUMERIC(10, 2) NOT NULL,\n")
            file.write("    price_final NUMERIC(10, 2) NOT NULL,\n")
            file.write("    quantity INTEGER NOT NULL,\n")
            file.write("    extended_warranty_price NUMERIC(10, 2) NOT NULL,\n")
            file.write("    extended_warranty_price_final NUMERIC(10, 2) NOT NULL\n")
            file.write(");\n")

        # Salva os dados em um arquivo de script do PostgreSQL
        with open("data.sql", "w") as file:
            # Insere comentário sobre o tipo de banco de dados
            file.write("-- PostgreSQL\n")
            # Insere comando para inserir os dados
            for product in products:
                file.write(
                    f"INSERT INTO products (name, date, date_final, price, discount, price_liquid, price_final, quantity, extended_warranty_price, extended_warranty_price_final) VALUES ('{product.name}', '{product.date}', '{product.date_final}', {product.price}, {product.discount}, {product.price_liquid}, {product.price_final}, {product.quantity}, {product.extended_warranty_price}, {product.extended_warranty_price_final});\n"
                )


# Inicialização
if __name__ == "__main__":

    DATA_QTY = 100    

    # Gera dados aleatórios
    data_generator = DataGenerator()

    # Gerador de dados aleatórios e salva em um arquivo do Excel
    data_generator.generate_excel_datafile(DATA_QTY)

    # Gerador de dados aleatórios e salva em um arquivo XML
    data_generator.generate_xml_datafile(DATA_QTY)

    # Gerador de dados aleatórios e salva em um arquivo CSV
    data_generator.generate_csv_datafile(DATA_QTY)

    # Gerador de dados aleatórios e salva em um arquivo JSON
    data_generator.generate_json_datafile(DATA_QTY)

    # Gerador de dados aleatórios e salva em um arquivo de script do PostgreSQL
    data_generator.generate_postgresql_script_datafile(100)
    

